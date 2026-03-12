# Air Quality Monitor Dashboard

A professional, real-time air quality monitoring dashboard powered by machine learning predictions. Built with Next.js, React, and Recharts, displaying real-time environmental sensor data with XGBoost ML model predictions.

## 🎯 Features

### Real-Time Monitoring
- **Current Sensor Readings**: CO, CO₂, Temperature, Humidity, PM2.5, PM10
- **Live Status Indicators**: Color-coded air quality status
- **Environmental Alerts**: Real-time notifications based on AQI

### Machine Learning Predictions
- **Next-Hour CO Forecast**: XGBoost model predictions with confidence scores
- **AQI Category Classification**: Good, Moderate, Unhealthy, Hazardous
- **Model Performance Metrics**: MAE, RMSE, R² Score, Category Accuracy

### Analytics & Insights
- **Time Series Analysis**: 50-hour historical CO concentration trends
- **Prediction Validation**: Scatter plot comparing actual vs predicted values
- **Feature Importance**: Top 10 most important features driving predictions
- **Category Distribution**: Histogram of predicted vs actual AQI categories

### Health Recommendations
- **Category-based Guidance**: Tailored health suggestions based on air quality
- **Activity Recommendations**: Outdoor activity advisories
- **Environmental Conditions**: Real-time environmental parameter display

## 🏗️ Project Structure

```
/app
  /api
    /predict          # ML prediction endpoint
    /metrics          # Model metrics endpoint
  /layout.tsx         # Root layout with dark theme
  /page.tsx           # Main dashboard page
  /globals.css        # Global styles with design tokens

/components
  /ui                 # shadcn/ui components
  /dashboard
    /status-card.tsx              # Current status display
    /prediction-card.tsx          # Next-hour forecast
    /metrics-card.tsx             # Model performance
    /recommendations.tsx          # Health guidance
    /co-timeseries-chart.tsx      # Time series chart
    /scatter-plot-chart.tsx       # Validation scatter
    /feature-importance-chart.tsx # Feature rankings
    /category-distribution-chart.tsx # AQI categories
    /model-info.tsx               # Model information

/lib
  /types.ts           # TypeScript interfaces
  /mock-data.ts       # Mock data for development

BACKEND_INTEGRATION.md # Guide for connecting Python backend
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- pnpm (recommended) or npm/yarn

### Installation

```bash
# Clone and install
git clone <repo>
cd air-quality-monitor
pnpm install

# Start development server
pnpm dev

# Open http://localhost:3000
```

### Development with Mock Data

The dashboard comes with mock data from `/lib/mock-data.ts`, allowing you to develop and test the UI without a backend. This includes:

- Realistic sensor readings with random variations
- XGBoost predictions with confidence scores
- 200 hours of historical data with actual vs predicted values
- Top 10 feature importances
- AQI category distributions

## 🔌 Backend Integration

To connect your Python ML models:

1. **Implement API Endpoints** (see `BACKEND_INTEGRATION.md`):
   - `POST /api/predict` - Get predictions
   - `GET /api/metrics` - Get model metrics
   - `GET /api/historical` - Get historical data
   - `GET /api/features` - Get feature importances

2. **Update API Routes**:
   - Replace mock data in `/app/api/predict/route.ts`
   - Replace mock data in `/app/api/metrics/route.ts`
   - Add new routes for historical and feature data

3. **Configure Environment**:
   ```env
   NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
   ```

See `BACKEND_INTEGRATION.md` for detailed Flask backend example.

## 📊 Dashboard Components

### StatusCard
Displays current sensor reading with unit and optional AQI category indicator.
```tsx
<StatusCard
  title="CO Concentration"
  value={2.5}
  unit="mg/m³"
  category="Moderate"
/>
```

### PredictionCard
Shows next-hour forecast with category emoji, confidence, and guidance.
```tsx
<PredictionCard prediction={{
  nextHourCO: 2.8,
  confidence: 0.92,
  category: 'Moderate',
  categoryConfidence: 0.89
}} />
```

### Charts
- **COTimeSeriesChart**: Actual vs predicted CO over time
- **ScatterPlotChart**: Validation against perfect prediction line
- **FeatureImportanceChart**: Top 10 most important features
- **CategoryDistributionChart**: AQI category accuracy

### Recommendations
Context-aware health recommendations based on current air quality:
```tsx
<Recommendations 
  category="Moderate" 
  sensorData={sensorData}
/>
```

## 🎨 Design

- **Theme**: Dark mode with cyan accents for environmental monitoring
- **Colors**: 
  - Background: Slate-950 gradient
  - Accent: Cyan-400 for highlights
  - Status: Green (Good), Yellow (Moderate), Orange (Unhealthy), Red (Hazardous)
- **Typography**: Geist font family
- **Charts**: Recharts with custom dark theme

## 📈 Model Information

**XGBoost Regressor Performance:**
- **R² Score**: 0.89
- **MAE**: 0.34 mg/m³
- **RMSE**: 0.52 mg/m³
- **Category Accuracy**: 93%

**Top Features:**
1. CO(GT)_lag1 (23% importance)
2. Hour (14% importance)
3. CO(GT)_rollmean3 (9% importance)
4. NOx(GT)_lag1 (6.5% importance)

**Training Data**: Air Quality UCI Dataset (~9,000+ samples)

## 🔧 Technologies Used

- **Framework**: Next.js 16
- **UI**: shadcn/ui
- **Charts**: Recharts
- **Styling**: Tailwind CSS
- **Type Safety**: TypeScript
- **Analytics**: Vercel Analytics

## 📝 API Response Examples

### Prediction Response
```json
{
  "nextHourCO": 2.8,
  "confidence": 0.92,
  "category": "Moderate",
  "categoryConfidence": 0.89
}
```

### Metrics Response
```json
{
  "mae": 0.34,
  "rmse": 0.52,
  "r2": 0.89,
  "categoryAccuracy": 0.93
}
```

### Historical Data Response
```json
[
  {
    "timestamp": "2024-03-12T10:00:00Z",
    "actual": 2.5,
    "predicted": 2.6
  }
]
```

### Features Response
```json
[
  { "feature": "CO(GT)_lag1", "importance": 0.23 },
  { "feature": "hour", "importance": 0.14 }
]
```

## 🚢 Deployment

### Vercel (Recommended)
```bash
vercel deploy
```

### Environment Variables
Create `.env.local`:
```env
NEXT_PUBLIC_BACKEND_URL=your-backend-url
```

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Recharts Documentation](https://recharts.org)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Tailwind CSS Documentation](https://tailwindcss.com)

## 📄 License

This project is part of a university coursework (23BCT0057).

## 🤝 Contributing

This is a coursework project. For modifications:

1. Backend integration is ready via API routes
2. Mock data can be replaced with real API calls
3. New charts or components can be added following existing patterns
4. Theme customization available through design tokens in `globals.css`

## 📞 Support

For backend integration assistance, refer to `BACKEND_INTEGRATION.md`.

---

Built with ❤️ for environmental monitoring and air quality awareness.
