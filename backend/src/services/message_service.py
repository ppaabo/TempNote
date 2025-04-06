import psycopg
from src.db import get_db
from datetime import datetime, timedelta, timezone
from src.exceptions import MessageNotFound, DatabaseError, InvalidPayload


def validate_message(data):
    """Validate that the required fields are present and valid."""
    required_fields = ["ciphertext", "iv", "salt", "expiration_days"]
    for field in required_fields:
        if field not in data:
            raise InvalidPayload(f"Missing required field: {field}")

    if not isinstance(data["expiration_days"], int):
        raise InvalidPayload("expiration_days must be an integer")

    max_days = 14
    if data["expiration_days"] > max_days:
        raise InvalidPayload(
            f"expiration_days must be less than or equal to {max_days}"
        )

    return True


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

        return msg_id

    except InvalidPayload as e:
        raise e
    except psycopg.Error as e:
        raise DatabaseError("Database insert failed") from e


def get_message(id):
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


def consume_message(id):
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

        return True

    except psycopg.Error as e:
        raise DatabaseError("Failed to delete message from database.") from e
