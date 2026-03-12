'use client';

import { useState, useEffect } from 'react';
import { StatusCard } from '@/components/dashboard/status-card';
import { MetricsCard } from '@/components/dashboard/metrics-card';
import { PredictionCard } from '@/components/dashboard/prediction-card';
import { AQIStatusCard } from '@/components/dashboard/aqi-status-card';
import { AQIGauge } from '@/components/dashboard/aqi-gauge';
import { SystemStatus } from '@/components/dashboard/system-status';
import { Recommendations } from '@/components/dashboard/recommendations';
import { COTimeSeriesChart } from '@/components/dashboard/co-timeseries-chart';
import { ScatterPlotChart } from '@/components/dashboard/scatter-plot-chart';
import { FeatureImportanceChart } from '@/components/dashboard/feature-importance-chart';
import { CategoryDistributionChart } from '@/components/dashboard/category-distribution-chart';
import { apiClient } from '@/lib/api-client';
import {
  getMockSensorData,
  getMockPrediction,
  getMockMetrics,
  getMockFeatureImportances,
  getMockHistoricalData,
  getMockCategoryDistribution,
} from '@/lib/mock-data';
import { SensorData, Prediction, ModelMetrics, FeatureImportance, HistoricalData } from '@/lib/types';

export default function Dashboard() {
  const [sensorData, setSensorData] = useState<SensorData | null>(null);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null);
  const [features, setFeatures] = useState<FeatureImportance[]>([]);
  const [historicalData, setHistoricalData] = useState<HistoricalData[]>([]);
  const [categoryDistribution, setCategoryDistribution] = useState(null);
  const [backendAvailable, setBackendAvailable] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    const loadData = async () => {
      try {
        const isHealthy = await apiClient.health();
        setBackendAvailable(isHealthy);

        if (isHealthy) {
          const sensorReadings = {
            co_gt: 2.5 + Math.random() * 2.5,
            nox_gt: 100 + Math.random() * 50,
            no2_gt: 80 + Math.random() * 40,
            temperature: 20 + Math.random() * 8,
            relative_humidity: 40 + Math.random() * 35,
            pt08_s1_co: 1200 + Math.random() * 300,
            c6h6_gt: 3 + Math.random() * 2,
          };

          const predictionResult = await apiClient.predict(sensorReadings);
          setPrediction({
            nextHourCO: predictionResult.co_concentration_next_hour,
            confidence: predictionResult.confidence,
            category: predictionResult.predicted_category as any,
            categoryConfidence: predictionResult.confidence,
          });

          const metricsResult = await apiClient.getMetrics();
          setMetrics({
            mae: metricsResult.mae,
            rmse: metricsResult.rmse,
            r2: metricsResult.r2_score,
            categoryAccuracy: metricsResult.category_accuracy,
          });

          const features = predictionResult.feature_importance;
          setFeatures(
            features.map((f) => ({
              feature: f.feature,
              importance: f.importance,
            }))
          );

          const historicalResult = await apiClient.getHistorical(200);
          setHistoricalData(
            historicalResult.timestamps.map((ts: string, idx: number) => ({
              timestamp: new Date(ts),
              actual: historicalResult.actual_co[idx],
              predicted: historicalResult.predicted_co[idx],
            }))
          );
        } else {
          console.warn('FastAPI backend not available, using mock data');
          setSensorData(getMockSensorData());
          setPrediction(getMockPrediction());
          setMetrics(getMockMetrics());
          setFeatures(getMockFeatureImportances());
          setHistoricalData(getMockHistoricalData());
          setCategoryDistribution(getMockCategoryDistribution());
        }
      } catch (error) {
        console.error('Error loading data:', error);
        setSensorData(getMockSensorData());
        setPrediction(getMockPrediction());
        setMetrics(getMockMetrics());
        setFeatures(getMockFeatureImportances());
        setHistoricalData(getMockHistoricalData());
        setCategoryDistribution(getMockCategoryDistribution());
      }
      setLastUpdate(new Date());
    };

    loadData();
    setSensorData(getMockSensorData());
    setCategoryDistribution(getMockCategoryDistribution());
  }, []);

  if (!sensorData || !prediction || !metrics) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 flex items-center justify-center">
        <div className="text-center">
          <div className="h-12 w-12 rounded-full border-4 border-cyan-400 border-t-transparent animate-spin mx-auto mb-4"></div>
          <p className="text-slate-400">Loading air quality data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Sticky Header */}
      <div className="border-b border-slate-800 bg-gradient-to-r from-slate-900 to-slate-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-5">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <h1 className="text-2xl font-bold text-white tracking-tight">
                Indoor Air Quality Monitor
              </h1>
              <p className="text-xs text-slate-400">
                Living Room • Device AQI-01 • Real-time environmental monitoring
              </p>
            </div>
            <div className={`flex items-center gap-2 px-3.5 py-1.5 rounded-full text-sm font-semibold ${
              backendAvailable
                ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
                : 'bg-rose-500/15 text-rose-400 border border-rose-500/30'
            }`}>
              <div className={`h-1.5 w-1.5 rounded-full ${backendAvailable ? 'bg-emerald-400' : 'bg-rose-400'} animate-pulse`} />
              {backendAvailable ? 'Connected' : 'Offline'}
            </div>
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Section 1: Air Quality Status (Primary Focus) */}
        <section className="space-y-4">
          <div className="space-y-1">
            <h2 className="text-lg font-semibold text-white">Air Quality Status</h2>
            <p className="text-xs text-slate-400">Current classification and sensor overview</p>
          </div>
          <div className="grid gap-6 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <AQIStatusCard category={prediction.category} confidence={prediction.confidence} />
            </div>
            <div className="space-y-6">
              <div className="rounded-lg border border-slate-700 bg-slate-900/50 p-6 shadow-lg">
                <AQIGauge category={prediction.category} confidence={prediction.confidence} />
              </div>
              <SystemStatus backendAvailable={backendAvailable} lastUpdate={lastUpdate} />
            </div>
          </div>
        </section>

        {/* Section 2: Current Measurements */}
        <section className="space-y-4">
          <div className="space-y-1">
            <h2 className="text-lg font-semibold text-white">Current Measurements</h2>
            <p className="text-xs text-slate-400">Real-time sensor readings</p>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            <StatusCard title="CO Concentration" value={sensorData.co} unit="mg/m³" category={prediction.category} />
            <StatusCard title="Nitrogen Dioxide" value={sensorData.co2} unit="ppm" />
            <StatusCard title="Benzene" value={sensorData.pm25} unit="µg/m³" />
            <StatusCard title="Temperature" value={sensorData.temperature} unit="°C" />
            <StatusCard title="Humidity" value={sensorData.humidity} unit="%" />
            <StatusCard title="PM10 Particulates" value={sensorData.pm10} unit="µg/m³" />
          </div>
        </section>

        {/* Section 3: Forecast & Prediction */}
        <section className="space-y-4">
          <div className="space-y-1">
            <h2 className="text-lg font-semibold text-white">Forecast & Prediction</h2>
            <p className="text-xs text-slate-400">Next hour air quality prediction</p>
          </div>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <PredictionCard prediction={prediction} currentCO={sensorData.co} />
            </div>
            <div />
          </div>
        </section>

        {/* Section 4: Trend Analysis */}
        <section className="space-y-4">
          <div className="space-y-1">
            <h2 className="text-lg font-semibold text-white">Trend Analysis</h2>
            <p className="text-xs text-slate-400">Actual vs predicted CO levels over time</p>
          </div>
          <COTimeSeriesChart data={historicalData} />
        </section>

        {/* Section 5: Model Performance */}
        <section className="space-y-4">
          <div className="space-y-1">
            <h2 className="text-lg font-semibold text-white">Model Performance</h2>
            <p className="text-xs text-slate-400">ML model metrics and accuracy analysis</p>
          </div>
          <div className="grid gap-6 lg:grid-cols-2">
            <MetricsCard
              title="XGBoost Regressor Performance"
              metrics={[
                { label: 'MAE', value: metrics.mae.toFixed(3) },
                { label: 'RMSE', value: metrics.rmse.toFixed(3) },
                { label: 'R² Score', value: metrics.r2.toFixed(3) },
                { label: 'Category Accuracy', value: (metrics.categoryAccuracy * 100).toFixed(1), suffix: '%' },
              ]}
            />
            {categoryDistribution && <CategoryDistributionChart data={categoryDistribution} />}
          </div>
        </section>

        {/* Section 6: Feature Importance & Accuracy */}
        <section className="space-y-4">
          <div className="space-y-1">
            <h2 className="text-lg font-semibold text-white">ML Insights</h2>
            <p className="text-xs text-slate-400">Feature importance and prediction accuracy</p>
          </div>
          <div className="grid gap-6 lg:grid-cols-2">
            <FeatureImportanceChart data={features} />
            <ScatterPlotChart data={historicalData} />
          </div>
        </section>

        {/* Section 7: Health Recommendations */}
        <section className="space-y-4">
          <div className="space-y-1">
            <h2 className="text-lg font-semibold text-white">Health & Safety Guidance</h2>
            <p className="text-xs text-slate-400">Personalized recommendations based on current air quality</p>
          </div>
          <Recommendations category={prediction.category} sensorData={sensorData} />
        </section>

        {/* Footer */}
        <footer className="rounded-lg border border-slate-800 bg-slate-900/30 p-6 text-center">
          <p className="text-xs text-slate-500">
            Last updated: {lastUpdate.toLocaleString()} • Models: XGBoost + Random Forest • 
            Data source: UCI Air Quality Dataset • Dashboard v2.0
          </p>
        </footer>
      </div>
    </div>
  );
}
