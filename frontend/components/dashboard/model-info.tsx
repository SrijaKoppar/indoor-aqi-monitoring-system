import { Card } from '@/components/ui/card';

export function ModelInfo() {
  return (
    <Card className="border-0 shadow-lg">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-6">
        <h3 className="mb-4 text-sm font-semibold text-slate-300">
          Model Information
        </h3>

        <div className="space-y-4">
          <div className="rounded-lg bg-black/20 p-4">
            <p className="text-xs text-slate-500 mb-1">Model Type</p>
            <p className="font-semibold text-white">XGBoost Regressor</p>
            <p className="text-xs text-slate-400 mt-1">Gradient boosting framework for CO prediction</p>
          </div>

          <div className="rounded-lg bg-black/20 p-4">
            <p className="text-xs text-slate-500 mb-1">Training Data</p>
            <p className="font-semibold text-white">Air Quality UCI Dataset</p>
            <p className="text-xs text-slate-400 mt-1">~9,000+ historical samples</p>
          </div>

          <div className="rounded-lg bg-black/20 p-4">
            <p className="text-xs text-slate-500 mb-1">Key Features</p>
            <ul className="text-xs text-slate-300 mt-2 space-y-1">
              <li>• CO(GT)_lag1 (23% importance)</li>
              <li>• Hour of day (14% importance)</li>
              <li>• 3-hour rolling average (9% importance)</li>
              <li>• 13 total input features</li>
            </ul>
          </div>

          <div className="rounded-lg bg-black/20 p-4">
            <p className="text-xs text-slate-500 mb-1">Prediction Target</p>
            <p className="font-semibold text-white">Next-Hour CO (mg/m³)</p>
            <p className="text-xs text-slate-400 mt-1">Continuous regression task</p>
          </div>
        </div>
      </div>
    </Card>
  );
}
