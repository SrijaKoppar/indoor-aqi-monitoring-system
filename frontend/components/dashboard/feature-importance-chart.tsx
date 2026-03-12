'use client';

import { Card } from '@/components/ui/card';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { FeatureImportance } from '@/lib/types';

interface FeatureImportanceChartProps {
  data: FeatureImportance[];
}

export function FeatureImportanceChart({ data }: FeatureImportanceChartProps) {
  const chartData = data.slice(0, 10).map((d) => ({
    name: d.feature.replace(/_/g, ' '),
    importance: parseFloat((d.importance * 100).toFixed(2)),
  }));

  return (
    <Card className="border-0 shadow-lg">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-6">
        <h3 className="mb-4 text-sm font-semibold text-slate-300">
          Top 10 Feature Importances (XGBoost)
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={chartData}
            margin={{ top: 20, right: 20, bottom: 60, left: 20 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" />
            <XAxis
              dataKey="name"
              tick={{ fill: '#94a3b8', fontSize: 11 }}
              angle={-45}
              textAnchor="end"
              height={100}
              stroke="#475569"
            />
            <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} stroke="#475569" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #334155',
                borderRadius: '8px',
              }}
              formatter={(value) => `${value}%`}
            />
            <Bar dataKey="importance" fill="#06b6d4" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
