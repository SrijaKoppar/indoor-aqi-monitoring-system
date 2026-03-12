# Backend Integration Guide

This dashboard is built to work seamlessly with your Python ML models. Follow this guide to connect your XGBoost and AQI models to the frontend.

## Overview

Your ML models:
- **aqi_model.py**: Trains multiple models (Linear, Ridge, Lasso) for CO prediction
- **aqi_xgboost_model.py**: XGBoost regressor for next-hour CO prediction with 0.89 R² score

The frontend dashboard expects:
1. Real-time sensor data (CO, CO₂, temperature, humidity, PM2.5, PM10)
2. Predictions from your XGBoost model
3. Model performance metrics (MAE, RMSE, R², Category Accuracy)

## API Endpoints to Implement

### 1. POST /api/predict
**Purpose**: Get next-hour CO prediction

**Frontend Code** (replace in `/app/api/predict/route.ts`):
```typescript
const response = await fetch('http://your-backend:PORT/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    co: sensorData.co,
    co2: sensorData.co2,
    temperature: sensorData.temperature,
    humidity: sensorData.humidity,
    pm25: sensorData.pm25,
    pm10: sensorData.pm10,
  })
});
```

**Backend Response Expected**:
```json
{
  "nextHourCO": 2.8,
  "confidence": 0.92,
  "category": "Moderate",
  "categoryConfidence": 0.89
}
```

### 2. GET /api/metrics
**Purpose**: Get model performance metrics

**Frontend Code** (replace in `/app/api/metrics/route.ts`):
```typescript
const response = await fetch('http://your-backend:PORT/metrics', {
  method: 'GET'
});
```

**Backend Response Expected**:
```json
{
  "mae": 0.34,
  "rmse": 0.52,
  "r2": 0.89,
  "categoryAccuracy": 0.93
}
```

### 3. GET /api/historical
**Purpose**: Get 200+ hours of historical predictions vs actuals

**Frontend Code** (add to dashboard):
```typescript
const response = await fetch('http://your-backend:PORT/historical?hours=200', {
  method: 'GET'
});
```

**Backend Response Expected**:
```json
[
  {
    "timestamp": "2024-03-12T10:00:00Z",
    "actual": 2.5,
    "predicted": 2.6
  },
  ...
]
```

### 4. GET /api/features
**Purpose**: Get feature importance rankings from XGBoost model

**Frontend Code** (add to dashboard):
```typescript
const response = await fetch('http://your-backend:PORT/features', {
  method: 'GET'
});
```

**Backend Response Expected**:
```json
[
  { "feature": "CO(GT)_lag1", "importance": 0.23 },
  { "feature": "hour", "importance": 0.14 },
  { "feature": "CO(GT)_rollmean3", "importance": 0.09 },
  ...
]
```

## Python Backend Setup Example

Here's a template using Flask to expose your models:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Load your trained models
xgb_model = joblib.load('your_xgb_model.pkl')

# AQI category mapping
CO_THRESHOLDS = {
    'Good': 2.0,
    'Moderate': 4.0,
    'Unhealthy': 6.0,
    'Hazardous': 10.0
}

def get_aqi_category(co_value):
    for category, threshold in CO_THRESHOLDS.items():
        if co_value <= threshold:
            return category
    return 'Hazardous'

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Prepare features for your model
        features = np.array([[
            data['co'],
            data['temperature'],
            data['humidity'],
            data['co2'],
            data['pm25'],
            data['pm10'],
            # Add any lag features you need
        ]])
        
        # Get prediction
        prediction = xgb_model.predict(features)[0]
        category = get_aqi_category(prediction)
        
        return jsonify({
            'nextHourCO': float(prediction),
            'confidence': 0.92,  # Calculate based on model uncertainty
            'category': category,
            'categoryConfidence': 0.89
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/metrics', methods=['GET'])
def metrics():
    # Return your model's metrics from evaluation
    return jsonify({
        'mae': 0.34,
        'rmse': 0.52,
        'r2': 0.89,
        'categoryAccuracy': 0.93
    })

@app.route('/historical', methods=['GET'])
def historical():
    hours = request.args.get('hours', 200, type=int)
    
    # Return your historical predictions vs actuals
    # This could come from a database or log file
    data = []
    for i in range(hours):
        timestamp = datetime.now() - timedelta(hours=i)
        data.append({
            'timestamp': timestamp.isoformat(),
            'actual': 2.5 + (i % 5) * 0.5,
            'predicted': 2.4 + (i % 5) * 0.5
        })
    
    return jsonify(data)

@app.route('/features', methods=['GET'])
def features():
    # Get feature importance from your XGBoost model
    importances = xgb_model.feature_importances_
    feature_names = ['CO(GT)_lag1', 'hour', 'CO(GT)_rollmean3', ...]
    
    feature_list = [
        {'feature': name, 'importance': float(imp)}
        for name, imp in zip(feature_names, importances)
    ]
    
    return jsonify(sorted(feature_list, key=lambda x: x['importance'], reverse=True))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Environment Variables

Add to your `.env.local` file:

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
```

Then use in API routes:

```typescript
const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
```

## Dashboard Components Using Backend Data

The dashboard has the following components ready to display your data:

1. **StatusCard**: Current sensor readings
2. **PredictionCard**: Next-hour CO forecast with confidence
3. **MetricsCard**: Model performance metrics
4. **COTimeSeriesChart**: 50-hour historical comparison
5. **ScatterPlotChart**: Actual vs predicted validation
6. **FeatureImportanceChart**: Top 10 most important features
7. **CategoryDistributionChart**: AQI category accuracy
8. **Recommendations**: Health guidance based on current AQI

## Testing Without Backend

The dashboard uses mock data by default from `/lib/mock-data.ts`. This allows you to:

1. Develop the frontend independently
2. Test the UI layout and interactions
3. Prepare API integration when backend is ready

To use real backend data, update the API routes in:
- `/app/api/predict/route.ts`
- `/app/api/metrics/route.ts`
- And add new routes as needed

## Deployment

When deploying to production:

1. Update backend URL to your production server
2. Ensure CORS headers are properly configured
3. Add authentication if needed
4. Set appropriate rate limits on API endpoints

For more details on your models, refer to the uploaded Python files:
- `aqi_model.py` - Multiple model implementations
- `aqi_xgboost_model.py` - XGBoost regressor details
