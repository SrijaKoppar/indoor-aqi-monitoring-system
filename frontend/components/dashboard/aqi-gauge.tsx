import { Card } from '@/components/ui/card';
import { AQICategory } from '@/lib/types';

interface AQIGaugeProps {
  category: AQICategory;
  confidence: number;
}

export function AQIGauge({ category, confidence }: AQIGaugeProps) {
  const categoryOrder: AQICategory[] = ['Good', 'Moderate', 'Unhealthy', 'Hazardous'];
  const categoryColors = {
    Good: 'bg-emerald-500',
    Moderate: 'bg-amber-400',
    Unhealthy: 'bg-orange-500',
    Hazardous: 'bg-rose-600',
  };

  const categoryLabels = {
    Good: 'emerald',
    Moderate: 'amber',
    Unhealthy: 'orange',
    Hazardous: 'rose',
  };

  const currentIndex = categoryOrder.indexOf(category);

  return (
    <Card className="border-0 shadow-lg overflow-hidden h-full">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-5">
        <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-3.5">
          Air Quality Index
        </h3>

        {/* Gauge Bars */}
        <div className="space-y-2.5 mb-4">
          <div className="flex gap-1.5">
            {categoryOrder.map((cat, idx) => (
              <div
                key={cat}
                className={`flex-1 h-9 rounded-lg transition-all duration-500 ${
                  idx <= currentIndex
                    ? `${categoryColors[cat]}`
                    : 'bg-slate-700/40'
                }`}
                title={cat}
              />
            ))}
          </div>

          <div className="flex justify-between text-xs font-semibold px-1">
            <span className="text-emerald-400">Good</span>
            <span className="text-amber-400">Moderate</span>
            <span className="text-orange-400">Unhealthy</span>
            <span className="text-rose-400">Hazardous</span>
          </div>
        </div>

        {/* Divider */}
        <div className="h-px bg-slate-700 mb-4" />

        {/* Confidence Display */}
        <div className="text-center">
          <p className="text-xs text-slate-400 uppercase tracking-wider mb-1">
            Model Confidence
          </p>
          <p className="text-2xl font-bold text-cyan-400">
            {(confidence * 100).toFixed(0)}%
          </p>
          <div className="mt-2.5 h-1.5 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-cyan-500 to-cyan-400"
              style={{ width: `${confidence * 100}%` }}
            />
          </div>
        </div>
      </div>
    </Card>
  );
}
