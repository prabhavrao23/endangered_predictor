# api/schemas/request.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class PopulationForecastRequest(BaseModel):
    species_id: str = Field(..., description="Unique species identifier")
    historical_data: List[Dict[str, float]] = Field(
        ..., 
        description="Historical population data with timestamps"
    )
    forecast_horizon: int = Field(
        default=5, 
        ge=1, 
        le=50, 
        description="Years to forecast"
    )
    confidence_level: float = Field(default=0.95, ge=0.5, le=0.99)
    
class RiskAssessmentRequest(BaseModel):
    species_id: str
    location: Dict[str, float]  # {"lat": x, "lon": y}
    factors: Optional[List[str]] = None  # Specific factors to assess

# api/schemas/response.py
class SpeciesImageResponse(BaseModel):
    species_id: str
    species_name: str
    confidence: float
    top_predictions: List[Dict[str, float]]
    processing_time_ms: float

class PopulationForecastResponse(BaseModel):
    species_id: str
    forecast: List[Dict[str, float]]  # [{"year": 2025, "population": 1000, "lower": 800, "upper": 1200}]
    trend: str  # "increasing", "decreasing", "stable"
    confidence_intervals: Dict[str, List[float]]
    model_version: str