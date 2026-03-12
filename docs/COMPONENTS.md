# Component Reference Guide

Complete documentation of all dashboard components with usage examples.

## 📋 Table of Contents

1. [Status Components](#status-components)
2. [Chart Components](#chart-components)
3. [Prediction & Analysis](#prediction--analysis)
4. [Utilities](#utilities)

---

## Status Components

### StatusCard
Displays a single metric with unit and optional AQI category indicator.

**Props:**
```typescript
interface StatusCardProps {
  title: string;           // e.g., "CO Concentration"
  value: number;           // e.g., 2.5
  unit: string;            // e.g., "mg/m³"
  category?: AQICategory;  // Optional: 'Good' | 'Moderate' | 'Unhealthy' | 'Hazardous'
  icon?: React.ReactNode;  // Optional: Icon component
}
```

**Usage:**
```tsx
<StatusCard
  title="CO Concentration"
  value={sensorData.co}
  unit="mg/m³"
  category="Moderate"
/>
```

**Features:**
- Dark gradient background
- Color-coded category indicator
- Responsive sizing
- Clean typography

---

### MetricsCard
Displays multiple metrics in a key-value list format.

**Props:**
```typescript
interface MetricsCardProps {
  title: string;
  metrics: Array<{
    label: string;
    value: number | string;
    suffix?: string;
  }>;
}
```

**Usage:**
```tsx
<MetricsCard
  title="Model Performance"
  metrics={[
    { label: 'MAE', value: 0.34 },
    { label: 'RMSE', value: 0.52 },
    { label: 'R² Score', value: 0.89 },
    { label: 'Accuracy', value: 93, suffix: '%' },
  ]}
/>
```

**Features:**
- Cyan highlighted values
- Optional suffix (%, mg/m³, etc.)
- Clean list formatting
- Dark theme optimized

---

## Chart Components

### COTimeSeriesChart
Time series line chart showing actual vs predicted CO over 50 hours.

**Props:**
```typescript
interface COTimeSeriesChartProps {
  data: HistoricalData[];  // Array of {timestamp, actual, predicted}
}
```

**Usage:**
```tsx
<COTimeSeriesChart data={historicalData} />
```

**Features:**
- Blue line for actual values
- Cyan dashed line for predictions
- Interactive tooltips
- Auto-scaling axes
- 50 most recent hours displayed
- Dark theme styling

**Data Format:**
```typescript
HistoricalData {
  timestamp: Date;
  actual: number;      // Actual CO in mg/m³
  predicted: number;   // Predicted CO in mg/m³
}
```

---

### ScatterPlotChart
Scatter plot validating predictions against perfect prediction line.

**Props:**
```typescript
interface ScatterPlotChartProps {
  data: HistoricalData[];
}
```

**Usage:**
```tsx
<ScatterPlotChart data={historicalData} />
```

**Features:**
- Blue scattered points for predictions
- Red dashed diagonal line (perfect prediction)
- Color-coded by distance from perfect line
- Interactive tooltips
- Helps visualize model accuracy
- Semi-transparent points for density visualization

---

### FeatureImportanceChart
Bar chart showing top 10 most important features from XGBoost model.

**Props:**
```typescript
interface FeatureImportanceChartProps {
  data: FeatureImportance[];
}

interface FeatureImportance {
  feature: string;      // e.g., "CO(GT)_lag1"
  importance: number;   // 0-1 scale
}
```

**Usage:**
```tsx
<FeatureImportanceChart data={features} />
```

**Features:**
- Top 10 features displayed
- Importance shown as percentage
- Cyan colored bars
- Angled labels for readability
- Shows feature names clearly
- Interactive hover information

---

### CategoryDistributionChart
Grouped bar chart comparing actual vs predicted AQI categories.

**Props:**
```typescript
interface CategoryDistributionChartProps {
  data: {
    Good: { actual: number; predicted: number };
    Moderate: { actual: number; predicted: number };
    Unhealthy: { actual: number; predicted: number };
    Hazardous: { actual: number; predicted: number };
  };
}
```

**Usage:**
```tsx
<CategoryDistributionChart data={categoryDistribution} />
```

**Features:**
- Green bars for actual counts
- Teal bars for predicted counts
- Clear category labels
- Shows model's category accuracy
- Interactive legend
- Responsive layout

---

## Prediction & Analysis

### PredictionCard
Large prominent card showing next-hour prediction with category emoji.

**Props:**
```typescript
interface PredictionCardProps {
  prediction: Prediction;
}

interface Prediction {
  nextHourCO: number;        // Predicted CO in mg/m³
  confidence: number;         // 0-1 scale
  category: AQICategory;      // 'Good' | 'Moderate' | 'Unhealthy' | 'Hazardous'
  categoryConfidence: number; // 0-1 scale
}
```

**Usage:**
```tsx
<PredictionCard prediction={prediction} />
```

**Features:**
- Large emoji for quick visual recognition (😊😐😷⚠️)
- Background color matches category
- Shows predicted CO value
- Displays confidence percentage
- Shows category confidence
- All values in highlighted boxes

**Category Colors:**
- Good: Green
- Moderate: Yellow
- Unhealthy: Orange
- Hazardous: Red

---

### Recommendations
Health guidance and recommendations based on current air quality.

**Props:**
```typescript
interface RecommendationsProps {
  category: AQICategory;
  sensorData: SensorData;
}

interface SensorData {
  co: number;
  co2: number;
  temperature: number;
  humidity: number;
  pm25: number;
  pm10: number;
  timestamp: Date;
}
```

**Usage:**
```tsx
<Recommendations 
  category={prediction.category} 
  sensorData={sensorData}
/>
```

**Features:**
- Category-specific guidance
- 3-4 key recommendations
- Environmental conditions section
- Real-time temperature display
- PM2.5 and PM10 values
- Humidity indicator
- Color-coded for readability

**Sample Recommendations:**

**Good Category:**
- ✓ Excellent time for outdoor activities
- ✓ No air quality alerts
- ✓ Keep windows open for ventilation

**Moderate Category:**
- ⚠ Avoid prolonged outdoor exertion
- ⚠ Sensitive groups should limit outdoor activities
- ⚠ Consider closing windows if needed

**Unhealthy Category:**
- 🚫 Avoid outdoor activities
- 🚫 Keep windows closed
- 🚫 Wear N95 masks if going outside
- 🚫 Use air purifiers indoors

**Hazardous Category:**
- 🚨 Remain indoors
- 🚨 Use air purifiers with HEPA filters
- 🚨 Wear N95+ masks if you must go out
- 🚨 Minimize physical exertion

---

### ModelInfo
Information card about the ML model and its capabilities.

**Usage:**
```tsx
<ModelInfo />
```

**Features:**
- Model type (XGBoost Regressor)
- Training data source
- Top features listed
- Prediction target explained
- Static component (no props)

---

## Utilities

### Types (lib/types.ts)

Core TypeScript interfaces for type safety:

```typescript
// Sensor data from devices
type SensorData = {
  co: number;
  co2: number;
  temperature: number;
  humidity: number;
  pm25: number;
  pm10: number;
  timestamp: Date;
}

// Model prediction output
type Prediction = {
  nextHourCO: number;
  confidence: number;
  category: AQICategory;
  categoryConfidence: number;
}

// Model performance
type ModelMetrics = {
  mae: number;
  rmse: number;
  r2: number;
  categoryAccuracy: number;
}

// Feature importance
type FeatureImportance = {
  feature: string;
  importance: number;
}

// Historical data point
type HistoricalData = {
  timestamp: Date;
  actual: number;
  predicted: number;
}

// AQI categories
type AQICategory = 'Good' | 'Moderate' | 'Unhealthy' | 'Hazardous';
```

### Mock Data (lib/mock-data.ts)

Functions for generating realistic mock data:

```typescript
// Get single sensor reading
getMockSensorData(): SensorData

// Get prediction
getMockPrediction(): Prediction

// Get model metrics
getMockMetrics(): ModelMetrics

// Get feature importances (top 10)
getMockFeatureImportances(): FeatureImportance[]

// Get 200 hours of historical data
getMockHistoricalData(): HistoricalData[]

// Get category distribution
getMockCategoryDistribution(): {
  Good: {actual, predicted},
  Moderate: {actual, predicted},
  Unhealthy: {actual, predicted},
  Hazardous: {actual, predicted}
}
```

---

## Layout Example

```tsx
export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950">
      {/* Header */}
      <header>
        <h1>Air Quality Monitor</h1>
      </header>

      {/* Status Overview */}
      <section>
        <StatusCard title="CO" value={2.5} unit="mg/m³" />
        <StatusCard title="Temp" value={22} unit="°C" />
        {/* ... more status cards ... */}
      </section>

      {/* Predictions & Metrics */}
      <section>
        <PredictionCard prediction={prediction} />
        <MetricsCard title="Model" metrics={[...]} />
        <Recommendations category={category} sensorData={data} />
      </section>

      {/* Charts */}
      <section>
        <COTimeSeriesChart data={historical} />
        <ScatterPlotChart data={historical} />
        <FeatureImportanceChart data={features} />
        <CategoryDistributionChart data={distribution} />
      </section>
    </div>
  );
}
```

---

## Styling & Theming

All components use:
- **Dark Background**: Slate-900/800
- **Text**: Slate-300/400 for secondary, white for primary
- **Accents**: Cyan-400 for highlights
- **Borders**: Subtle slate-700/800
- **Cards**: Gradient backgrounds from slate-900 to slate-800

To customize, edit `/app/globals.css`:
```css
:root {
  --primary: oklch(...);     /* Cyan */
  --secondary: oklch(...);   /* Slate */
  --accent: oklch(...);      /* Cyan accent */
}
```

---

## Responsive Behavior

All components are responsive:
- **Mobile**: Full width, stacked layout
- **Tablet**: 2-column grids
- **Desktop**: 3-column grids where applicable

Charts automatically:
- Adjust height
- Scale fonts
- Reduce animation
- Optimize for touch

---

## Accessibility

Components include:
- ✓ Semantic HTML
- ✓ Color contrast compliance
- ✓ Keyboard navigation support
- ✓ ARIA labels where needed
- ✓ Mobile-friendly touch targets

---

## Performance Tips

1. **Memoize Components**: Use React.memo for expensive renders
2. **Lazy Load Charts**: Use dynamic imports for Recharts
3. **Optimize Data**: Slice historical data to needed range
4. **Debounce Resizes**: Use resize debouncing for responsive charts

---

For more information, see:
- **README.md** - Full project overview
- **BACKEND_INTEGRATION.md** - API integration guide
- **QUICKSTART.md** - Getting started
