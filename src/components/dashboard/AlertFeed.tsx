import { AlertTriangle, MapPin, Clock, ChevronRight } from "lucide-react";
import { StatusBadge } from "../ui/StatusBadge";
import { cn } from "@/lib/utils";

// Backend API response structure
interface BackendResponse {
  intent_score: number;
  individual_scores: {
    vibration_anomaly: number;
    acoustic_tool: number;
    human_presence: number;
    temporal_unplanned: number;
    context: number;
  };
  reasons: string[];
  alert_triggered: boolean;
  alert?: {
    alert_id: string;
    risk: "high" | "medium";
    intent_score: number;
    reason: string[];
  };
}

// Extended interface for display (includes metadata)
interface AlertData extends BackendResponse {
  timestamp: string;
  trackId?: string;
  location?: string;
}

// Mock data matching backend API structure
const mockAlerts: AlertData[] = [
  {
    intent_score: 0.82,
    individual_scores: {
      vibration_anomaly: 0.75,
      acoustic_tool: 0.68,
      human_presence: 0.92,
      temporal_unplanned: 0.45,
      context: 1.0,
    },
    reasons: [
      "Human presence detected (score: 0.92)",
      "Tool-like acoustic pattern (score: 0.68)",
      "Abnormal vibration (score: 0.75)",
    ],
    alert_triggered: true,
    alert: {
      alert_id: "ALT-221",
      risk: "high",
      intent_score: 0.82,
      reason: [
        "Human presence detected (score: 0.92)",
        "Tool-like acoustic pattern (score: 0.68)",
        "Abnormal vibration (score: 0.75)",
      ],
    },
    timestamp: "22:19:45",
    trackId: "TS-004",
    location: "KM 47.3, Ghaziabad-Meerut",
  },
  {
    intent_score: 0.91,
    individual_scores: {
      vibration_anomaly: 0.94,
      acoustic_tool: 0.52,
      human_presence: 0.88,
      temporal_unplanned: 0.38,
      context: 1.0,
    },
    reasons: [
      "Abnormal vibration (score: 0.94)",
      "Human presence detected (score: 0.88)",
    ],
    alert_triggered: true,
    alert: {
      alert_id: "ALT-222",
      risk: "high",
      intent_score: 0.91,
      reason: [
        "Abnormal vibration (score: 0.94)",
        "Human presence detected (score: 0.88)",
      ],
    },
    timestamp: "22:22:12",
    trackId: "TS-004",
    location: "KM 47.3, Ghaziabad-Meerut",
  },
  {
    intent_score: 0.45,
    individual_scores: {
      vibration_anomaly: 0.35,
      acoustic_tool: 0.28,
      human_presence: 0.88,
      temporal_unplanned: 0.42,
      context: 1.0,
    },
    reasons: ["Human presence detected (score: 0.88)"],
    alert_triggered: false,
    timestamp: "22:14:33",
    trackId: "TS-003",
    location: "Ghaziabad Junction",
  },
  {
    intent_score: 0.38,
    individual_scores: {
      vibration_anomaly: 0.42,
      acoustic_tool: 0.31,
      human_presence: 0.15,
      temporal_unplanned: 0.35,
      context: 1.0,
    },
    reasons: [],
    alert_triggered: false,
    timestamp: "22:08:17",
    trackId: "TS-008",
    location: "KM 12.8, Delhi-Rohtak",
  },
];

export function AlertFeed() {
  // Filter to show only triggered alerts
  const triggeredAlerts = mockAlerts.filter((alert) => alert.alert_triggered);

  return (
    <div className="space-y-3">
      {triggeredAlerts.map((alert, index) => (
        <div
          key={alert.alert?.alert_id || `alert-${index}`}
          className={cn(
            "group relative p-4 rounded-lg border transition-all duration-300 cursor-pointer",
            "animate-slide-in-right",
            alert.alert?.risk === "high" &&
              "bg-status-critical/5 border-status-critical/30 hover:border-status-critical/60",
            alert.alert?.risk === "medium" &&
              "bg-status-warning/5 border-status-warning/30 hover:border-status-warning/60",
            !alert.alert && "bg-card border-border hover:border-primary/50"
          )}
          style={{ animationDelay: `${index * 100}ms` }}
        >
          {/* Severity indicator line */}
          <div
            className={cn(
              "absolute left-0 top-0 bottom-0 w-1 rounded-l-lg",
              alert.alert?.risk === "high" && "bg-status-critical",
              alert.alert?.risk === "medium" && "bg-status-warning",
              !alert.alert && "bg-status-info"
            )}
          />

          {/* Header */}
          <div className="flex items-start justify-between mb-2">
            <div className="flex items-center gap-2">
              <AlertTriangle
                className={cn(
                  "w-4 h-4",
                  alert.alert?.risk === "high" && "text-status-critical",
                  alert.alert?.risk === "medium" && "text-status-warning"
                )}
              />
              <span className="text-xs font-mono text-muted-foreground">
                {alert.alert?.alert_id || "N/A"}
              </span>
              {alert.alert && (
                <StatusBadge
                  status={
                    alert.alert.risk === "high" ? "critical" : "warning"
                  }
                  size="sm"
                >
                  {alert.alert.risk}
                </StatusBadge>
              )}
            </div>
            <div className="flex items-center gap-1 text-[10px] text-muted-foreground">
              <Clock className="w-3 h-3" />
              {alert.timestamp}
            </div>
          </div>

          {/* Reasons/Messages */}
          <div className="space-y-1 mb-3">
            {alert.reasons.length > 0 ? (
              alert.reasons.map((reason, idx) => (
                <p key={idx} className="text-sm text-foreground">
                  {reason}
                </p>
              ))
            ) : (
              <p className="text-sm text-muted-foreground">No significant threats detected</p>
            )}
          </div>

          {/* Details */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4 text-[10px] text-muted-foreground">
              {alert.location && (
                <div className="flex items-center gap-1">
                  <MapPin className="w-3 h-3" />
                  {alert.location}
                </div>
              )}
              {alert.trackId && (
                <div className="flex items-center gap-1">
                  <span className="font-mono font-bold text-foreground">
                    {alert.trackId}
                  </span>
                </div>
              )}
            </div>

            {/* Intent Score */}
            <div className="flex items-center gap-2">
              <span className="text-[10px] text-muted-foreground">Intent:</span>
              <div className="flex items-center gap-1">
                <div className="w-16 h-1.5 bg-secondary rounded-full overflow-hidden">
                  <div
                    className={cn(
                      "h-full rounded-full transition-all",
                      alert.intent_score >= 0.7 && "bg-status-critical",
                      alert.intent_score >= 0.4 &&
                        alert.intent_score < 0.7 &&
                        "bg-status-warning",
                      alert.intent_score < 0.4 && "bg-status-safe"
                    )}
                    style={{ width: `${alert.intent_score * 100}%` }}
                  />
                </div>
                <span
                  className={cn(
                    "text-xs font-mono font-bold",
                    alert.intent_score >= 0.7 && "text-status-critical",
                    alert.intent_score >= 0.4 &&
                      alert.intent_score < 0.7 &&
                      "text-status-warning",
                    alert.intent_score < 0.4 && "text-status-safe"
                  )}
                >
                  {(alert.intent_score * 100).toFixed(0)}%
                </span>
              </div>
            </div>
          </div>

          {/* Hover action */}
          <ChevronRight className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
        </div>
      ))}
    </div>
  );
}
