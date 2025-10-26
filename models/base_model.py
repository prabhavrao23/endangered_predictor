# models/base_model.py
from abc import ABC, abstractmethod
from typing import Any, Dict
import numpy as np

class BaseModel(ABC):
    """Abstract base class for all ML models"""
    
    def __init__(self, model_name: str, version: str):
        self.model_name = model_name
        self.version = version
        self.model = None
        
    @abstractmethod
    def load(self, model_path: str):
        """Load model from disk"""
        pass
    
    @abstractmethod
    def predict(self, input_data: Any) -> Dict:
        """Make predictions"""
        pass
    
    @abstractmethod
    def preprocess(self, raw_data: Any) -> Any:
        """Preprocess input data"""
        pass
    
    def get_metadata(self) -> Dict:
        """Return model metadata"""
        return {
            "name": self.model_name,
            "version": self.version,
            "status": "loaded" if self.model else "unloaded"
        }