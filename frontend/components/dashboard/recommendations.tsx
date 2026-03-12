import { Card } from '@/components/ui/card';
import { AQICategory, SensorData } from '@/lib/types';

interface RecommendationsProps {
  category: AQICategory;
  sensorData: SensorData;
}

const recommendations: Record<AQICategory, string[]> = {
  Good: [
    '✓ Excellent time for outdoor activities',
    '✓ No air quality alerts',
    '✓ Keep windows open for ventilation',
  ],
  Moderate: [
    '⚠ Avoid prolonged outdoor exertion',
    '⚠ Sensitive groups should limit outdoor activities',
    '⚠ Consider closing windows if needed',
  ],
  Unhealthy: [
    '🚫 Avoid outdoor activities',
    '🚫 Keep windows closed',
    '🚫 Wear N95 masks if going outside',
    '🚫 Use air purifiers indoors',
  ],
  Hazardous: [
    '🚨 Remain indoors',
    '🚨 Use air purifiers with HEPA filters',
    '🚨 Wear N95+ masks if you must go out',
    '🚨 Minimize physical exertion',
  ],
};

export function Recommendations({
  category,
  sensorData,
}: RecommendationsProps) {
  return (
    <Card className="border-0 shadow-lg overflow-hidden col-span-full lg:col-span-1">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-6">
        {/* Header */}
        <h3 className="mb-4 text-sm font-semibold text-slate-300 uppercase tracking-wider">
          Health & Safety Guidance
        </h3>

        <div className="h-px bg-slate-700 mb-6" />

        {/* Recommendations List */}
        <div className="space-y-3 mb-6">
          {recommendations[category].map((rec, idx) => (
            <div
              key={idx}
              className="flex gap-3 p-3 rounded-lg bg-slate-700/20 hover:bg-slate-700/30 transition-colors"
            >
              <div className="flex-shrink-0 text-lg mt-0.5">{rec.split(' ')[0]}</div>
              <p className="text-sm text-slate-300 flex-1">
                {rec.split(' ').slice(1).join(' ')}
              </p>
            </div>
          ))}
        </div>

        {/* Environmental Conditions */}
        <div className="pt-4 border-t border-slate-700">
          <h4 className="mb-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Environmental Conditions
          </h4>
          <div className="grid grid-cols-2 gap-2">
            {[
              { label: 'Temperature', value: sensorData.temperature.toFixed(1), unit: '°C' },
              { label: 'Humidity', value: sensorData.humidity.toFixed(0), unit: '%' },
              { label: 'PM2.5', value: sensorData.pm25.toFixed(1), unit: 'µg/m³' },
              { label: 'PM10', value: sensorData.pm10.toFixed(1), unit: 'µg/m³' },
            ].map((item, idx) => (
              <div key={idx} className="p-2 rounded bg-slate-700/20">
                <p className="text-xs text-slate-400 uppercase tracking-wide mb-1">
                  {item.label}
                </p>
                <p className="font-semibold text-cyan-400 text-sm">
                  {item.value} <span className="text-slate-400 text-xs">{item.unit}</span>
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
}
