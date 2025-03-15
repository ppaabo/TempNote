from src.db import get_db


def save_message(data):
    db = get_db()
    try:
        with db.cursor() as cur:
            SQL = "INSERT INTO messages (ciphertext, iv, salt) VALUES (%s, %s, %s) RETURNING msg_id"
            cur.execute(
                SQL,
                (
                    data["ciphertext"],
                    data["iv"],
                    data["salt"],
                ),
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
            SQL = "SELECT ciphertext, iv, salt FROM messages WHERE msg_id = %s"
            cur.execute(SQL, (id,))
            message = cur.fetchone()
        if message:
            return {"ciphertext": message[0], "iv": message[1], "salt": message[2]}
    except Exception as e:
        print(f"get_message Error: {e}")
        return None
    return None


def delete_message(id):
    db = get_db()
    try:
        with db.cursor() as cur:
            SQL = "DELETE FROM messages WHERE msg_id = %s RETURNING msg_id"
            cur.execute(SQL, (id,))
            deleted_row = cur.fetchone()
        db.commit()
        if deleted_row:
            return True
    except Exception as e:
        print(f"delete_message Error: {e}")
        return False
    return False
