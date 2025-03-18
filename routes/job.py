from fastapi import APIRouter, Depends
from services.auth_service import get_current_user
from services.auth_service import get_current_user
from services.job_service import get_job_roles

router = APIRouter()

@router.get("/api/job-roles")
async def fetch_job_roles(user: dict = Depends(get_current_user)):
    """
    Fetch the list of available job roles.
    """
    return get_job_roles()