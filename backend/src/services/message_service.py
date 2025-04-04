from src.db import get_db
from datetime import datetime, timedelta, timezone


def save_message(data):
    db = get_db()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=data["expiration_days"])
    try:
        with db.cursor() as cur:
            SQL = "INSERT INTO messages (ciphertext, iv, salt, expires_at) VALUES (%s, %s, %s, %s) RETURNING msg_id"
            cur.execute(
                SQL,
                (data["ciphertext"], data["iv"], data["salt"], expires_at),
            )
            msg_id = cur.fetchone()[0]
            db.commit()
            if msg_id:
                return msg_id
    except Exception as e:
        print(f"save_message Error: {e}")
        return None
    return None


def get_message(id):
    db = get_db()
    try:
        with db.cursor() as cur:
            SQL = "SELECT ciphertext, iv, salt, created_at, expires_at FROM messages WHERE msg_id = %s"
            cur.execute(SQL, (id,))
            message = cur.fetchone()
        if message:
            return {
                "ciphertext": message[0],
                "iv": message[1],
                "salt": message[2],
                "created_at": message[3],
                "expires_at": message[4],
            }
    except Exception as e:
        print(f"get_message Error: {e}")
        return None
    return None


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
        if result:
            return True
    except Exception as e:
        print(f"read_message error: {e}")
        return None
    return None
