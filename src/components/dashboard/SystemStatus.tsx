import { Activity, Cpu, Database, Radio, Wifi, HardDrive } from "lucide-react";
import { cn } from "@/lib/utils";

interface SystemMetric {
  name: string;
  icon: React.ElementType;
  value: number;
  unit: string;
  status: "healthy" | "warning" | "critical";
}

const systemMetrics: SystemMetric[] = [
  { name: "Sensors Online", icon: Radio, value: 847, unit: "/ 856", status: "healthy" },
  { name: "Edge Nodes", icon: Cpu, value: 98.7, unit: "%", status: "healthy" },
  { name: "Data Pipeline", icon: Activity, value: 12.4, unit: "k/s", status: "healthy" },
  { name: "Database", icon: Database, value: 99.9, unit: "% up", status: "healthy" },
  { name: "Network", icon: Wifi, value: 24, unit: "ms", status: "healthy" },
  { name: "Storage", icon: HardDrive, value: 67, unit: "%", status: "warning" },
];

export function SystemStatus() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
      {systemMetrics.map((metric) => (
        <div
          key={metric.name}
          className={cn(
            "p-3 rounded-lg border transition-all",
            metric.status === "healthy" && "bg-card border-border hover:border-status-safe/50",
            metric.status === "warning" && "bg-status-warning/5 border-status-warning/30",
            metric.status === "critical" && "bg-status-critical/5 border-status-critical/30"
          )}
        >
          <div className="flex items-center gap-2 mb-2">
            <metric.icon
              className={cn(
                "w-4 h-4",
                metric.status === "healthy" && "text-status-safe",
                metric.status === "warning" && "text-status-warning",
                metric.status === "critical" && "text-status-critical"
              )}
            />
            <span className="text-[10px] text-muted-foreground uppercase tracking-wider truncate">
              {metric.name}
            </span>
          </div>
          <div className="flex items-baseline gap-1">
            <span className="text-lg font-bold font-mono text-foreground">
              {metric.value}
            </span>
            <span className="text-xs text-muted-foreground">{metric.unit}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
