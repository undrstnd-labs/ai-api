from fastapi import APIRouter

router = APIRouter()


@router.get("/api/py/health")
async def healthCheck():
    return {"message": "success"}
