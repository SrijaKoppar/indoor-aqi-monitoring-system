import { Card } from '@/components/ui/card';

interface SystemStatusProps {
  backendAvailable: boolean;
  lastUpdate: Date;
  roomName?: string;
  deviceId?: string;
}

export function SystemStatus({
  backendAvailable,
  lastUpdate,
  roomName = 'Living Room',
  deviceId = 'AQI-01',
}: SystemStatusProps) {
  const statusColor = backendAvailable ? 'text-emerald-400' : 'text-rose-400';
  const statusDot = backendAvailable ? 'bg-emerald-400' : 'bg-rose-400';
  const statusBg = backendAvailable ? 'bg-emerald-500/10' : 'bg-rose-500/10';

  return (
    <Card className="border-0 shadow-lg overflow-hidden h-full">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-5">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">System Status</h3>
            <p className="text-xs text-slate-500 mt-1.5">{roomName} • {deviceId}</p>
          </div>
          <div className={`flex items-center gap-2 ${statusColor} px-2.5 py-1 rounded-full text-xs font-semibold ${statusBg}`}>
            <div className={`h-1.5 w-1.5 rounded-full ${statusDot} animate-pulse`} />
            {backendAvailable ? 'Connected' : 'Offline'}
          </div>
        </div>

        {/* Divider */}
        <div className="h-px bg-slate-700 mb-3.5" />

        {/* Status Items */}
        <div className="space-y-2">
          <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-700/20 hover:bg-slate-700/30 transition-colors">
            <span className="text-xs text-slate-400">Backend API</span>
            <span className={`text-xs font-semibold ${statusColor}`}>
              {backendAvailable ? 'Connected' : 'Offline'}
            </span>
          </div>

          <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-700/20 hover:bg-slate-700/30 transition-colors">
            <span className="text-xs text-slate-400">ML Models</span>
            <span className="text-xs font-semibold text-emerald-400">Ready</span>
          </div>

          <div className="flex items-center justify-between p-2.5 rounded-lg bg-slate-700/20 hover:bg-slate-700/30 transition-colors">
            <span className="text-xs text-slate-400">Last Update</span>
            <span className="text-xs font-semibold text-cyan-400">
              {lastUpdate.toLocaleTimeString()}
            </span>
          </div>
        </div>
      </div>
    </Card>
  );
}
