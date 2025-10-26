# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.routes import prediction, model_info
from services.prediction_service import PredictionService
from utils.config import Settings
from utils.logging import setup_logging

# Initialize settings and logging
settings = Settings()
logger = setup_logging()

# Initialize services
prediction_service = PredictionService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load models
    logger.info("Loading ML models...")
    await prediction_service.load_all_models()
    yield
    # Shutdown: Cleanup
    logger.info("Shutting down...")

app = FastAPI(
    title="Endangered Species Prediction API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(prediction.router, prefix="/api/v1/predict", tags=["predictions"])
app.include_router(model_info.router, prefix="/api/v1/models", tags=["models"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)