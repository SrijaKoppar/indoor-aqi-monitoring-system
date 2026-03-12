'use client';

import { Card } from '@/components/ui/card';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Line,
  ResponsiveContainer,
} from 'recharts';
import { HistoricalData } from '@/lib/types';

interface ScatterPlotChartProps {
  data: HistoricalData[];
}

export function ScatterPlotChart({ data }: ScatterPlotChartProps) {
  const chartData = data.map((d) => ({
    actual: parseFloat(d.actual.toFixed(2)),
    predicted: parseFloat(d.predicted.toFixed(2)),
  }));

  // Generate perfect prediction line
  const minVal = Math.min(...data.map((d) => Math.min(d.actual, d.predicted))) - 0.5;
  const maxVal = Math.max(...data.map((d) => Math.max(d.actual, d.predicted))) + 0.5;

  return (
    <Card className="border-0 shadow-lg">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-6">
        <h3 className="mb-4 text-sm font-semibold text-slate-300">
          Actual vs Predicted CO
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" />
            <XAxis
              type="number"
              dataKey="actual"
              name="Actual CO"
              tick={{ fill: '#94a3b8', fontSize: 12 }}
              stroke="#475569"
              domain={[Math.max(0, minVal), maxVal]}
            />
            <YAxis
              type="number"
              dataKey="predicted"
              name="Predicted CO"
              tick={{ fill: '#94a3b8', fontSize: 12 }}
              stroke="#475569"
              domain={[Math.max(0, minVal), maxVal]}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #334155',
                borderRadius: '8px',
              }}
              cursor={{ fill: 'rgba(6, 182, 212, 0.1)' }}
              formatter={(value) => parseFloat(String(value)).toFixed(2)}
            />
            <Scatter
              name="Predictions"
              data={chartData}
              fill="#0ea5e9"
              fillOpacity={0.6}
            />
            <Line
              type="linear"
              dataKey="actual"
              stroke="#ef4444"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={false}
              name="Perfect Prediction"
              data={[
                { actual: minVal, predicted: minVal },
                { actual: maxVal, predicted: maxVal },
              ]}
            />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
