from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId 
import jwt
import os
import bcrypt 
from datetime import datetime, timedelta
from database import db

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "fdsjhcouwidhfocui3h4r780hfc0r78ehfdudsiarf3248r023984ryh0f3304hf08")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# User collection
users_collection = db["users"]

def hash_password(password: str) -> str:
    """
    Hashes the password using bcrypt.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a hashed password.
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(user_id: str) -> str:
    """
    Generates JWT access token.
    """
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_payload = {"user_id": user_id, "exp": expiration}
    return jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

def register_user(name: str, email: str, password: str):
    """
    Registers a new user.
    """
    if users_collection.find_one({"email": email}):
        return None  # Email already exists

    hashed_password = hash_password(password)
    user_data = {
        "name": name,
        "email": email,
        "password": hashed_password,
    }
    inserted_user = users_collection.insert_one(user_data)
    return str(inserted_user.inserted_id)

def authenticate_user(email: str, password: str):
    """
    Authenticates user login.
    """
    user = users_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return None

    access_token = create_access_token(str(user["_id"]))
    return {
        "user_id": str(user["_id"]),
        "access_token": access_token,
        "user_details": {
            "name": user["name"],
            "email": user["email"]
        }
    }


def decode_access_token(token: str):
    """
    Decodes and validates JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except jwt.ExpiredSignature.Error:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency to get the current user from JWT token.
    """
    user_id = decode_access_token(token)
    
    try:
        user = db["users"].find_one({"_id": ObjectId(user_id)})  # ✅ Convert to ObjectId
    except:
        raise HTTPException(status_code=401, detail="Invalid user ID format")

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user