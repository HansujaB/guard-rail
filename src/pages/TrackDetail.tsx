import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { DataPanel } from "@/components/ui/DataPanel";
import { MetricCard } from "@/components/ui/MetricCard";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { IntentTimeline } from "@/components/dashboard/IntentTimeline";
import {
  Activity,
  Volume2,
  Thermometer,
  Gauge,
  AlertTriangle,
  Clock,
  MapPin,
  Train,
  ChevronLeft,
  Play,
  Pause,
  RefreshCw,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
} from "recharts";

// Generate mock sensor data
const generateSensorData = (points: number) => {
  return Array.from({ length: points }, (_, i) => ({
    time: `${22}:${String(i).padStart(2, "0")}`,
    vibration: 20 + Math.random() * 30 + (i > 15 && i < 25 ? 40 : 0),
    acoustic: 15 + Math.random() * 20 + (i > 18 && i < 23 ? 35 : 0),
    temperature: 28 + Math.random() * 5,
    pressure: 95 + Math.random() * 10,
  }));
};

const sensorData = generateSensorData(30);

// Intent breakdown data
const intentBreakdown = [
  { signal: "Human presence detected", contribution: 0.25, color: "bg-sensor-acoustic" },
  { signal: "Tool acoustics signature", contribution: 0.18, color: "bg-sensor-vibration" },
  { signal: "Night timing factor", contribution: 0.12, color: "bg-muted-foreground" },
  { signal: "Train proximity (23 min)", contribution: 0.21, color: "bg-accent" },
  { signal: "Weather exclusion", contribution: 0.04, color: "bg-status-info" },
];

