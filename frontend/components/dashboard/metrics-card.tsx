import { Card } from '@/components/ui/card';

interface MetricsCardProps {
  title: string;
  metrics: Array<{
    label: string;
    value: number | string;
    suffix?: string;
  }>;
}

export function MetricsCard({ title, metrics }: MetricsCardProps) {
  return (
    <Card className="border-0 shadow-lg overflow-hidden h-full">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-5">
        <h3 className="mb-3 text-sm font-semibold text-slate-300 uppercase tracking-wider">
          {title}
        </h3>
        
        <div className="h-px bg-slate-700 mb-4" />

        <div className="space-y-2">
          {metrics.map((metric, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between p-2.5 rounded-lg bg-slate-700/20 hover:bg-slate-700/30 transition-colors"
            >
              <span className="text-xs text-slate-400 uppercase tracking-wider">
                {metric.label}
              </span>
              <div className="text-right">
                <span className="font-semibold text-cyan-400 text-sm">
                  {metric.value}
                </span>
                {metric.suffix && (
                  <span className="ml-1 text-slate-400 text-xs">{metric.suffix}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}
