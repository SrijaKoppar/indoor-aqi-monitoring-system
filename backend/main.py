from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import os

from schemas import (
    PredictionRequest,
    PredictionResponse,
    MetricsResponse,
    HistoricalDataResponse,
    HealthRecommendation
)
from model_loader import ModelLoader
from pm_simulator import pm_simulator

app = FastAPI(
    title="Air Quality Monitor API",
    description="FastAPI backend for real-time AQI predictions with PM simulation",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader = None

# ============================================================
# IN-MEMORY STORE — holds the latest reading from ESP8266
# Frontend polls /api/latest to get this
# ============================================================
latest_reading = {
    "co_concentration"          : 0.0,
    "co_concentration_next_hour": 0.0,
    "confidence"                : 0.89,
    "aqi_category"              : "Good",
    "predicted_category"        : "Good",
    "timestamp"                 : datetime.now().isoformat(),
    "model_used"                : "none",
    "feature_importance"        : [],
    "pm25"                      : 12.0,
    "pm10"                      : 18.0,
    "pm25_category"             : "Good",
    "pm10_category"             : "Good",
    "pm_simulated"              : True,
    "temperature"               : 25.0,
    "relative_humidity"         : 55.0,
    "has_data"                  : False
}

@app.on_event("startup")
async def startup_event():
    global model_loader
    try:
        model_loader = ModelLoader()
        print("✓ Models loaded successfully")
    except Exception as e:
        print(f"⚠ Warning: Models not loaded. Error: {e}")
        model_loader = None

@app.get("/health")
async def health_check():
    return {
        "status"       : "healthy",
        "timestamp"    : datetime.now().isoformat(),
        "models_loaded": model_loader is not None,
        "pm_simulator" : "active"
    }

@app.post("/api/predict")
async def predict(request: PredictionRequest):
    global latest_reading
    try:
        pm_data = pm_simulator.simulate(
            co_concentration  = request.co_gt,
            temperature       = request.temperature,
            relative_humidity = request.relative_humidity
        )

        if model_loader is None or not model_loader.models_available:
            result = {
                "co_concentration"          : request.co_gt,
                "co_concentration_next_hour": request.co_gt * 1.1,
                "confidence"                : 0.89,
                "aqi_category"              : _classify_aqi(request.co_gt),
                "predicted_category"        : _classify_aqi(request.co_gt * 1.1),
                "timestamp"                 : datetime.now().isoformat(),
                "model_used"                : "mock",
                "feature_importance"        : [],
                "pm25"                      : pm_data["pm25"],
                "pm10"                      : pm_data["pm10"],
                "pm25_category"             : pm_data["pm25_category"],
                "pm10_category"             : pm_data["pm10_category"],
                "pm_simulated"              : True,
                "temperature"               : request.temperature,
                "relative_humidity"         : request.relative_humidity,
                "has_data"                  : True
            }
        else:
            features = model_loader.prepare_features(
                co_gt             = request.co_gt,
                nox_gt            = request.nox_gt,
                no2_gt            = request.no2_gt,
                temperature       = request.temperature,
                relative_humidity = request.relative_humidity,
                pt08_s1_co        = request.pt08_s1_co,
                c6h6_gt           = request.c6h6_gt
            )
            co_prediction      = model_loader.predict_co(features)
            aqi_category       = model_loader.classify_aqi(request.co_gt)
            predicted_category = model_loader.classify_aqi(co_prediction)

            result = {
                "co_concentration"          : float(request.co_gt),
                "co_concentration_next_hour": float(co_prediction),
                "confidence"                : 0.89,
                "aqi_category"              : aqi_category,
                "predicted_category"        : predicted_category,
                "timestamp"                 : datetime.now().isoformat(),
                "model_used"                : "xgboost_regressor",
                "feature_importance"        : model_loader.get_feature_importance(),
                "pm25"                      : pm_data["pm25"],
                "pm10"                      : pm_data["pm10"],
                "pm25_category"             : pm_data["pm25_category"],
                "pm10_category"             : pm_data["pm10_category"],
                "pm_simulated"              : True,
                "temperature"               : request.temperature,
                "relative_humidity"         : request.relative_humidity,
                "has_data"                  : True
            }

        latest_reading = result
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/latest")
async def get_latest():
    """
    Returns the most recent sensor reading from ESP8266.
    Frontend polls this every 5 seconds for live updates.
    """
    return latest_reading


@app.get("/api/pm")
async def get_pm(co: float = 2.0, temperature: float = 25.0, humidity: float = 50.0):
    return pm_simulator.simulate(co, temperature, humidity)


@app.get("/api/metrics", response_model=MetricsResponse)
async def get_metrics():
    try:
        return MetricsResponse(
            model_name       = "XGBoost Regressor",
            accuracy         = model_loader.get_accuracy() if model_loader else 0.93,
            r2_score         = 0.89,
            mae              = 0.42,
            rmse             = 0.68,
            category_accuracy= 0.93,
            test_samples     = 200,
            training_samples = 800,
            features_used    = 22,
            last_updated     = datetime.now().isoformat(),
            model_status     = "loaded" if (model_loader and model_loader.models_available) else "mock"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/historical", response_model=HistoricalDataResponse)
async def get_historical_data(hours: int = 24):
    try:
        timestamps       = pd.date_range(end=datetime.now(), periods=hours, freq='H')
        actual_values    = np.random.uniform(1, 6, hours).tolist()
        predicted_values = np.clip(
            np.array(actual_values) + np.random.normal(0, 0.3, hours), 0, 10
        ).tolist()
        return HistoricalDataResponse(
            timestamps   = [ts.isoformat() for ts in timestamps],
            actual_co    = actual_values,
            predicted_co = predicted_values,
            hours        = hours
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recommendations")
async def get_health_recommendations(aqi_category: str):
    recommendations_map = {
        "Good"     : {"level": "Good",      "description": "Air quality is satisfactory",                       "recommendations": ["Safe for all activities", "Perfect for outdoor exercise"],                                              "at_risk_groups": []},
        "Moderate" : {"level": "Moderate",  "description": "Air quality is acceptable",                         "recommendations": ["Sensitive people should limit outdoor activity", "Ventilate indoor spaces"],                            "at_risk_groups": ["Asthma patients", "Elderly", "Children"]},
        "Unhealthy": {"level": "Unhealthy", "description": "General public may experience health effects",       "recommendations": ["Limit outdoor activities", "Keep windows closed", "Use HEPA air purifiers"],                            "at_risk_groups": ["Everyone", "Asthma patients", "Heart disease patients"]},
        "Hazardous": {"level": "Hazardous", "description": "Entire population is likely to be affected",        "recommendations": ["Avoid all outdoor activities", "Keep doors and windows closed", "Run air purifiers on high setting"],    "at_risk_groups": ["Everyone"]}
    }
    return recommendations_map.get(aqi_category, recommendations_map["Moderate"])


@app.get("/")
async def root():
    return {
        "name"     : "Air Quality Monitor API",
        "version"  : "1.1.0",
        "endpoints": {
            "health"         : "GET  /health",
            "predict"        : "POST /api/predict  ← ESP8266 posts here",
            "latest"         : "GET  /api/latest   ← Frontend polls here every 5s",
            "pm_only"        : "GET  /api/pm",
            "metrics"        : "GET  /api/metrics",
            "historical"     : "GET  /api/historical?hours=24",
            "recommendations": "GET  /api/recommendations?aqi_category=Moderate",
            "docs"           : "/docs"
        }
    }


def _classify_aqi(co: float) -> str:
    if co <= 2:    return "Good"
    elif co <= 5:  return "Moderate"
    elif co <= 10: return "Unhealthy"
    else:          return "Hazardous"



# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import numpy as np
# import pandas as pd
# from typing import Dict, List, Optional
# from datetime import datetime
# import os

# from schemas import (
#     PredictionRequest,
#     PredictionResponse,
#     MetricsResponse,
#     HistoricalDataResponse,
#     HealthRecommendation
# )
# from model_loader import ModelLoader
# from pm_simulator import pm_simulator          # ← PM simulator import

# app = FastAPI(
#     title="Air Quality Monitor API",
#     description="FastAPI backend for real-time AQI predictions with PM simulation",
#     version="1.1.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://localhost:3001", "https://*.vercel.app"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# model_loader = None

# @app.on_event("startup")
# async def startup_event():
#     global model_loader
#     try:
#         model_loader = ModelLoader()
#         print("✓ Models loaded successfully")
#     except Exception as e:
#         print(f"⚠ Warning: Models not loaded. Using mock predictions. Error: {e}")
#         model_loader = None

# # ============================================================
# # HEALTH CHECK
# # ============================================================
# @app.get("/health")
# async def health_check():
#     return {
#         "status"       : "healthy",
#         "timestamp"    : datetime.now().isoformat(),
#         "models_loaded": model_loader is not None,
#         "pm_simulator" : "active"        # lets frontend know PM is simulated
#     }

# # ============================================================
# # PREDICT — now includes PM simulation
# # ============================================================
# @app.post("/api/predict")
# async def predict(request: PredictionRequest):
#     """
#     Predict next-hour CO concentration and AQI category.
#     Also returns simulated PM2.5 / PM10 values (no physical sensor needed).

#     PM values are generated by pm_simulator.py, correlated with
#     CO concentration, temperature, and humidity from real sensors.
#     """
#     try:
#         # ── Run PM simulation using real sensor inputs ──────────
#         pm_data = pm_simulator.simulate(
#             co_concentration  = request.co_gt,
#             temperature       = request.temperature,
#             relative_humidity = request.relative_humidity
#         )

#         # ── ML prediction ────────────────────────────────────────
#         if model_loader is None or not model_loader.models_available:
#             return {
#                 "co_concentration"         : request.co_gt,
#                 "co_concentration_next_hour": request.co_gt * 1.1,
#                 "confidence"               : 0.89,
#                 "aqi_category"             : model_loader.classify_aqi(request.co_gt) if model_loader else "Moderate",
#                 "predicted_category"       : "Moderate",
#                 "timestamp"                : datetime.now().isoformat(),
#                 "model_used"               : "mock",
#                 "feature_importance"       : [],
#                 # PM data appended
#                 "pm25"                     : pm_data["pm25"],
#                 "pm10"                     : pm_data["pm10"],
#                 "pm25_category"            : pm_data["pm25_category"],
#                 "pm10_category"            : pm_data["pm10_category"],
#                 "pm_simulated"             : True
#             }

#         features = model_loader.prepare_features(
#             co_gt             = request.co_gt,
#             nox_gt            = request.nox_gt,
#             no2_gt            = request.no2_gt,
#             temperature       = request.temperature,
#             relative_humidity = request.relative_humidity,
#             pt08_s1_co        = request.pt08_s1_co,
#             c6h6_gt           = request.c6h6_gt
#         )

#         co_prediction    = model_loader.predict_co(features)
#         aqi_category     = model_loader.classify_aqi(request.co_gt)
#         predicted_category = model_loader.classify_aqi(co_prediction)

#         return {
#             "co_concentration"          : float(request.co_gt),
#             "co_concentration_next_hour": float(co_prediction),
#             "confidence"                : 0.89,
#             "aqi_category"              : aqi_category,
#             "predicted_category"        : predicted_category,
#             "timestamp"                 : datetime.now().isoformat(),
#             "model_used"                : "xgboost_regressor",
#             "feature_importance"        : model_loader.get_feature_importance(),
#             # PM data appended — simulated from real sensor inputs
#             "pm25"                      : pm_data["pm25"],
#             "pm10"                      : pm_data["pm10"],
#             "pm25_category"             : pm_data["pm25_category"],
#             "pm10_category"             : pm_data["pm10_category"],
#             "pm_simulated"              : True    # frontend can show "simulated" badge
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # ============================================================
# # PM ONLY — dedicated endpoint if frontend needs just PM
# # ============================================================
# @app.get("/api/pm")
# async def get_pm(
#     co: float = 2.0,
#     temperature: float = 25.0,
#     humidity: float = 50.0
# ):
#     """
#     Returns simulated PM2.5 / PM10 values.
#     Query params: co (mg/m³), temperature (°C), humidity (%)
#     Example: GET /api/pm?co=3.5&temperature=27&humidity=60
#     """
#     pm_data = pm_simulator.simulate(co, temperature, humidity)
#     return pm_data

# # ============================================================
# # METRICS, HISTORICAL, RECOMMENDATIONS — unchanged
# # ============================================================
# @app.get("/api/metrics", response_model=MetricsResponse)
# async def get_metrics():
#     try:
#         if model_loader is None or not model_loader.models_available:
#             return MetricsResponse(
#                 model_name       = "XGBoost Regressor",
#                 accuracy         = 0.93,
#                 r2_score         = 0.89,
#                 mae              = 0.42,
#                 rmse             = 0.68,
#                 category_accuracy= 0.93,
#                 test_samples     = 200,
#                 training_samples = 800,
#                 features_used    = 22,
#                 last_updated     = datetime.now().isoformat(),
#                 model_status     = "mock"
#             )
#         return MetricsResponse(
#             model_name       = "XGBoost Regressor",
#             accuracy         = model_loader.get_accuracy(),
#             r2_score         = 0.89,
#             mae              = 0.42,
#             rmse             = 0.68,
#             category_accuracy= 0.93,
#             test_samples     = 200,
#             training_samples = 800,
#             features_used    = 22,
#             last_updated     = datetime.now().isoformat(),
#             model_status     = "loaded"
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/api/historical", response_model=HistoricalDataResponse)
# async def get_historical_data(hours: int = 24):
#     try:
#         timestamps       = pd.date_range(end=datetime.now(), periods=hours, freq='H')
#         actual_values    = np.random.uniform(1, 6, hours).tolist()
#         predicted_values = np.clip(
#             np.array(actual_values) + np.random.normal(0, 0.3, hours), 0, 10
#         ).tolist()
#         return HistoricalDataResponse(
#             timestamps   = [ts.isoformat() for ts in timestamps],
#             actual_co    = actual_values,
#             predicted_co = predicted_values,
#             hours        = hours
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/api/recommendations")
# async def get_health_recommendations(aqi_category: str):
#     recommendations_map = {
#         "Good": {
#             "level"          : "Good",
#             "description"    : "Air quality is satisfactory",
#             "recommendations": [
#                 "Air quality is safe for outdoor activities",
#                 "Perfect time for outdoor exercise",
#                 "No restrictions on any activities"
#             ],
#             "at_risk_groups" : []
#         },
#         "Moderate": {
#             "level"          : "Moderate",
#             "description"    : "Air quality is acceptable",
#             "recommendations": [
#                 "Unusually sensitive people should limit prolonged outdoor activity",
#                 "Use air filters if sensitive",
#                 "Ventilate indoor spaces regularly"
#             ],
#             "at_risk_groups" : ["Asthma patients", "Elderly", "Children"]
#         },
#         "Unhealthy": {
#             "level"          : "Unhealthy",
#             "description"    : "General public may experience health effects",
#             "recommendations": [
#                 "Limit outdoor activities",
#                 "Keep windows closed",
#                 "Use air purifiers with HEPA filters",
#                 "Wear N95 masks if going outdoors"
#             ],
#             "at_risk_groups" : ["Everyone", "Asthma patients", "Heart disease patients", "Elderly", "Children"]
#         },
#         "Hazardous": {
#             "level"          : "Hazardous",
#             "description"    : "Entire population is likely to be affected",
#             "recommendations": [
#                 "Avoid all outdoor activities",
#                 "Keep windows and doors closed",
#                 "Run air purifiers on high setting",
#                 "Wear N95 or P100 masks outdoors"
#             ],
#             "at_risk_groups" : ["Everyone"]
#         }
#     }
#     return recommendations_map.get(aqi_category, recommendations_map["Moderate"])


# @app.get("/")
# async def root():
#     return {
#         "name"     : "Air Quality Monitor API",
#         "version"  : "1.1.0",
#         "endpoints": {
#             "health"         : "GET  /health",
#             "predict"        : "POST /api/predict",
#             "pm_only"        : "GET  /api/pm?co=3.5&temperature=27&humidity=60",
#             "metrics"        : "GET  /api/metrics",
#             "historical"     : "GET  /api/historical?hours=24",
#             "recommendations": "GET  /api/recommendations?aqi_category=Moderate",
#             "docs"           : "/docs"
#         }
#     }


# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import numpy as np
# import pandas as pd
# from typing import Dict, List, Optional
# from datetime import datetime
# import os
# import sys

# # Import Pydantic models
# from schemas import (
#     PredictionRequest,
#     PredictionResponse,
#     MetricsResponse,
#     HistoricalDataResponse,
#     HealthRecommendation
# )

# # Import model loaders
# from model_loader import ModelLoader

# app = FastAPI(
#     title="Air Quality Monitor API",
#     description="FastAPI backend for real-time air quality predictions with ML models",
#     version="1.0.0"
# )

# # Enable CORS for React frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://localhost:3001", "https://*.vercel.app"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Initialize model loader
# model_loader = None

# @app.on_event("startup")
# async def startup_event():
#     """Load ML models on startup"""
#     global model_loader
#     try:
#         model_loader = ModelLoader()
#         print("✓ Models loaded successfully")
#     except Exception as e:
#         print(f"⚠ Warning: Models not loaded. Using mock predictions. Error: {e}")
#         model_loader = None

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {
#         "status": "healthy",
#         "timestamp": datetime.now().isoformat(),
#         "models_loaded": model_loader is not None
#     }

# @app.post("/api/predict", response_model=PredictionResponse)
# async def predict(request: PredictionRequest):
#     """
#     Predict next-hour CO concentration and AQI category
    
#     Required sensor readings:
#     - co_gt: Carbon Monoxide (mg/m³)
#     - nox_gt: Nitrogen Oxides (µg/m³)
#     - no2_gt: Nitrogen Dioxide (µg/m³)
#     - temperature: Temperature (°C)
#     - relative_humidity: Relative Humidity (%)
#     - pt08_s1_co: PT08.S1 (CO) sensor value
#     - c6h6_gt: Benzene (µg/m³)
#     """
#     try:
#         if model_loader is None or not model_loader.models_available:
#             # Return mock prediction with realistic data
#             return PredictionResponse(
#                 co_concentration=3.5,
#                 co_concentration_next_hour=4.2,
#                 confidence=0.89,
#                 aqi_category="Moderate",
#                 predicted_category="Moderate",
#                 timestamp=datetime.now().isoformat(),
#                 model_used="mock",
#                 feature_importance=[
#                     {"feature": "CO(GT)_lag1", "importance": 0.23},
#                     {"feature": "hour", "importance": 0.14},
#                     {"feature": "CO(GT)_rollmean3", "importance": 0.09},
#                     {"feature": "NOx(GT)_lag1", "importance": 0.065},
#                 ]
#             )
        
#         # Prepare features for XGBoost model
#         features = model_loader.prepare_features(
#             co_gt=request.co_gt,
#             nox_gt=request.nox_gt,
#             no2_gt=request.no2_gt,
#             temperature=request.temperature,
#             relative_humidity=request.relative_humidity,
#             pt08_s1_co=request.pt08_s1_co,
#             c6h6_gt=request.c6h6_gt
#         )
        
#         # Get CO prediction from XGBoost regressor
#         co_prediction = model_loader.predict_co(features)
        
#         # Classify AQI category
#         aqi_category = model_loader.classify_aqi(request.co_gt)
#         predicted_category = model_loader.classify_aqi(co_prediction)
        
#         return PredictionResponse(
#             co_concentration=float(request.co_gt),
#             co_concentration_next_hour=float(co_prediction),
#             confidence=0.89,  # From your XGBoost model's R² score
#             aqi_category=aqi_category,
#             predicted_category=predicted_category,
#             timestamp=datetime.now().isoformat(),
#             model_used="xgboost_regressor",
#             feature_importance=model_loader.get_feature_importance()
#         )
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/metrics", response_model=MetricsResponse)
# async def get_metrics():
#     """
#     Get model performance metrics
#     """
#     try:
#         if model_loader is None or not model_loader.models_available:
#             # Return mock metrics
#             return MetricsResponse(
#                 model_name="XGBoost Regressor",
#                 accuracy=0.93,
#                 r2_score=0.89,
#                 mae=0.42,
#                 rmse=0.68,
#                 category_accuracy=0.93,
#                 test_samples=200,
#                 training_samples=800,
#                 features_used=22,
#                 last_updated=datetime.now().isoformat(),
#                 model_status="mock"
#             )
        
#         return MetricsResponse(
#             model_name="XGBoost Regressor",
#             accuracy=model_loader.get_accuracy(),
#             r2_score=0.89,
#             mae=0.42,
#             rmse=0.68,
#             category_accuracy=0.93,
#             test_samples=200,
#             training_samples=800,
#             features_used=22,
#             last_updated=datetime.now().isoformat(),
#             model_status="loaded"
#         )
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/historical", response_model=HistoricalDataResponse)
# async def get_historical_data(hours: int = 24):
#     """
#     Get historical predictions and actual values
#     Default: last 24 hours
#     """
#     try:
#         # Generate mock time series data
#         timestamps = pd.date_range(end=datetime.now(), periods=hours, freq='H')
#         actual_values = np.random.uniform(1, 6, hours).tolist()
#         predicted_values = np.array(actual_values) + np.random.normal(0, 0.3, hours)
#         predicted_values = np.clip(predicted_values, 0, 10).tolist()
        
#         return HistoricalDataResponse(
#             timestamps=[ts.isoformat() for ts in timestamps],
#             actual_co=actual_values,
#             predicted_co=predicted_values,
#             hours=hours
#         )
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/recommendations")
# async def get_health_recommendations(aqi_category: str):
#     """
#     Get health recommendations based on AQI category
#     """
#     recommendations_map = {
#         "Good": {
#             "level": "Good",
#             "description": "Air quality is satisfactory",
#             "recommendations": [
#                 "Air quality is safe for outdoor activities",
#                 "Perfect time for outdoor exercise",
#                 "No restrictions on any activities"
#             ],
#             "at_risk_groups": []
#         },
#         "Moderate": {
#             "level": "Moderate",
#             "description": "Air quality is acceptable",
#             "recommendations": [
#                 "Moderate air quality. Unusually sensitive people should consider limiting prolonged outdoor activities",
#                 "Use air filters if sensitive",
#                 "Ventilate indoor spaces regularly"
#             ],
#             "at_risk_groups": ["Asthma patients", "Elderly", "Children"]
#         },
#         "Unhealthy": {
#             "level": "Unhealthy",
#             "description": "Members of general public are beginning to experience health effects",
#             "recommendations": [
#                 "Active children and adults, and people with respiratory or heart disease should limit outdoor activities",
#                 "Keep windows closed to reduce indoor pollution",
#                 "Use air purifiers with HEPA filters",
#                 "Wear N95 masks if going outdoors",
#                 "Stay hydrated and rest more"
#             ],
#             "at_risk_groups": ["Everyone", "Asthma patients", "Heart disease patients", "Elderly", "Children"]
#         },
#         "Hazardous": {
#             "level": "Hazardous",
#             "description": "Entire population is more likely to be affected",
#             "recommendations": [
#                 "Avoid all outdoor activities",
#                 "Keep windows and doors closed",
#                 "Run air purifiers on high setting",
#                 "Wear N95 or P100 masks if going outdoors",
#                 "Stay in an air-conditioned room",
#                 "Monitor air quality regularly"
#             ],
#             "at_risk_groups": ["Everyone"]
#         }
#     }
    
#     return recommendations_map.get(aqi_category, recommendations_map["Moderate"])

# @app.get("/")
# async def root():
#     """Root endpoint with API documentation"""
#     return {
#         "name": "Air Quality Monitor API",
#         "version": "1.0.0",
#         "endpoints": {
#             "health": "GET /health",
#             "predict": "POST /api/predict",
#             "metrics": "GET /api/metrics",
#             "historical": "GET /api/historical?hours=24",
#             "recommendations": "GET /api/recommendations?aqi_category=Moderate",
#             "docs": "/docs"
#         }
#     }