export default function TrackDetail() {
  const navigate = useNavigate();
  const [isLive, setIsLive] = useState(true);
  const [selectedSensor, setSelectedSensor] = useState<"vibration" | "acoustic" | "temperature" | "pressure">("vibration");

  const totalIntent = intentBreakdown.reduce((sum, item) => sum + item.contribution, 0);

  return (
    <DashboardLayout>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate("/dashboard")}
            className="gap-2"
          >
            <ChevronLeft className="w-4 h-4" />
            Back
          </Button>
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-foreground">TS-004</h1>
              <StatusBadge status="critical" size="lg">
                HIGH RISK
              </StatusBadge>
            </div>
            <div className="flex items-center gap-4 mt-1 text-sm text-muted-foreground">
              <span className="flex items-center gap-1">
                <MapPin className="w-3 h-3" />
                KM 47.3, Ghaziabad-Meerut Section
              </span>
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" />
                Last update: 2s ago
              </span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant={isLive ? "default" : "outline"}
            size="sm"
            onClick={() => setIsLive(!isLive)}
            className="gap-2"
          >
            {isLive ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            {isLive ? "Pause" : "Resume"}
          </Button>
          <Button variant="outline" size="sm" className="gap-2">
            <RefreshCw className="w-4 h-4" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Sensor Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <MetricCard
          label="Vibration"
          value={68.4}
          unit="Hz"
          icon={Activity}
          status="critical"
          trend="up"
          trendValue="+45%"
        />
        <MetricCard
          label="Acoustic"
          value={52.1}
          unit="dB"
          icon={Volume2}
          status="warning"
          trend="up"
          trendValue="+28%"
        />
        <MetricCard
          label="Temperature"
          value={31.2}
          unit="°C"
          icon={Thermometer}
          status="safe"
        />
        <MetricCard
          label="Pressure"
          value={98.7}
          unit="kPa"
          icon={Gauge}
          status="safe"
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Sensor Charts */}
        <div className="xl:col-span-2 space-y-6">
          {/* Sensor Type Selector */}
          <div className="flex gap-2">
            {[
              { key: "vibration", label: "Vibration", color: "bg-sensor-vibration" },
              { key: "acoustic", label: "Acoustic", color: "bg-sensor-acoustic" },
              { key: "temperature", label: "Temperature", color: "bg-sensor-thermal" },
              { key: "pressure", label: "Pressure", color: "bg-sensor-pressure" },
            ].map((sensor) => (
              <button
                key={sensor.key}
                onClick={() => setSelectedSensor(sensor.key as typeof selectedSensor)}
                className={cn(
                  "px-4 py-2 rounded-lg text-sm font-medium transition-all",
                  selectedSensor === sensor.key
                    ? "bg-primary text-primary-foreground"
                    : "bg-secondary text-muted-foreground hover:text-foreground"
                )}
              >
                <span className={cn("inline-block w-2 h-2 rounded-full mr-2", sensor.color)} />
                {sensor.label}
              </button>
            ))}
          </div>

          {/* Main Chart */}
          <DataPanel
            title="Sensor Timeline"
            subtitle="Last 30 minutes • Anomalies highlighted"
            variant="elevated"
          >
            <div className="h-[300px] mt-4">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={sensorData}>
                  <defs>
                    <linearGradient id="colorVibration" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="hsl(var(--sensor-vibration))" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="hsl(var(--sensor-vibration))" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="colorAcoustic" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="hsl(var(--sensor-acoustic))" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="hsl(var(--sensor-acoustic))" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis
                    dataKey="time"
                    stroke="hsl(var(--muted-foreground))"
                    fontSize={10}
                    tickLine={false}
                  />
                  <YAxis
                    stroke="hsl(var(--muted-foreground))"
                    fontSize={10}
                    tickLine={false}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                      fontSize: "12px",
                    }}
                    labelStyle={{ color: "hsl(var(--foreground))" }}
                  />
                  <Area
                    type="monotone"
                    dataKey={selectedSensor}
                    stroke={`hsl(var(--sensor-${selectedSensor}))`}
                    fill={`url(#color${selectedSensor.charAt(0).toUpperCase() + selectedSensor.slice(1)})`}
                    strokeWidth={2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </DataPanel>

          {/* Train Proximity */}
          <DataPanel
            title="Train Proximity"
            variant="warning"
            action={
              <div className="flex items-center gap-2">
                <Train className="w-4 h-4 text-accent" />
                <span className="text-sm font-mono font-bold text-accent">12001 Shatabdi</span>
              </div>
            }
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-3xl font-bold font-mono text-foreground">23 min</p>
                <p className="text-sm text-muted-foreground">Estimated time to segment</p>
              </div>
              <div className="text-right">
                <p className="text-lg font-mono text-foreground">142 km/h</p>
                <p className="text-sm text-muted-foreground">Current speed</p>
              </div>
              <div className="w-32 h-2 bg-secondary rounded-full overflow-hidden">
                <div className="h-full bg-accent rounded-full w-3/4 animate-pulse" />
              </div>
            </div>
          </DataPanel>
        </div>

        {/* Intent Analysis */}
        <div className="space-y-6">
          {/* Intent Score */}
          <DataPanel
            title="Intent Analysis"
            subtitle="Explainable AI scoring"
            variant="danger"
          >
            <div className="space-y-4">
              {/* Total Score */}
              <div className="p-4 rounded-lg bg-status-critical/10 border border-status-critical/30">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-foreground">Final Intent Score</span>
                  <AlertTriangle className="w-5 h-5 text-status-critical" />
                </div>
                <div className="flex items-end gap-2">
                  <span className="text-4xl font-bold font-mono text-status-critical">
                    {(totalIntent * 100).toFixed(0)}%
                  </span>
                  <span className="text-sm text-status-critical mb-1">HIGH RISK</span>
                </div>
              </div>

              {/* Breakdown */}
              <div className="space-y-3">
                <p className="text-xs text-muted-foreground uppercase tracking-wider font-medium">
                  Signal Contributions
                </p>
                {intentBreakdown.map((item, index) => (
                  <div key={index} className="space-y-1">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">{item.signal}</span>
                      <span className="font-mono font-bold text-foreground">
                        +{(item.contribution * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="h-1.5 bg-secondary rounded-full overflow-hidden">
                      <div
                        className={cn("h-full rounded-full transition-all", item.color)}
                        style={{ width: `${(item.contribution / 0.3) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              {/* Explainability note */}
              <div className="p-3 rounded-lg bg-secondary border border-border">
                <p className="text-xs text-muted-foreground">
                  <strong className="text-foreground">Why this score?</strong> Combination of human presence, tool-like acoustic signatures, and proximity to scheduled train creates high-confidence sabotage pattern.
                </p>
              </div>
            </div>
          </DataPanel>

          {/* Event Timeline */}
          <DataPanel title="Event Timeline" subtitle="Chronological sequence">
            <IntentTimeline />
          </DataPanel>
        </div>
      </div>
    </DashboardLayout>
  );
}
