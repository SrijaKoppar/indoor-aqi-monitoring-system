# Quick Reference Guide

## Dashboard Structure at a Glance

### Page Layout (Top to Bottom)

```
1. HEADER
   └─ Device Info + Connection Status (green/red indicator)

2. SENSOR READINGS (Row 1)
   ├─ CO Concentration (mg/m³)
   ├─ Nitrogen Dioxide (ppm)
   ├─ Benzene (µg/m³)
   ├─ Temperature (°C)
   ├─ Humidity (%)
   └─ PM10 (µg/m³)

3. CURRENT AQI [MAIN FOCUS] (Row 2)
   ├─ AQI Category (Good/Moderate/Unhealthy/Hazardous)
   ├─ Model Confidence
   └─ Category Description

4. FORECAST (Row 3)
   ├─ Next Hour CO Prediction
   ├─ Trend Indicator (↑/↓/→)
   ├─ Confidence Score
   ├─ AQI Gauge Visual
   └─ System Status

5. TRENDS (Row 4)
   └─ Actual vs Predicted CO Time Series

6. ML INSIGHTS #1 (Row 5)
   ├─ Feature Importance Chart
   └─ Scatter Plot (Actual vs Predicted)

7. ML INSIGHTS #2 (Row 6)
   ├─ Model Metrics (MAE, RMSE, R², Accuracy)
   └─ Category Distribution

8. HEALTH RECOMMENDATIONS (Row 7)
   ├─ Activity Recommendations
   ├─ Precautions
   └─ Environmental Conditions

9. FOOTER
   └─ Data Info & Credits
```

## Color Coding Quick Ref

| AQI Level | Color | Meaning |
|-----------|-------|---------|
| 🟢 Good | Green | Safe, normal activities |
| 🟡 Moderate | Yellow | Caution for sensitive groups |
| 🟠 Unhealthy | Orange | Avoid outdoor exertion |
| 🔴 Hazardous | Red | Remain indoors |

## Key Features

### ✅ What's New
1. **AQI Status Card** - Large, prominent main display
2. **System Status** - Backend, models, last update
3. **AQI Gauge** - Visual representation of quality
4. **Trend Indicator** - ↑ Increasing / ↓ Improving / → Stable
5. **Reorganized Layout** - Monitoring first, analysis last

### ✅ What Still Works
- FastAPI backend integration
- Mock data fallback
- Responsive design (mobile/tablet/desktop)
- All original components and charts
- Type-safe with TypeScript

### ✅ What Improved
- Error handling with graceful fallback
- Better visual hierarchy
- System health visibility
- Health recommendations prominence
- Header shows connection status

## Running the Project

### Without Backend (Quick Testing)
```bash
npm install
npm run dev
# Open http://localhost:3000
```
→ Uses beautiful mock data

### With Backend (Full Features)
```bash
# Terminal 1: Frontend
npm install
npm run dev

# Terminal 2: Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
→ Header shows green "Connected"

## Component Files Location

### Core Components
```
components/dashboard/
├── aqi-status-card.tsx (NEW) - Main AQI display
├── aqi-gauge.tsx (NEW) - Visual gauge
├── system-status.tsx (NEW) - System health
├── prediction-card.tsx (UPDATED) - Now has trend
├── status-card.tsx - Sensor readings
├── co-timeseries-chart.tsx - Time series
├── scatter-plot-chart.tsx - Accuracy plot
├── feature-importance-chart.tsx - Top features
├── category-distribution-chart.tsx - AQI distribution
├── recommendations.tsx - Health guidance
├── metrics-card.tsx - Model performance
└── model-info.tsx - Model information
```

### Main Page
```
app/
├── page.tsx (UPDATED) - Reorganized dashboard layout
└── layout.tsx - Root layout with dark theme
```

## Common Customizations

### Change Header Info
File: `app/page.tsx` → Header section
```tsx
<p className="mt-1 text-sm text-slate-400">
  Living Room • Device AQI-01 • Real-time environmental monitoring
