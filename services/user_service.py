from database import users_collection
from bson import ObjectId

def get_user_profile(user_id: str):
    """
    Fetch user profile details.
    """
    user = users_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0})  # Exclude password
    print(user)
    if not user:
        return None

    user["user_id"] = str(user["_id"])
    del user["_id"]
    return user


def update_user_profile(user_id: str, updates: dict):
    """
    Updates user profile information.
    """
    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updates})
    return result.modified_count > 0 