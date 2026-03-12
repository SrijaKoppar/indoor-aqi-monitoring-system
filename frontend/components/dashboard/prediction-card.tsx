import { Card } from '@/components/ui/card';
import { Prediction, AQICategory } from '@/lib/types';

interface PredictionCardProps {
  prediction: Prediction;
  currentCO?: number;
}

const categoryEmoji: Record<AQICategory, string> = {
  Good: '😊',
  Moderate: '😐',
  Unhealthy: '😷',
  Hazardous: '⚠️',
};

const categoryBgGradient: Record<AQICategory, string> = {
  Good: 'from-green-900 to-green-800',
  Moderate: 'from-yellow-900 to-yellow-800',
  Unhealthy: 'from-orange-900 to-orange-800',
  Hazardous: 'from-red-900 to-red-800',
};

export function PredictionCard({ prediction, currentCO }: PredictionCardProps) {
  const getTrendIndicator = (currentCO: number | undefined, nextHourCO: number): { text: string; emoji: string } => {
    if (!currentCO) return { text: 'Stable', emoji: '→' };
    const diff = nextHourCO - currentCO;
    if (diff > 0.2) return { text: 'Increasing', emoji: '↑' };
    if (diff < -0.2) return { text: 'Improving', emoji: '↓' };
    return { text: 'Stable', emoji: '→' };
  };

  const trend = getTrendIndicator(currentCO, prediction.nextHourCO);

  return (
    <Card className="overflow-hidden border-0 shadow-lg">
      <div className={`bg-gradient-to-br ${categoryBgGradient[prediction.category]} p-8`}>
        <div className="space-y-6">
          {/* Header */}
          <div>
            <h3 className="text-sm font-semibold text-white/80 uppercase tracking-wider mb-2">
              Next Hour Forecast
            </h3>
            <p className="text-3xl font-bold text-white">
              {prediction.category} Expected
            </p>
          </div>

          {/* Emoji indicator */}
          <div className="text-5xl">{categoryEmoji[prediction.category]}</div>

          {/* Divider */}
          <div className="h-px bg-white/20" />

          {/* Stats Grid */}
          <div className="space-y-3">
            <div className="flex items-center justify-between rounded-lg bg-black/15 p-4 backdrop-blur-sm">
              <span className="text-sm text-white/80">CO Level</span>
              <span className="text-lg font-bold text-white">
                {prediction.nextHourCO.toFixed(2)} mg/m³
              </span>
            </div>

            <div className="flex items-center justify-between rounded-lg bg-black/15 p-4 backdrop-blur-sm">
              <span className="text-sm text-white/80">Trend</span>
              <div className="flex items-center gap-2">
                <span className="text-lg">{trend.emoji}</span>
                <span className="text-lg font-bold text-white">
                  {trend.text}
                </span>
              </div>
            </div>

            <div className="flex items-center justify-between rounded-lg bg-black/15 p-4 backdrop-blur-sm">
              <span className="text-sm text-white/80">Confidence</span>
              <span className="text-lg font-bold text-white">
                {(prediction.confidence * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}
