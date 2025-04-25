import psycopg
from src.db import get_db
from datetime import datetime, timedelta, timezone
from src.exceptions import MessageNotFound, DatabaseError, InvalidPayload
import uuid
import logging

logger = logging.getLogger(__name__)


def validate_message(data):
    """Validate that the required fields are present and valid."""

    # Check that all required fields exist
    required_fields = ["ciphertext", "iv", "salt", "expiration_days"]
    for field in required_fields:
        if field not in data:
            raise InvalidPayload(f"Missing required field: {field}")

        # Check if string fields are empty
        if isinstance(data[field], str) and data[field].strip() == "":
            raise InvalidPayload(f"Field '{field}' cannot be empty")

    if not isinstance(data["expiration_days"], int):
        raise InvalidPayload("expiration_days must be an integer")

    if data["expiration_days"] <= 0:
        raise InvalidPayload("expiration_days must be greater than 0")

    max_days = 14
    if data["expiration_days"] > max_days:
        raise InvalidPayload(
            f"expiration_days must be less than or equal to {max_days}"
        )

    return True


# Check if given uuid_string is a valid
def validate_uuid(uuid_string):
    try:
        return uuid.UUID(uuid_string)
    except ValueError as e:
        logger.warning(f"Invalid UUID format: {uuid_string} - {str(e)}")
        raise InvalidPayload(f"Invalid UUID format: {uuid_string}")


# Create a new message
def save_message(data):
    db = get_db()

    try:
        validate_message(data)
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=data["expiration_days"])
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
    validate_uuid(id)
    db = get_db()
    try:
        with db.cursor() as cur:
            SQL = "SELECT ciphertext, iv, salt, created_at, expires_at FROM messages WHERE msg_id = %s"
            cur.execute(SQL, (id,))
            message = cur.fetchone()

        if not message:
            raise MessageNotFound(f"Message {id} not found")

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
    validate_uuid(id)
    db = get_db()
    now = datetime.now(timezone.utc)

    try:
        with db.cursor() as cur:
            SQL = "DELETE FROM messages WHERE msg_id = %s AND expires_at > %s RETURNING msg_id"
            cur.execute(
                SQL,
                (id, now),
            )
            result = cur.fetchone()
        db.commit()

        if not result:
            raise MessageNotFound(f"Message with {id} not found or already expired")

        logger.info(f"Message with id: {id} deleted")

        return True

    except psycopg.Error as e:
        raise DatabaseError("Failed to delete message from database.") from e
