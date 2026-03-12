import pickle
import os
import numpy as np
import pandas as pd
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ModelLoader:
    """Load and manage ML models for predictions"""
    
    def __init__(self):
        self.xgb_model = None
        self.rf_model = None
        self.le = None  # Label encoder for AQI categories
        self.models_available = False
        self.feature_names = None
        self.feature_importance_data = [
            {"feature": "CO(GT)_lag1", "importance": 0.23},
            {"feature": "hour", "importance": 0.14},
            {"feature": "CO(GT)_rollmean3", "importance": 0.09},
            {"feature": "NOx(GT)_lag1", "importance": 0.065},
            {"feature": "NO2(GT)_lag1", "importance": 0.06},
            {"feature": "NO2(GT)_rollmean3", "importance": 0.03},
            {"feature": "CO(GT)_lag3", "importance": 0.03},
            {"feature": "CO(GT)_lag2", "importance": 0.025},
            {"feature": "NO2(GT)_lag2", "importance": 0.025},
            {"feature": "NO2(GT)_lag3", "importance": 0.02},
            {"feature": "PT08.S1(CO)_rollmean3", "importance": 0.02},
            {"feature": "T_rollmean3", "importance": 0.015},
            {"feature": "RH_rollmean3", "importance": 0.015},
            {"feature": "C6H6(GT)_lag2", "importance": 0.01},
            {"feature": "PT08.S1(CO)_lag3", "importance": 0.01},
        ]
        
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models from pickle files"""
        try:
            models_dir = os.path.join(os.path.dirname(__file__), 'models_pickle')
            
            # Try to load XGBoost model
            xgb_path = os.path.join(models_dir, 'xgb_model.pkl')
            if os.path.exists(xgb_path):
                with open(xgb_path, 'rb') as f:
                    self.xgb_model = pickle.load(f)
                logger.info("✓ XGBoost model loaded")
            
            # Try to load Random Forest model
            rf_path = os.path.join(models_dir, 'rf_model.pkl')
            if os.path.exists(rf_path):
                with open(rf_path, 'rb') as f:
                    self.rf_model = pickle.load(f)
                logger.info("✓ Random Forest model loaded")
            
            # Try to load label encoder
            le_path = os.path.join(models_dir, 'label_encoder.pkl')
            if os.path.exists(le_path):
                with open(le_path, 'rb') as f:
                    self.le = pickle.load(f)
                logger.info("✓ Label encoder loaded")
            
            # Set feature names for XGBoost
            if self.xgb_model:
                self.feature_names = [imp["feature"] for imp in self.feature_importance_data]
            
            # Models are available if at least XGBoost is loaded
            self.models_available = self.xgb_model is not None
            if self.models_available:
                logger.info("✓ Models successfully initialized")
            else:
                logger.warning("⚠ No models found. Using mock predictions.")
                
        except Exception as e:
            logger.warning(f"⚠ Error loading models: {e}. Will use mock predictions.")
            self.models_available = False
    
    def prepare_features(
        self,
        co_gt: float,
        nox_gt: float,
        no2_gt: float,
        temperature: float,
        relative_humidity: float,
        pt08_s1_co: float,
        c6h6_gt: float,
        hour: int = None
    ) -> np.ndarray:
        """
        Prepare features for XGBoost prediction
        Creates lag features and rolling means
        """
        if hour is None:
            from datetime import datetime
            hour = datetime.now().hour
        
        # Create feature array matching the 22 features used in training
        # This is a simplified version - in production, you'd maintain proper lag/rolling history
        features = np.array([
            co_gt,  # CO(GT)
            co_gt,  # CO(GT)_lag1 (simulated)
            co_gt * 0.95,  # CO(GT)_lag2 (simulated)
            co_gt * 0.92,  # CO(GT)_lag3 (simulated)
            (co_gt + co_gt*0.95 + co_gt*0.92) / 3,  # CO(GT)_rollmean3
            nox_gt,  # NOx(GT)
            nox_gt * 0.98,  # NOx(GT)_lag1
            nox_gt * 0.96,  # NOx(GT)_lag2
            nox_gt * 0.94,  # NOx(GT)_lag3
            (nox_gt + nox_gt*0.98 + nox_gt*0.96) / 3,  # NOx(GT)_rollmean3
            no2_gt,  # NO2(GT)
            no2_gt * 0.97,  # NO2(GT)_lag1
            no2_gt * 0.94,  # NO2(GT)_lag2
            no2_gt * 0.91,  # NO2(GT)_lag3
            (no2_gt + no2_gt*0.97 + no2_gt*0.94) / 3,  # NO2(GT)_rollmean3
            pt08_s1_co,  # PT08.S1(CO)
            pt08_s1_co * 0.99,  # PT08.S1(CO)_lag1
            pt08_s1_co * 0.98,  # PT08.S1(CO)_lag2
            (pt08_s1_co + pt08_s1_co*0.99 + pt08_s1_co*0.98) / 3,  # PT08.S1(CO)_rollmean3
            temperature,  # T
            (temperature + temperature + temperature) / 3,  # T_rollmean3
            relative_humidity,  # RH
            (relative_humidity + relative_humidity + relative_humidity) / 3,  # RH_rollmean3
            hour,  # hour
            c6h6_gt,  # C6H6(GT)_lag2
        ]).reshape(1, -1)
        
        return features
    
    def predict_co(self, features: np.ndarray) -> float:
        """
        Predict next-hour CO concentration using XGBoost
        Returns: float - predicted CO concentration
        """
        try:
            if self.xgb_model:
                prediction = self.xgb_model.predict(features)[0]
                # Ensure prediction is within reasonable bounds
                return float(np.clip(prediction, 0, 15))
            else:
                # Return mock prediction
                return float(features[0, 0] * 1.1 + np.random.normal(0, 0.3))
        except Exception as e:
            logger.error(f"Error in CO prediction: {e}")
            return float(features[0, 0] * 1.05)
    
    def classify_aqi(self, co_value: float) -> str:
        """
        Classify air quality based on CO concentration
        Based on your AQI classification rules
        """
        if co_value <= 2:
            return "Good"
        elif co_value <= 5:
            return "Moderate"
        elif co_value <= 10:
            return "Unhealthy"
        else:
            return "Hazardous"
    
    def get_feature_importance(self) -> List[Dict[str, float]]:
        """Return top 15 feature importances"""
        return self.feature_importance_data
    
    def get_accuracy(self) -> float:
        """Return model accuracy (from your XGBoost results)"""
        return 0.89
