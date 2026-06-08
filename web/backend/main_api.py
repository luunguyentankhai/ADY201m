from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
from web.backend.config.logs_config import logger
from web.backend.middleware.logging_middleware import AutoLoggingMiddleware
from web.backend.core.ml_manager import ml_manager
from web.backend.routes import health_router, upload_router, predict_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server FastAPI startup")

    ml_manager.load_assets()

    yield

    logger.info("Server shutdowning")
    ml_manager.models.clear()
    ml_manager.scaler = None

app = FastAPI(
        title="AI Fraud Detection API",
        description="Backend for research models fraud detecter",
        lifespan=lifespan
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
    )

app.add_middleware(AutoLoggingMiddleware)

app.include_router(health_router.router)
app.include_router(upload_router.router)
app.include_router(predict_routes.router)
