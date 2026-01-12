import { AlertTriangle } from "lucide-react";
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

// Mock data matching backend API structure
const mockAnalysis: BackendResponse = {
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
};

export function IntentTimeline() {
  const { intent_score, individual_scores } = mockAnalysis;

  const scoreConfigs = [
    {
      label: "Vibration Anomaly",
      value: individual_scores.vibration_anomaly,
      color: "bg-status-warning text-status-warning",
    },
    {
      label: "Acoustic Tool",
      value: individual_scores.acoustic_tool,
      color: "bg-status-warning text-status-warning",
    },
    {
      label: "Human Presence",
      value: individual_scores.human_presence,
      color: "bg-status-critical text-status-critical",
    },
    {
      label: "Temporal Unplanned",
      value: individual_scores.temporal_unplanned,
      color: "bg-muted-foreground text-muted-foreground",
    },
    {
      label: "Context",
      value: individual_scores.context,
      color: "bg-status-safe text-status-safe",
    },
  ];

  return (
    <div className="space-y-4">
      {/* Intent Score Summary */}
      <div className="flex items-center justify-between p-3 rounded-lg bg-status-critical/10 border border-status-critical/30">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-status-critical" />
          <span className="text-sm font-medium text-foreground">
            Intent Score
          </span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-24 h-2 bg-secondary rounded-full overflow-hidden">
            <div
              className="h-full bg-status-critical rounded-full transition-all duration-500"
              style={{ width: `${Math.min(intent_score * 100, 100)}%` }}
            />
          </div>
          <span className="text-lg font-bold font-mono text-status-critical">
            {(intent_score * 100).toFixed(0)}%
          </span>
        </div>
      </div>

      {/* Individual Scores */}
      <div className="space-y-2">
        {scoreConfigs.map((config) => (
          <div key={config.label} className="p-3 rounded-lg bg-card border border-border">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium text-foreground">
                {config.label}
              </span>
              <span
                className={cn(
                  "text-xs font-mono font-bold",
                  config.color.split(" ")[1]
                )}
              >
                {(config.value * 100).toFixed(0)}%
              </span>
            </div>
            <div className="w-full h-1.5 bg-secondary rounded-full overflow-hidden">
              <div
                className={cn("h-full rounded-full", config.color.split(" ")[0])}
                style={{ width: `${config.value * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
