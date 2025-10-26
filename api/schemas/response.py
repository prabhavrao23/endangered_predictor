class SpeciesImageResponse(BaseModel):
    species_id: str
    species_name: str
    confidence: float
    top_predictions: List[Dict[str, float]]
    processing_time_ms: float