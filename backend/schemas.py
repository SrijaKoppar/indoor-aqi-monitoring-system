from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class PredictionRequest(BaseModel):
    """Request schema for CO prediction"""
    co_gt: float = Field(..., description="Current CO concentration (mg/m³)")
    nox_gt: float = Field(..., description="Nitrogen Oxides (µg/m³)")
    no2_gt: float = Field(..., description="Nitrogen Dioxide (µg/m³)")
    temperature: float = Field(..., description="Temperature (°C)")
    relative_humidity: float = Field(..., description="Relative Humidity (%)")
    pt08_s1_co: float = Field(..., description="PT08.S1 (CO) sensor value")
    c6h6_gt: float = Field(..., description="Benzene concentration (µg/m³)")

class FeatureImportance(BaseModel):
    """Feature importance in model"""
    feature: str
    importance: float

class PredictionResponse(BaseModel):
    """Response schema for predictions"""
    co_concentration: float = Field(..., description="Current CO concentration")
    co_concentration_next_hour: float = Field(..., description="Predicted CO for next hour")
    confidence: float = Field(..., description="Model confidence (0-1)")
    aqi_category: str = Field(..., description="Current AQI category")
    predicted_category: str = Field(..., description="Predicted AQI category")
    timestamp: str
    model_used: str
    feature_importance: List[FeatureImportance]

class MetricsResponse(BaseModel):
    """Model performance metrics"""
    model_name: str
    accuracy: float
    r2_score: float
    mae: float
    rmse: float
    category_accuracy: float
    test_samples: int
    training_samples: int
    features_used: int
    last_updated: str
    model_status: str

class HistoricalDataResponse(BaseModel):
    """Historical predictions and actuals"""
    timestamps: List[str]
    actual_co: List[float]
    predicted_co: List[float]
    hours: int

class HealthRecommendation(BaseModel):
    """Health recommendations"""
    level: str
    description: str
    recommendations: List[str]
    at_risk_groups: List[str]
