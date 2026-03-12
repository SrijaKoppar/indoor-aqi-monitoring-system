# Air Quality Monitor - React + FastAPI

A modern, full-stack air quality monitoring dashboard with real-time environmental data visualization and XGBoost ML predictions.

**Tech Stack:**
- **Frontend**: React (Next.js 15) + Tailwind CSS + Recharts
- **Backend**: FastAPI (Python) with integrated XGBoost & Random Forest models
- **ML Models**: CO concentration regression + AQI classification
- **Database**: Optional (easily add PostgreSQL/MongoDB)

## 🎯 Features

### Real-time Monitoring
- 📊 Live sensor data visualization (CO, CO₂, temperature, humidity, PM2.5, PM10)
- 🎯 Air quality status with color-coded indicators
- 📈 Interactive charts and time series analysis

### AI-Powered Predictions
- 🤖 XGBoost regressor for next-hour CO forecasting (R² = 0.89)
- 📋 Random Forest classifier for AQI categorization (93% accuracy)
- 🔍 Feature importance analysis (top 15 features)
- 📊 Actual vs predicted comparison charts

### Health & Safety
- 💡 Personalized health recommendations based on AQI
- ⚠️ At-risk group alerts
- 📱 Responsive mobile-first design
- 🌙 Dark theme optimized for 24/7 monitoring

## 📁 Project Structure

```
air-quality-monitor/
├── frontend/                      # React/Next.js application
│   ├── app/
│   │   ├── page.tsx              # Main dashboard
│   │   ├── layout.tsx            # Root layout
│   │   └── globals.css           # Global styles
│   ├── components/
│   │   └── dashboard/            # Dashboard components
│   │       ├── status-card.tsx
│   │       ├── prediction-card.tsx
│   │       ├── co-timeseries-chart.tsx
│   │       ├── feature-importance-chart.tsx
│   │       └── ...
│   ├── lib/
│   │   ├── api-client.ts         # FastAPI client
│   │   ├── types.ts              # TypeScript types
│   │   └── mock-data.ts          # Fallback mock data
│   ├── .env.local                # Environment variables
│   └── package.json
│
└── backend/                       # FastAPI application
    ├── main.py                   # FastAPI app
    ├── schemas.py                # Pydantic models
    ├── model_loader.py           # ML model management
    ├── train_models.py           # Model training script
    ├── models/
    │   ├── aqi_classifier.py     # AQI classification code
    │   ├── co_regressor.py       # CO regression code
    │   └── models_pickle/        # Trained model files
    ├── requirements.txt
    └── .env                      # Backend config
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.9+ (for backend)
- pip or poetry (Python package manager)

### Option 1: Running Both Locally (Recommended for Development)

#### 1️⃣ Frontend Setup

```bash
# Install dependencies
pnpm install

# Create .env.local
cp .env.local.example .env.local

# Start development server
pnpm dev
```

Frontend runs at: **http://localhost:3000**

#### 2️⃣ Backend Setup (in another terminal)

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Optional: Train models with your data
python train_models.py --data path/to/AirQualityUCI.csv

# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend API runs at: **http://localhost:8000**
API Docs at: **http://localhost:8000/docs**

### Option 2: Using Only Frontend (with Mock Data)

If you don't have FastAPI running, the frontend will automatically:
- ✅ Detect missing backend
- ✅ Fall back to mock data
- ✅ Display realistic demo predictions

```bash
pnpm dev
```

The app works perfectly with mock data for development/demos!

## 🔧 Configuration

### Frontend Environment Variables

Create `.env.local`:

```env
# FastAPI backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# For production:
# NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Backend Environment Variables

Create `backend/.env`:

```env
LOG_LEVEL=INFO
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
MODEL_DIR=./models_pickle
```

## 🤖 ML Models

### 1. XGBoost Regressor (CO Prediction)

**Task**: Predict CO concentration 1 hour ahead
**Performance**:
- R² Score: 0.89
- MAE: 0.42 mg/m³
- RMSE: 0.68 mg/m³

**Top Features**:
1. CO(GT)_lag1 (23%)
2. hour (14%)
3. CO(GT)_rollmean3 (9%)
4. NOx(GT)_lag1 (6.5%)
5. NOx(GT)_lag3 (3.5%)

### 2. Random Forest Classifier (AQI Categories)

**Task**: Classify air quality into 4 categories
**Performance**: 93% accuracy

**Categories**:
- 🟢 Good: CO ≤ 2 mg/m³
- 🟡 Moderate: 2 < CO ≤ 5 mg/m³
- 🟠 Unhealthy: 5 < CO ≤ 10 mg/m³
- 🔴 Hazardous: CO > 10 mg/m³

