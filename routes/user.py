from fastapi import APIRouter, HTTPException, Depends
from services.auth_service import get_current_user
from models import UserProfileResponse, UpdateUserProfileRequest
from services.user_service import get_user_profile, update_user_profile

router = APIRouter()

@router.get("/api/user/profile", response_model=UserProfileResponse)
async def fetch_user_profile(user: dict = Depends(get_current_user)):
    """
    Fetch user profile details.
    """
    profile = get_user_profile(str(user["_id"]))  # ✅ Pass user["_id"] directly
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")

    return profile

@router.put("/api/user/profile")
async def modify_user_profile(update_data: UpdateUserProfileRequest, user: dict = Depends(get_current_user)):
    """
    Update the currently logged-in user's profile.
    """
    user_id = str(user["_id"])  # ✅ Extract user ID from the JWT token

    updates = update_data.dict(exclude_unset=True)  # ✅ Get only updated fields
    success = update_user_profile(user_id, updates)  # ✅ Update current user, not from request body

    if not success:
        raise HTTPException(status_code=400, detail="Failed to update profile")

    return {"message": "Profile updated successfully"} 