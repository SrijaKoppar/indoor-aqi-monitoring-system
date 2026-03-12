'use client';

import { Card } from '@/components/ui/card';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface CategoryDistributionChartProps {
  data: {
    Good: { actual: number; predicted: number };
    Moderate: { actual: number; predicted: number };
    Unhealthy: { actual: number; predicted: number };
    Hazardous: { actual: number; predicted: number };
  };
}

export function CategoryDistributionChart({
  data,
}: CategoryDistributionChartProps) {
  const chartData = [
    {
      category: 'Good',
      actual: data.Good.actual,
      predicted: data.Good.predicted,
    },
    {
      category: 'Moderate',
      actual: data.Moderate.actual,
      predicted: data.Moderate.predicted,
    },
    {
      category: 'Unhealthy',
      actual: data.Unhealthy.actual,
      predicted: data.Unhealthy.predicted,
    },
    {
      category: 'Hazardous',
      actual: data.Hazardous.actual,
      predicted: data.Hazardous.predicted,
    },
  ];

  return (
    <Card className="border-0 shadow-lg">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-6">
        <h3 className="mb-4 text-sm font-semibold text-slate-300">
          AQI Category Distribution
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" />
            <XAxis
              dataKey="category"
              tick={{ fill: '#94a3b8', fontSize: 12 }}
              stroke="#475569"
            />
            <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} stroke="#475569" />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1e293b',
                border: '1px solid #334155',
                borderRadius: '8px',
              }}
            />
            <Legend wrapperStyle={{ paddingTop: '16px' }} />
            <Bar dataKey="actual" fill="#22c55e" name="Actual" radius={[8, 8, 0, 0]} />
            <Bar dataKey="predicted" fill="#10b981" name="Predicted" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
