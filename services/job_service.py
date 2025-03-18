from database import db

# Static list of job roles
JOB_ROLES = [
    {"id": "software_engineer", "name": "Software Engineer", "description": "Software development and programming."},
    {"id": "data_scientist", "name": "Data Scientist", "description": "Machine learning and data analysis."},
    {"id": "backend_developer", "name": "Backend Developer", "description": "Server-side programming and databases."},
    {"id": "frontend_developer", "name": "Frontend Developer", "description": "Client-side programming and databases."},
    {"id": "data_engineer", "name": "Data Engineer", "description": "Data manipulation, ETL and databases."}
]

def get_job_roles():
    """
    Returns a list of available job roles.
    """
    return JOB_ROLES