## 📊 API Endpoints

### Health Check
```bash
GET /health
```

### Get Predictions
```bash
POST /api/predict
Content-Type: application/json

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

### Get Model Metrics
```bash
GET /api/metrics
```

### Get Historical Data
```bash
GET /api/historical?hours=24
```

### Get Health Recommendations
```bash
GET /api/recommendations?aqi_category=Moderate
```

Full API documentation available at: **http://localhost:8000/docs**

## 🎨 Dashboard Components

### Status Cards
- Display current sensor readings
- Color-coded health indicators
- Real-time updates

### Prediction Card
- Next-hour CO forecast
- Confidence score
- Predicted AQI category

### Charts
- **Time Series**: Actual vs predicted CO over time
- **Scatter Plot**: Validation visualization
- **Feature Importance**: Top 15 features by importance
- **Category Distribution**: Actual vs predicted distribution

### Recommendations
- Personalized health guidance
- Activity recommendations
- At-risk group alerts

## 🔌 Integration Points

### Adding Real Sensor Data

Update the prediction request in `app/page.tsx`:

```typescript
const sensorReadings = {
  co_gt: realSensorData.co,         // From your IoT device
  nox_gt: realSensorData.nox,
  no2_gt: realSensorData.no2,
  temperature: realSensorData.temp,
  relative_humidity: realSensorData.humidity,
  pt08_s1_co: realSensorData.pt08,
  c6h6_gt: realSensorData.benzene,
};

const prediction = await apiClient.predict(sensorReadings);
```

### Adding Database

The FastAPI backend can easily integrate with:
- ✅ PostgreSQL (with SQLAlchemy)
- ✅ MongoDB (with PyMongo)
- ✅ Firebase (with Python SDK)

Example setup would be minimal - just add a database layer to `model_loader.py`.

## 📈 Training Custom Models

Use the provided training script:

```bash
cd backend

python train_models.py \
  --data path/to/AirQualityUCI.csv \
  --output ./models_pickle
```

This will:
1. Load and clean the dataset
2. Engineer lag and rolling mean features
3. Train XGBoost and Random Forest models
4. Save models as pickle files
5. Display performance metrics

## 🚀 Production Deployment

### Deploy Frontend to Vercel

```bash
# Connect to GitHub and push
git push origin main

# Vercel auto-deploys on push
```

Update environment variables in Vercel dashboard:
```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Deploy Backend to Railway/Render

**Railway** (Recommended):
```bash
npm i -g @railway/cli
railway up
```

**Render**:
1. Connect GitHub
2. Create new Web Service
3. Start command: `uvicorn main:app --host 0.0.0.0 --port 8000`

See `FASTAPI_SETUP.md` for detailed deployment instructions.

## 🐛 Troubleshooting

### Frontend not connecting to backend

1. Check backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Verify `.env.local` has correct `NEXT_PUBLIC_API_URL`

3. Check browser console for CORS errors

### Models not loading in backend

1. Verify pickle files exist in `backend/models_pickle/`
2. File names must be exact:
   - `xgb_model.pkl`
   - `rf_model.pkl`
   - `label_encoder.pkl`
3. Ensure xgboost version matches training version

### Port already in use

```bash
# Change FastAPI port
uvicorn main:app --reload --port 8001

# Update .env.local
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## 📚 Documentation

- **[FASTAPI_SETUP.md](./FASTAPI_SETUP.md)** - Detailed backend setup
- **[BACKEND_INTEGRATION.md](./BACKEND_INTEGRATION.md)** - Integration guide
- **[DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)** - Production checklist
- **[COMPONENTS.md](./COMPONENTS.md)** - Component reference
- **[BUILD_SUMMARY.md](./BUILD_SUMMARY.md)** - What was built

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙋 Support

- 📖 Check documentation files
- 🐛 Open an issue on GitHub
- 💬 Check API docs at /docs
- 🎯 See FASTAPI_SETUP.md for setup issues

## 🎉 Getting Started Checklist

- [ ] Clone/download the project
- [ ] Install frontend dependencies: `pnpm install`
- [ ] Create `.env.local` from `.env.local.example`
- [ ] Install backend dependencies: `pip install -r requirements.txt`
- [ ] Start backend: `uvicorn main:app --reload`
- [ ] Start frontend: `pnpm dev`
- [ ] Open http://localhost:3000
- [ ] View API docs at http://localhost:8000/docs
- [ ] Train models with your data (optional)
- [ ] Deploy to production!

---

**Built with ❤️ for real-time air quality monitoring**

Questions? Check the documentation files or review API docs at /docs!
