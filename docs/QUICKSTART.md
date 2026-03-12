# Quick Start Guide

Get your Air Quality Monitor dashboard running in minutes!

## 🚀 Start Development Server

```bash
# Install dependencies
pnpm install

# Start the dev server
pnpm dev

# Open http://localhost:3000 in your browser
```

**That's it!** The dashboard loads with mock data and is ready to use.

## 📦 What's Included

The dashboard comes pre-configured with:

- ✅ Real-time sensor data display (CO, CO₂, temperature, humidity, PM2.5, PM10)
- ✅ XGBoost model performance metrics (0.89 R² score)
- ✅ Next-hour CO predictions with confidence scores
- ✅ 200 hours of historical prediction data
- ✅ Interactive time series and scatter plot charts
- ✅ Feature importance rankings (top 10)
- ✅ AQI category distribution analysis
- ✅ Health recommendations based on air quality
- ✅ Dark theme with cyan accents

## 🎨 Dashboard Sections

### Top Section
- **Status Cards**: Current environmental readings
- **Live Indicator**: Shows real-time status

### Middle Section
- **Prediction Card**: Next hour's CO forecast
- **Performance Metrics**: Model accuracy metrics
- **Health Recommendations**: Guidance based on air quality

### Bottom Section
- **Analytics Charts**: Time series and validation plots
- **Model Analysis**: Feature importance and category distribution

## 🔄 Switching to Real Backend Data

When ready to connect your Python ML models:

1. **Update API endpoints** in `/app/api/`:
   - `predict/route.ts` - For CO predictions
   - `metrics/route.ts` - For model metrics

2. **See** `BACKEND_INTEGRATION.md` for detailed examples

3. **Example API integration**:
   ```typescript
   // In /app/api/predict/route.ts
   const response = await fetch('http://your-backend:5000/predict', {
     method: 'POST',
     body: JSON.stringify(sensorData)
   });
   ```

## 📊 Component Documentation

### Displaying Data
All components accept data and automatically handle formatting:

```tsx
// Sensor readings
<StatusCard title="CO" value={2.5} unit="mg/m³" />

// Predictions
<PredictionCard prediction={predictionData} />

// Metrics
<MetricsCard 
  title="Model Metrics"
  metrics={[
    { label: 'MAE', value: 0.34 },
    { label: 'RMSE', value: 0.52 }
  ]}
/>

// Charts (auto-scale to data)
<COTimeSeriesChart data={historicalData} />
<ScatterPlotChart data={historicalData} />
```

## 🎯 Key Files to Know

| File | Purpose |
|------|---------|
| `/app/page.tsx` | Main dashboard page |
| `/lib/mock-data.ts` | Replace here for real data |
| `/lib/types.ts` | TypeScript interfaces |
| `/components/dashboard/` | All dashboard components |
| `BACKEND_INTEGRATION.md` | Backend connection guide |

## ⚙️ Configuration

### Environment Variables

Create `.env.local`:
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
```

### Theme Customization

Edit `/app/globals.css` to customize:
- Colors (via CSS variables)
- Fonts (via Tailwind config)
- Spacing and sizing

## 🧪 Testing Features

### Try Different Air Quality Levels
Edit `/lib/mock-data.ts` to change simulated values:

```typescript
// Change CO level to test different categories
co: 5.0, // Will show "Unhealthy" category
```

### Mock Data Functions
- `getMockSensorData()` - Random sensor readings
- `getMockPrediction()` - Random predictions
- `getMockHistoricalData()` - 200 hours of data
- `getMockFeatureImportances()` - Top 10 features
- `getMockCategoryDistribution()` - AQI categories

## 🐛 Troubleshooting

**"Module not found" error:**
```bash
# Reinstall dependencies
rm -rf node_modules pnpm-lock.yaml
pnpm install
pnpm dev
```

**Charts not showing:**
- Ensure data is loaded (check console)
- Verify historical data has enough points (>5)
- Check browser DevTools console for errors

**Build failing:**
```bash
# Clean and rebuild
pnpm clean
pnpm build
```

## 📈 Next Steps

1. **Develop UI** - The mock data lets you work on the interface
2. **Test interactions** - Click, hover, check responsive design
3. **Prepare backend** - Set up Flask/FastAPI endpoints
4. **Connect models** - Update API routes with real calls
5. **Deploy** - Push to Vercel or your hosting

## 📚 Resources

- Next.js: https://nextjs.org/docs
- Recharts: https://recharts.org/docs
- Tailwind: https://tailwindcss.com/docs
- TypeScript: https://www.typescriptlang.org/docs

## 🔗 Important Links

- **Backend Integration**: `BACKEND_INTEGRATION.md`
- **Project README**: `README.md`
- **Component Library**: `components/dashboard/`

## 💡 Pro Tips

1. **Data Refresh**: Update mock data every 5 seconds in useEffect
2. **Real-time Updates**: Use SWR or React Query for API calls
3. **Error Handling**: All components have built-in loading states
4. **Mobile Responsive**: Dashboard is fully responsive on mobile

## 🎉 You're Ready!

Your Air Quality Monitor dashboard is ready to go. Open http://localhost:3000 and explore!

For backend connection help, see **BACKEND_INTEGRATION.md**.

---

Happy monitoring! 🌍
