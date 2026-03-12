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
    <Card className="border-0 shadow-lg overflow-hidden">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div>
            <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">System Status</h3>
            <p className="text-xs text-slate-500 mt-2">{roomName} • {deviceId}</p>
          </div>
          <div className={`flex items-center gap-2 ${statusColor} px-3 py-1.5 rounded-full ${statusBg}`}>
            <div className={`h-2 w-2 rounded-full ${statusDot} animate-pulse`} />
            <span className="text-xs font-semibold">
              {backendAvailable ? 'Connected' : 'Offline'}
            </span>
          </div>
        </div>

        {/* Divider */}
        <div className="h-px bg-slate-700 mb-4" />

        {/* Status Items */}
        <div className="space-y-2">
          <div className="flex items-center justify-between p-3 rounded-lg bg-slate-700/20 hover:bg-slate-700/30 transition-colors">
            <span className="text-xs text-slate-400">Backend API</span>
            <span className={`text-xs font-semibold ${statusColor}`}>
              {backendAvailable ? 'Connected' : 'Offline'}
            </span>
          </div>

          <div className="flex items-center justify-between p-3 rounded-lg bg-slate-700/20 hover:bg-slate-700/30 transition-colors">
            <span className="text-xs text-slate-400">ML Models</span>
            <span className="text-xs font-semibold text-emerald-400">Ready</span>
          </div>

          <div className="flex items-center justify-between p-3 rounded-lg bg-slate-700/20 hover:bg-slate-700/30 transition-colors">
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
