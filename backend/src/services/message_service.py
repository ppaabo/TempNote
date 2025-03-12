import uuid

database = {}


def save_message(data):
    message_id = str(uuid.uuid4())[:8]
    database[message_id] = {
        "encrypted_msg": data["encrypted_message"],
        "iv": data["iv"],
        "salt": data["salt"],
    }
    return message_id


def get_message(message_id):
    return database.get(message_id)


def delete_message(message_id):
    return database.pop(message_id, None) is not None
