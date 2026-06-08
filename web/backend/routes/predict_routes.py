from logging.config import valid_ident
from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError

from web.backend.config.logs_config import logger
from web.backend.services.predict_services import predict_service
from web.backend.models.transaction_schema import TransactionInput

router = APIRouter(
    prefix="/api/predict",
    tags=["Prediction"]
)

@router.post("/single")
async def predict_single_api(transaction: TransactionInput):
    try:
        logger.info(f"API Request: Single Prediction for {transaction.nameOrig}")

        result = predict_service.predict_single(transaction)

        return {
                "status": "success",
                "data": result
                }

    except ValueError as ve:
        logger.error(f"Validation/Logic Error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logger.error(f"Internal Server Error in Single Prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Lỗi máy chủ nội bộ. Vui lòng kiểm tra log.")
