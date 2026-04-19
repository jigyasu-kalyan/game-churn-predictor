# core/models/predictor.py

import joblib
import pandas as pd
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class ChurnPredictor:
    def __init__(self, model_path: str = settings.MODEL_PATH):
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        try:
            logger.info(f"Loading churn model from {self.model_path}")
            return joblib.load(self.model_path)
        except FileNotFoundError:
            logger.warning(f"Churn model not found at {self.model_path}. Predictor will be inactive.")
            return None
        except Exception as e:
            logger.error(f"Error loading churn model: {e}")
            return None

    def predict(self, player_data: dict):
        if self.model is None:
            # Fallback values if model is missing
            return 0.5, 0 
            
        df = pd.DataFrame([player_data])
        try:
            prob = self.model.predict_proba(df)[0][1]
            predicted_class = self.model.predict(df)[0]
            return float(prob), int(predicted_class)
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return 0.5, 0
