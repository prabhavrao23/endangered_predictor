# api/routes/prediction.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
import numpy as np

from api.schemas.request import (
    SpeciesImageRequest,
    PopulationForecastRequest,
    RiskAssessmentRequest
)
from api.schemas.response import (
    SpeciesImageResponse,
    PopulationForecastResponse,
    RiskAssessmentResponse
)
from services.prediction_service import prediction_service

router = APIRouter()

@router.post("/species-recognition", response_model=SpeciesImageResponse)
async def recognize_species(file: UploadFile = File(...)):
    """Identify species from uploaded image"""
    try:
        image_data = await file.read()
        result = await prediction_service.recognize_species(image_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/population-forecast", response_model=PopulationForecastResponse)
async def forecast_population(request: PopulationForecastRequest):
    """Forecast population trends"""
    try:
        result = await prediction_service.forecast_population(
            species_id=request.species_id,
            historical_data=request.historical_data,
            forecast_horizon=request.forecast_horizon
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/risk-assessment", response_model=RiskAssessmentResponse)
async def assess_risk(request: RiskAssessmentRequest):
    """Comprehensive risk assessment"""
    try:
        result = await prediction_service.assess_risk(
            species_id=request.species_id,
            location=request.location,
            factors=request.factors
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))