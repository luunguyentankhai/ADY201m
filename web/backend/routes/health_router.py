from fastapi import APIRouter
from web.backend.core.ml_manager import ml_manager

router = APIRouter(prefix="/api/system", tags=["System Health"])

@router.get("/ml-status")
async def check_ml_status():

    status = ml_manager.get_status()

    if status["ai_engine_active"]:
        return {
                "status": "success",
                "message": "Models AI acting",
                "data": status,
            }
    return {
            "status": "error",
            "message": "Models AI unactive or error",
        }
