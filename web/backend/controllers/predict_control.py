from fastapi import UploadFile, HTTPException
from web.backend.services.predict_services import predict_service

ALLOWED_EXTENSIONS = [".csv"]
MAX_FILE_SIZE = 30

MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE * 1024 * 1024

class PredictControl:
    async def handle_csv_file(self, file: UploadFile) -> dict:
        
        filename = file.filename
        if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            raise HTTPException(
                    status_code=400,
                    detail=f"File format not supported"
                )

        file_content = await file.read()
        file_size = len(file_content)

        if file_size > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                    status_code=413,
                    detail=f"Payload too large"
                )
        
        if file_size == 0:
            raise HTTPException(
                    status_code=400,
                    detail=f"File is empty data"
                )

        try:
           result = predict_service.process_and_predict(file_content)

           return {
                   "status": "success",
                   "message": "Analyzied",
                   "data": result,
                }
        except Exception as e:
           raise HTTPException(
                    status_code=500,
                    detail=f"System Error when processing data"
                )

predict_control = PredictControl()