</p>
```

### Add Sensor to Dashboard
File: `app/page.tsx` → ROW 1
```tsx
<StatusCard
  title="New Sensor"
  value={sensorData.newValue}
  unit="unit"
/>
```

### Change Color Scheme
Files: `components/dashboard/aqi-*.tsx`
```tsx
const categoryColors: Record<AQICategory, string> = {
  Good: 'from-green-600 to-green-700',  // Change these
  Moderate: 'from-yellow-500 to-yellow-600',
  // ...
}
```

### Adjust Trend Threshold
File: `components/dashboard/prediction-card.tsx`
```tsx
if (diff > 0.2) return '↑ Increasing';  // Change 0.2 to adjust
if (diff < -0.2) return '↓ Improving';
```

## API Endpoints (When Backend Running)

```
GET  /health              - Check if backend is alive
POST /predict             - Get CO prediction
GET  /metrics             - Get model performance metrics
GET  /historical/{count}  - Get historical data
GET  /docs               - API documentation (Swagger UI)
GET  /redoc              - API documentation (ReDoc)
```

## Troubleshooting

### Dashboard shows "Loading..."
- Check browser console (F12) for errors
- Verify Node.js is installed: `node --version`
- Clear node_modules: `rm -rf node_modules && npm install`

### Backend shows "Offline"
- Check if backend is running
- Verify port 8000 is not in use
- Check FastAPI startup messages

### Charts not displaying
- Verify data is loaded (check console)
- Check if backend is returning valid data
- Try page refresh

### Colors look wrong
- Check if dark mode is enabled
- Verify Tailwind CSS is loaded
- Clear browser cache (Ctrl+Shift+Del)

## Documentation Files

| File | Purpose |
|------|---------|
| `README_REACT_FASTAPI.md` | Full backend integration guide |
| `IMPLEMENTATION_CHANGES.md` | What was changed (detailed) |
| `VERIFICATION_CHECKLIST.md` | Testing checklist |
| `CONFIG_IMPLEMENTATION_SUMMARY.md` | Configuration summary |
| `ARCHITECTURE.md` | System architecture |
| `START_HERE.md` | Quick start guide |

## Important Files

```
MUST READ:
├── README_REACT_FASTAPI.md - Backend setup
├── CONFIG_IMPLEMENTATION_SUMMARY.md - What's new
└── VERIFICATION_CHECKLIST.md - Test this

REFERENCE:
├── IMPLEMENTATION_CHANGES.md - Detailed changes
├── ARCHITECTURE.md - System design
├── COMPONENTS.md - Component reference
└── QUICKSTART.md - 5-minute setup
```

## Status Indicator Legend

| Icon | Meaning |
|------|---------|
| 🟢 Connected | Backend is running and responsive |
| 🔴 Offline | Backend unreachable, using mock data |
| 🟡 Moderate | System healthy, slight issues |
| 🔵 Loading | Data is being fetched |

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| F12 | Open Developer Tools |
| Ctrl+R | Refresh Page |
| Ctrl+Shift+I | Inspect Element |

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Performance Tips

1. **Reduce chart data**: Limit historical data points
2. **Lazy load charts**: Load on demand instead of all at once
3. **Cache predictions**: Store in localStorage
4. **Debounce updates**: Reduce refresh frequency
5. **Compress images**: Optimize any images used

## Security Notes

- All API calls should use HTTPS in production
- Validate all sensor data from backend
- Don't expose API keys in frontend code
- Use environment variables for configuration
- Implement rate limiting on backend

## Next Steps

1. **Run the app**: `npm run dev`
2. **Check the layout**: Verify 7 rows display correctly
3. **Test responsiveness**: Open DevTools (F12) → Mobile
4. **Start backend** (optional): Follow backend setup
5. **Explore code**: Check components/ and app/ directories
6. **Customize**: Modify header, colors, sensors as needed

---

**Quick Links**:
- 📖 [README](./README_REACT_FASTAPI.md)
- 🚀 [Quick Start](./START_HERE.md)
- 🏗️ [Architecture](./ARCHITECTURE.md)
- ✅ [Checklist](./VERIFICATION_CHECKLIST.md)
