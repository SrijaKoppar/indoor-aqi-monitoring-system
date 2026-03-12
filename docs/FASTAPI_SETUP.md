# FastAPI Backend Setup Guide

Your Air Quality Monitor now uses **FastAPI** for the backend, fully integrated with your ML models.

## Project Structure

```
project-root/
├── frontend/                 # React/Next.js frontend
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── .env.local
│   └── package.json
│
└── backend/                  # FastAPI backend
    ├── main.py              # FastAPI application
    ├── schemas.py           # Pydantic request/response models
    ├── model_loader.py      # ML model loading & inference
    ├── models/
    │   ├── aqi_classifier.py
    │   ├── co_regressor.py
    │   └── models_pickle/   # Pre-trained model files
    ├── requirements.txt     # Python dependencies
    └── __init__.py
```

## Backend Setup

### 1. Create Python Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare ML Models

Your backend includes two ML models:

- **XGBoost Regressor** (`co_regressor.py`): Predicts next-hour CO concentration
- **Random Forest Classifier** (`aqi_classifier.py`): Classifies AQI categories

To use pre-trained models:

```bash
# 1. Train and save models (run your training scripts)
python models/co_regressor.py      # Generates xgb_model.pkl
python models/aqi_classifier.py    # Generates rf_model.pkl

# 2. Move .pkl files to models_pickle directory
mkdir models_pickle
mv xgb_model.pkl models_pickle/
mv rf_model.pkl models_pickle/
mv label_encoder.pkl models_pickle/
```

The backend will:
- ✅ Automatically load models if they exist
- ⚠️ Use mock predictions if models aren't found (perfect for development)

### 4. Run the FastAPI Server

```bash
# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# For production
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

### 5. Access API Documentation

Open your browser to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Frontend Setup

### 1. Install Dependencies

```bash
cd ..  # Go back to project root
pnpm install
```

### 2. Configure API URL

Create `.env.local` in the root directory:

```env
# For local development with FastAPI backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# For production (change to your deployed FastAPI URL)
# NEXT_PUBLIC_API_URL=https://api.yourapp.com
```

### 3. Run the Frontend

```bash
pnpm dev
```

Frontend will be available at: **http://localhost:3000**

## API Endpoints

### Predictions

**POST** `/api/predict`

Request body:
```json
{
  "co_gt": 2.5,
  "nox_gt": 120,
  "no2_gt": 90,
  "temperature": 22,
  "relative_humidity": 45,
  "pt08_s1_co": 1200,
  "c6h6_gt": 2.5
}
```

Response:
```json
{
  "co_concentration": 2.5,
  "co_concentration_next_hour": 3.5,
  "confidence": 0.89,
  "aqi_category": "Moderate",
  "predicted_category": "Moderate",
  "timestamp": "2024-01-01T12:00:00",
  "model_used": "xgboost_regressor",
  "feature_importance": [...]
}
```

### Metrics

**GET** `/api/metrics`

Returns model performance metrics.

### Historical Data

**GET** `/api/historical?hours=24`

Returns time series of actual vs predicted CO values.

### Recommendations

**GET** `/api/recommendations?aqi_category=Moderate`

Returns health recommendations based on AQI category.

## Running Both Frontend and Backend

**Option 1: Separate Terminals**

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

Terminal 2 (Frontend):
```bash
pnpm dev
```

**Option 2: Using a Process Manager**

Install `concurrently`:
```bash
pnpm add -D concurrently
```

Add to `package.json`:
```json
{
  "scripts": {
    "dev": "concurrently \"cd backend && source venv/bin/activate && uvicorn main:app --reload\" \"pnpm next dev\""
  }
}
```

## Environment Variables

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env in backend directory)

Optional environment variables:

```env
# CORS settings
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Model paths
MODEL_DIR=./models_pickle

# Logging
LOG_LEVEL=INFO
```

## Troubleshooting

### Backend not connecting

1. Check if backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check CORS is enabled (it should be in main.py)

3. Verify `.env.local` has correct API_URL

### Models not loading

1. Ensure pickle files exist in `backend/models_pickle/`
2. Check model file names match exactly:
   - `xgb_model.pkl`
   - `rf_model.pkl`
   - `label_encoder.pkl`

3. Verify pickle files are compatible with xgboost version:
   ```bash
   pip list | grep xgboost
   ```

### Port already in use

Change port in command:
```bash
uvicorn main:app --reload --port 8001
# Then update NEXT_PUBLIC_API_URL=http://localhost:8001
```

## Production Deployment

### Deploy FastAPI Backend

**Option 1: Railway**

```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
railway up
```

**Option 2: Render**

1. Create account at render.com
2. Connect GitHub repo
3. Create new "Web Service"
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port 8000`

**Option 3: AWS/Azure/GCP**

See DEPLOYMENT_CHECKLIST.md for detailed instructions.

### Deploy React Frontend

Frontend deploys to Vercel automatically. Just update:

```env
NEXT_PUBLIC_API_URL=https://your-fastapi-backend.com
```

## Model Integration Details

### XGBoost Regressor

- **Input**: 22 features (current readings + lags + rolling means)
- **Output**: Next-hour CO concentration
- **Accuracy**: R² = 0.89, MAE = 0.42 mg/m³

Feature importance (top 5):
1. CO(GT)_lag1 (23%)
2. hour (14%)
3. CO(GT)_rollmean3 (9%)
4. NOx(GT)_lag1 (6.5%)
5. NOx(GT)_lag3 (3.5%)

### Random Forest Classifier

- **Input**: 6 sensor features
- **Output**: AQI category (Good/Moderate/Unhealthy/Hazardous)
- **Accuracy**: 93%

Categories:
- Good: CO ≤ 2 mg/m³
- Moderate: 2 < CO ≤ 5 mg/m³
- Unhealthy: 5 < CO ≤ 10 mg/m³
- Hazardous: CO > 10 mg/m³

## Next Steps

1. ✅ Start backend: `uvicorn main:app --reload`
2. ✅ Start frontend: `pnpm dev`
3. ✅ Open http://localhost:3000
4. ✅ Check /docs for API documentation
5. 📊 Integrate your sensor data sources
6. 🚀 Deploy to production

For issues, check the logs in both frontend and backend terminals.
