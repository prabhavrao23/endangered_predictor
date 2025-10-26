# services/prediction_service.py
import asyncio
from typing import Dict, List
import logging

from models.image_recognition.cnn_model import SpeciesRecognitionModel
from models.time_series.population_forecast import PopulationForecastModel
from models.risk_assessment.multi_factor import RiskAssessmentModel

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        self.models = {}
        
    async def load_all_models(self):
        """Load all models during startup"""
        try:
            self.models['species_recognition'] = SpeciesRecognitionModel()
            await self.models['species_recognition'].load('models/weights/species_cnn_v1.pth')
            
            self.models['population_forecast'] = PopulationForecastModel()
            await self.models['population_forecast'].load('models/weights/timeseries_v1.pkl')
            
            self.models['risk_assessment'] = RiskAssessmentModel()
            await self.models['risk_assessment'].load('models/weights/risk_v1.pkl')
            
            logger.info("All models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    async def recognize_species(self, image_data: bytes) -> Dict:
        """Species recognition from image"""
        model = self.models.get('species_recognition')
        if not model:
            raise ValueError("Species recognition model not loaded")
        
        return await model.predict(image_data)
    
    async def forecast_population(self, species_id: str, historical_data: List[Dict], 
                                 forecast_horizon: int) -> Dict:
        """Forecast population trends"""
        model = self.models.get('population_forecast')
        if not model:
            raise ValueError("Population forecast model not loaded")
        
        return await model.predict(species_id, historical_data, forecast_horizon)
    
    async def assess_risk(self, species_id: str, location: Dict, 
                         factors: Optional[List[str]] = None) -> Dict:
        """Multi-factor risk assessment - orchestrates multiple models"""
        
        # This would call multiple models and aggregate results
        risk_model = self.models.get('risk_assessment')
        
        # Parallel execution of sub-models
        tasks = [
            self._get_habitat_risk(location),
            self._get_climate_risk(location, species_id),
            self._get_poaching_risk(location)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Combine results
        return await risk_model.aggregate_risks(species_id, results)
    
    async def _get_habitat_risk(self, location: Dict) -> Dict:
        # Call habitat loss model
        pass
    
    async def _get_climate_risk(self, location: Dict, species_id: str) -> Dict:
        # Call climate impact model
        pass
    
    async def _get_poaching_risk(self, location: Dict) -> Dict:
        # Call poaching threat model
        pass

# Global instance
prediction_service = PredictionService()