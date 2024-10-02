from fastapi import APIRouter

router = APIRouter()


@router.get("/api/health")
async def healthCheck():
    return {"message": "success"}
