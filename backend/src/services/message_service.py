import psycopg
from src.db import get_db
from datetime import datetime, timedelta, timezone
from src.exceptions import MessageNotFound, DatabaseError, InvalidPayload
import uuid
import logging
import base64
import re

logger = logging.getLogger(__name__)
required_fields = ["ciphertext", "iv", "salt", "expiration_hours"]
max_hours = 336  # 14 days
min_hours = 1


def is_valid_base64(s):
    """
    Check if a string is valid base64 encoding.

    Args:
        s (str): String to validate as base64
    Returns:
        bool: True if string is valid base64
    """
    if not isinstance(s, str):
        return False

    # Regex pattern for standard Base64 charset
    pattern = r"^[A-Za-z0-9+/]+={0,2}$"
    if not re.match(pattern, s):
        return False

    if len(s) % 4 != 0:
        return False
    try:
        base64.b64decode(s)
        return True
    except Exception:
        return False


def validate_message(data):
    """
    Validates message data contains all required fields with proper values.

    Args:
        data (dict): Message data containing required fields
    Raises:
        InvalidPayload: If validation fails
    Returns:
        bool: True if validation passes
    """
    # Check that all required fields exist
    for field in required_fields:
        if field not in data:
            raise InvalidPayload(f"Missing required field: {field}")

        # Check if string fields are empty
        if isinstance(data[field], str) and data[field].strip() == "":
            raise InvalidPayload(f"Field '{field}' cannot be empty")

    # Check that expiration_hours is a valid value
    if not isinstance(data["expiration_hours"], int):
        raise InvalidPayload("expiration_hours must be an int")

    if (
        not min(min_hours, max_hours)
        <= data["expiration_hours"]
        <= max(min_hours, max_hours)
    ):
        raise InvalidPayload(
            f"expiration_hours must be between {min_hours} and {max_hours}"
        )

    # Validate Base64 format for crypto fields
    for field in ["ciphertext", "iv", "salt"]:
        if not is_valid_base64(data[field]):
            raise InvalidPayload(
                f"Field '{field}' must be a valid Base64-encoded string"
            )
    # Length validation based on expected values
    # IV should be 16 characters in Base64 (12 bytes)
    if len(data["iv"]) != 16:
        raise InvalidPayload("Invalid IV length - must be exactly 16 characters")

    # Salt should be 24 characters in Base64 (16 bytes)
    if len(data["salt"]) != 24:
        raise InvalidPayload("Invalid salt length - must be exactly 24 characters")

    return True


def validate_uuid(uuid_string):
    """
    Validates a string is a proper UUID format.

    Args:
        uuid_string (str): String to validate as UUID
    Raises:
        InvalidPayload: If UUID format is invalid
    Returns:
        uuid.UUID: Validated UUID object
    """
    try:
        return uuid.UUID(uuid_string)
    except ValueError as e:
        logger.warning(f"Invalid UUID format: {uuid_string} - {str(e)}")
        raise InvalidPayload(f"Invalid UUID format: {uuid_string}")


# Create a new message


def save_message(data):
    """
    Saves a new encrypted message to the database.

    Args:
        data (dict): Message data containing ciphertext, iv, salt and expiration_hours
    Raises:
        DatabaseError: If database operation fails
        InvalidPayload: If message data is invalid

    Returns:
        str: UUID of the created message
    """
    validate_message(data)
    db = get_db()
    try:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(hours=data["expiration_hours"])
        with db.cursor() as cur:
            SQL = "INSERT INTO messages (ciphertext, iv, salt, expires_at) VALUES (%s, %s, %s, %s) RETURNING msg_id"
            cur.execute(
                SQL,
                (data["ciphertext"], data["iv"], data["salt"], expires_at),
            )
            msg_id = cur.fetchone()[0]
        db.commit()

        if not msg_id:
            raise DatabaseError("Failed to save message")
        logger.info(f"Message with id: {msg_id} created")
        return msg_id

    except InvalidPayload as e:
        raise e
    except psycopg.Error as e:
        raise DatabaseError("Database insert failed") from e


# Fetch a message
def get_message(id):
    """
    Retrieves a message by its ID if it exists and hasn't expired.

    Args:
        id (str): UUID of the message to retrieve
    Raises:
        MessageNotFound: If message doesn't exist or has expired
        DatabaseError: If database operation fails
        InvalidPayload: If UUID format is invalid
    Returns:
        dict: Message data including ciphertext, iv, salt and timestamps
    """
    validate_uuid(id)
    db = get_db()
    now = datetime.now(timezone.utc)
    try:
        with db.cursor() as cur:
            SQL = "SELECT ciphertext, iv, salt, created_at, expires_at FROM messages WHERE msg_id = %s"
            cur.execute(SQL, (id,))
            message = cur.fetchone()

        if not message:
            raise MessageNotFound(f"Message {id} not found")

        # Check if the message has expired
        expires_at = message[4]
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at < now:
            logger.info(f"Message {id} has expired, deleting it")
            consume_message(id)
            raise MessageNotFound(f"Message {id} has expired and been deleted")

        return {
            "ciphertext": message[0],
            "iv": message[1],
            "salt": message[2],
            "created_at": message[3],
            "expires_at": message[4],
        }

    except psycopg.Error as e:
        raise DatabaseError("Database failure") from e


# Delete a message
def consume_message(id):
    """
    Deletes a message from the database by its ID.

    Args:
        id (str): UUID of the message to delete
    Raises:
        MessageNotFound: If message doesn't exist
        DatabaseError: If database operation fails
        InvalidPayload: If UUID format is invalid
    Returns:
        bool: True if message was successfully deleted
    """
    validate_uuid(id)
    db = get_db()

    try:
        with db.cursor() as cur:
            SQL = "DELETE FROM messages WHERE msg_id = %s RETURNING msg_id"
            cur.execute(
                SQL,
                (id,),
            )
            result = cur.fetchone()
        db.commit()

        if not result:
            raise MessageNotFound(f"Message with {id} not found or already expired")

        logger.info(f"Message with id: {id} deleted")

        return True

    except psycopg.Error as e:
        raise DatabaseError("Failed to delete message from database.") from e
