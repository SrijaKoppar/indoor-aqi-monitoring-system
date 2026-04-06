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
import { getLatestReading } from "@/lib/api-client";

export default function Dashboard() {
  const [sensorData, setSensorData] = useState<SensorData | null>(null);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null);
  const [features, setFeatures] = useState<FeatureImportance[]>([]);
  const [historicalData, setHistoricalData] = useState<HistoricalData[]>([]);
  const [categoryDistribution, setCategoryDistribution] = useState(null);
  const [backendAvailable, setBackendAvailable] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [data, setData] = useState(null);

  useEffect(() => {
    // Fetch immediately on load
    getLatestReading().then(setData);

    // Then poll every 5 seconds
    const interval = setInterval(() => {
      getLatestReading().then(setData);
    }, 2000);

    // Cleanup on unmount
    return () => clearInterval(interval);
  }, []);

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
      <div className="min-h-screen bg-gradient-to-br from-slate-800 via-slate-850 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="h-12 w-12 rounded-full border-4 border-cyan-400 border-t-transparent animate-spin mx-auto mb-4"></div>
          <p className="text-slate-400">Loading air quality data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-0">
      {/* Sticky Header */}
      <div className="border-b border-slate-800 bg-gradient-to-r from-slate-900 to-slate-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <h1 className="text-2xl font-bold text-white tracking-tight">
                Indoor Air Quality Monitor
              </h1>
              <p className="text-xs text-slate-400">
                Living Room • Device AQI-01 • Real-time environmental monitoring
              </p>
            </div>
            <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-semibold ${
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

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6">
        {/* Section 1: Air Quality Status - Premium Focus */}
        <div className="mb-6">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-white">Air Quality Status</h2>
          </div>
          <div className="grid gap-5 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <AQIStatusCard category={prediction.category} confidence={prediction.confidence} />
            </div>
            <div className="space-y-5">
              <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-5 shadow-lg">
                <AQIGauge category={prediction.category} confidence={prediction.confidence} />
              </div>
            </div>
          </div>
        </div>

        {/* Section 2: Forecast & Prediction */}
        <div className="mb-6">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-white">Forecast & Prediction</h2>
          </div>
          <div className="grid gap-5 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <PredictionCard prediction={prediction} currentCO={sensorData.co} />
            </div>
          </div>
        </div>

        {/* Section 3: Current Measurements */}
        <div className="mb-6">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-white">Current Measurements</h2>
          </div>
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
            <StatusCard title="CO Concentration" value={sensorData.co} unit="mg/m³" category={prediction.category} />
            <StatusCard title="Nitrogen Dioxide" value={sensorData.co2} unit="ppm" />
            <StatusCard title="Benzene" value={sensorData.pm25} unit="µg/m³" />
            <StatusCard title="Temperature" value={sensorData.temperature} unit="°C" />
            <StatusCard title="Humidity" value={sensorData.humidity} unit="%" />
            <StatusCard title="PM10 Particulates" value={sensorData.pm10} unit="µg/m³" />
          </div>
        </div>

        {/* Section 4: Trend Analysis */}
        <div className="mb-6">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-white">Trend Analysis</h2>
          </div>
          <COTimeSeriesChart data={historicalData} />
        </div>

        {/* Section 5: Model Performance */}
        <div className="mb-6">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-white">Model Performance</h2>
          </div>
          <div className="grid gap-5 lg:grid-cols-2">
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
        </div>

        {/* Section 6: Feature Importance & Accuracy */}
        <div className="mb-6">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-white">ML Insights</h2>
          </div>
          <div className="grid gap-5 lg:grid-cols-2">
            <FeatureImportanceChart data={features} />
            <ScatterPlotChart data={historicalData} />
          </div>
        </div>

        {/* Section 7: Health Recommendations */}
        <div className="mb-6">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-white">Health & Safety Guidance</h2>
          </div>
          <Recommendations category={prediction.category} sensorData={sensorData} />
        </div>

        {/* Footer */}
        <footer className="rounded-lg border border-slate-800 bg-slate-900/30 p-5 text-center">
          <p className="text-xs text-slate-500">
            Last updated: {lastUpdate.toLocaleString()} • Models: XGBoost + Random Forest • 
            Data source: UCI Air Quality Dataset • Dashboard v2.0
          </p>
        </footer>
      </div>
    </div>
  );
}
