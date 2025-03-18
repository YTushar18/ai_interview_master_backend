from fastapi import APIRouter, HTTPException, Depends   
from models import User, UserLogin, AuthResponse
from services.auth_service import register_user, authenticate_user

router = APIRouter()

@router.post("/api/auth/register", response_model=AuthResponse)
async def register(user: User):
    """
    Register a new user.
    """
    user_id = register_user(user.name, user.email, user.password)
    if not user_id:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    access_token = authenticate_user(user.email, user.password)["access_token"]
    return {"user_id": user_id, "access_token": access_token}

@router.post("/api/auth/login", response_model=AuthResponse)
async def login(user: UserLogin):
    """
    Authenticate user and return JWT token.
    """
    auth_data = authenticate_user(user.email, user.password)
    if not auth_data:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return auth_data