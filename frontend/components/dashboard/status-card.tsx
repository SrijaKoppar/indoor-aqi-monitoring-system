import { Card } from '@/components/ui/card';
import { AQICategory } from '@/lib/types';

interface StatusCardProps {
  title: string;
  value: number;
  unit: string;
  category?: AQICategory;
  icon?: React.ReactNode;
}

const categoryColors: Record<AQICategory, string> = {
  Good: 'bg-green-500',
  Moderate: 'bg-yellow-400',
  Unhealthy: 'bg-orange-500',
  Hazardous: 'bg-red-600',
};

const categoryTextColors: Record<AQICategory, string> = {
  Good: 'text-green-600',
  Moderate: 'text-yellow-600',
  Unhealthy: 'text-orange-600',
  Hazardous: 'text-red-600',
};

export function StatusCard({
  title,
  value,
  unit,
  category,
  icon,
}: StatusCardProps) {
  return (
    <Card className="overflow-hidden border border-slate-700 shadow-lg hover:border-slate-600 hover:shadow-xl transition-all duration-300 h-full">
      <div className="bg-slate-900/50 backdrop-blur-sm p-5">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
              {title}
            </p>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-bold text-white">
                {value.toFixed(2)}
              </span>
              <span className="text-sm text-slate-400">{unit}</span>
            </div>
          </div>
          {icon && <div className="text-slate-400 opacity-60">{icon}</div>}
        </div>

        {category && (
          <div className="flex items-center gap-2 pt-3 border-t border-slate-700">
            <div
              className={`h-2 w-2 rounded-full ${categoryColors[category]}`}
            />
            <span
              className={`text-xs font-semibold ${categoryTextColors[category]}`}
            >
              {category}
            </span>
          </div>
        )}
      </div>
    </Card>
  );
}
