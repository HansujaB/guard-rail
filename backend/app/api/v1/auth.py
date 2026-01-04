from fastapi import APIRouter
from app.schemas.common import StatusResponse

router = APIRouter()


@router.get("/divisions", response_model=list[dict])
async def get_divisions():
    """
    Get list of divisions for login page
    TODO: Implement authentication - currently returns mock data
    """
    return [
        {"id": "1", "name": "Northern Railway Division", "code": "NR"},
        {"id": "2", "name": "Western Railway Division", "code": "WR"},
        {"id": "3", "name": "Eastern Railway Division", "code": "ER"},
    ]


@router.post("/login", response_model=StatusResponse)
async def login():
    """
    Login endpoint
    TODO: Implement authentication - currently placeholder
    """
    return {"status": "success", "message": "Login endpoint - to be implemented"}

