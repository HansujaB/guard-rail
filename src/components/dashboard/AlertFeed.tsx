import { AlertTriangle, MapPin, Clock, User, Wrench, ChevronRight } from "lucide-react";
import { StatusBadge } from "../ui/StatusBadge";
import { cn } from "@/lib/utils";

interface Alert {
  id: string;
  type: "intrusion" | "tampering" | "anomaly" | "surveillance";
  severity: "critical" | "warning" | "info";
  trackId: string;
  location: string;
  message: string;
  timestamp: string;
  intentScore?: number;
}

const mockAlerts: Alert[] = [
  {
    id: "ALT-001",
    type: "intrusion",
    severity: "critical",
    trackId: "TS-004",
    location: "KM 47.3, Ghaziabad-Meerut",
    message: "Human presence detected with tool-like acoustic signature",
    timestamp: "22:19:45",
    intentScore: 0.82,
  },
  {
    id: "ALT-002",
    type: "tampering",
    severity: "critical",
    trackId: "TS-004",
    location: "KM 47.3, Ghaziabad-Meerut",
    message: "Bolt vibration anomaly detected - possible loosening attempt",
    timestamp: "22:22:12",
    intentScore: 0.91,
  },
  {
    id: "ALT-003",
    type: "surveillance",
    severity: "warning",
    trackId: "TS-003",
    location: "Ghaziabad Junction",
    message: "Repeated loitering pattern detected (3+ minutes)",
    timestamp: "22:14:33",
    intentScore: 0.45,
  },
  {
    id: "ALT-004",
    type: "anomaly",
    severity: "warning",
    trackId: "TS-008",
    location: "KM 12.8, Delhi-Rohtak",
    message: "Unusual vibration pattern - weather excluded",
    timestamp: "22:08:17",
    intentScore: 0.38,
  },
];

export function AlertFeed() {
  return (
    <div className="space-y-3">
      {mockAlerts.map((alert, index) => (
        <div
          key={alert.id}
          className={cn(
            "group relative p-4 rounded-lg border transition-all duration-300 cursor-pointer",
            "animate-slide-in-right",
            alert.severity === "critical" && "bg-status-critical/5 border-status-critical/30 hover:border-status-critical/60",
            alert.severity === "warning" && "bg-status-warning/5 border-status-warning/30 hover:border-status-warning/60",
            alert.severity === "info" && "bg-card border-border hover:border-primary/50"
          )}
          style={{ animationDelay: `${index * 100}ms` }}
        >
          {/* Severity indicator line */}
          <div
            className={cn(
              "absolute left-0 top-0 bottom-0 w-1 rounded-l-lg",
              alert.severity === "critical" && "bg-status-critical",
              alert.severity === "warning" && "bg-status-warning",
              alert.severity === "info" && "bg-status-info"
            )}
          />

          {/* Header */}
          <div className="flex items-start justify-between mb-2">
            <div className="flex items-center gap-2">
              <AlertTriangle
                className={cn(
                  "w-4 h-4",
                  alert.severity === "critical" && "text-status-critical",
                  alert.severity === "warning" && "text-status-warning"
                )}
              />
              <span className="text-xs font-mono text-muted-foreground">{alert.id}</span>
              <StatusBadge
                status={alert.severity === "critical" ? "critical" : alert.severity === "warning" ? "warning" : "info"}
                size="sm"
              >
                {alert.severity}
              </StatusBadge>
            </div>
            <div className="flex items-center gap-1 text-[10px] text-muted-foreground">
              <Clock className="w-3 h-3" />
              {alert.timestamp}
            </div>
          </div>

          {/* Message */}
          <p className="text-sm text-foreground mb-3">{alert.message}</p>

          {/* Details */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4 text-[10px] text-muted-foreground">
              <div className="flex items-center gap-1">
                <MapPin className="w-3 h-3" />
                {alert.location}
              </div>
              <div className="flex items-center gap-1">
                <span className="font-mono font-bold text-foreground">{alert.trackId}</span>
              </div>
            </div>

            {/* Intent Score */}
            {alert.intentScore && (
              <div className="flex items-center gap-2">
                <span className="text-[10px] text-muted-foreground">Intent:</span>
                <div className="flex items-center gap-1">
                  <div className="w-16 h-1.5 bg-secondary rounded-full overflow-hidden">
                    <div
                      className={cn(
                        "h-full rounded-full transition-all",
                        alert.intentScore >= 0.7 && "bg-status-critical",
                        alert.intentScore >= 0.4 && alert.intentScore < 0.7 && "bg-status-warning",
                        alert.intentScore < 0.4 && "bg-status-safe"
                      )}
                      style={{ width: `${alert.intentScore * 100}%` }}
                    />
                  </div>
                  <span
                    className={cn(
                      "text-xs font-mono font-bold",
                      alert.intentScore >= 0.7 && "text-status-critical",
                      alert.intentScore >= 0.4 && alert.intentScore < 0.7 && "text-status-warning",
                      alert.intentScore < 0.4 && "text-status-safe"
                    )}
                  >
                    {(alert.intentScore * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Hover action */}
          <ChevronRight className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
        </div>
      ))}
    </div>
  );
}
