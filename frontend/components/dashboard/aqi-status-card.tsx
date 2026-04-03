import { Card } from '@/components/ui/card';
import { AQICategory } from '@/lib/types';

interface AQIStatusCardProps {
  category: AQICategory;
  confidence: number;
}

const categoryColors: Record<AQICategory, string> = {
  Good: 'from-emerald-600 to-emerald-700',
  Moderate: 'from-amber-500 to-amber-600',
  Unhealthy: 'from-orange-600 to-orange-700',
  Hazardous: 'from-rose-600 to-rose-700',
};

const categoryAccent: Record<AQICategory, string> = {
  Good: 'emerald',
  Moderate: 'amber',
  Unhealthy: 'orange',
  Hazardous: 'rose',
};

const categoryDescriptions: Record<AQICategory, string> = {
  Good: 'Air quality is satisfactory and air pollution poses little or no risk.',
  Moderate: 'Air quality is acceptable. Sensitive groups should limit prolonged outdoor exertion.',
  Unhealthy: 'Sensitive groups may experience health effects. General public may be less affected.',
  Hazardous: 'Health warning. Everyone may experience health effects. Minimize outdoor activities.',
};

export function AQIStatusCard({ category, confidence }: AQIStatusCardProps) {
  return (
    <Card className="overflow-hidden border-0 shadow-2xl h-full">
      <div className={`bg-gradient-to-br ${categoryColors[category]} p-6`}>
        <div className="space-y-5">
          {/* Header */}
          <div className="space-y-1.5">
            <h3 className="text-sm font-semibold text-white/80 tracking-wider">
              CURRENT AIR QUALITY STATUS
            </h3>
            <p className="text-5xl font-bold text-white tracking-tight">
              {category}
            </p>
          </div>

          {/* Description */}
          <p className="text-sm text-white/90 leading-relaxed max-w-2xl">
            {categoryDescriptions[category]}
          </p>

          {/* Divider */}
          <div className="h-px bg-white/20" />

          {/* Stats */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <p className="text-xs text-white/70 font-medium uppercase tracking-wide">Model Confidence</p>
              <p className="text-3xl font-bold text-white">
                {(confidence * 100).toFixed(0)}%
              </p>
            </div>
            <div className="space-y-1">
              <p className="text-xs text-white/70 font-medium uppercase tracking-wide">Classification Model</p>
              <p className="text-lg font-semibold text-white">
                Random Forest
              </p>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}
