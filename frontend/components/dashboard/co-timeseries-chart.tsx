'use client';

import { Card } from '@/components/ui/card';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { HistoricalData } from '@/lib/types';

interface COTimeSeriesChartProps {
  data: HistoricalData[];
}

export function COTimeSeriesChart({ data }: COTimeSeriesChartProps) {
  const chartData = data.slice(-50).map((d) => ({
    time: d.timestamp.getHours() + ':' + String(d.timestamp.getMinutes()).padStart(2, '0'),
    actual: parseFloat(d.actual.toFixed(2)),
    predicted: parseFloat(d.predicted.toFixed(2)),
  }));

  return (
    <Card className="border-0 shadow-lg">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-6">
        <h3 className="mb-4 text-sm font-semibold text-slate-300">
          CO Concentration (Next 50 Hours)
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" />
            <XAxis
              dataKey="time"
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
              labelStyle={{ color: '#94a3b8' }}
              formatter={(value) => parseFloat(String(value)).toFixed(2)}
            />
            <Legend wrapperStyle={{ paddingTop: '16px' }} />
            <Line
              type="monotone"
              dataKey="actual"
              stroke="#3b82f6"
              dot={false}
              strokeWidth={2}
              name="Actual CO"
            />
            <Line
              type="monotone"
              dataKey="predicted"
              stroke="#06b6d4"
              dot={false}
              strokeWidth={2}
              strokeDasharray="5 5"
              name="Predicted CO"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
