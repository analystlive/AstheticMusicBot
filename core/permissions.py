from config import OWNER_ID
from database.mongo import sudo_users


def is_owner(user_id: int) -> bool:
    return str(user_id) == OWNER_ID


def is_sudo(user_id: int) -> bool:
    # Owner hamesha sudo hota hai
    if is_owner(user_id):
        return True

    return sudo_users.find_one({"user_id": user_id}) is not None


def add_sudo(user_id: int):
    sudo_users.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )


def remove_sudo(user_id: int):
    sudo_users.delete_one({"user_id": user_id})


def list_sudo():
    return [str(x["user_id"]) for x in sudo_users.find()]
