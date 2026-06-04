import uvicorn
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from web.backend.config.logs_config import logger

def start_server():
    logger.info("WEB START")
    logger.info(f"{'='*50}")
    logger.info("Server Address : http://127.0.0.1:8000")
    logger.info("Swagger UI     : http://127.0.0.1:8000/docs")
    logger.info("Upload API     : POST http://127.0.0.1:8000/api/predict/upload-csv")
    logger.info(f"{'='*50}")
    logger.info("Waiting for Uvicorn ASGI server to start")

    uvicorn.run(
            "web.backend.main_api:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
            )

if __name__ == "__main__":
    start_server()

