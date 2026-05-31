from fastapi import APIRouter, UploadFile, File
from web.backend.controllers.predict_control import predict_control

router = APIRouter(
        prefix="/api/predict",
        tags=["Prediction"]
    )

@router.post("/upload-csv")
async def upload_csv_file(file: UploadFile = File(...)):
    return await predict_control.handle_csv_file(file)
