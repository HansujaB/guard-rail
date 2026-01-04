import { User, Wrench, Activity, AlertTriangle, Train, Clock } from "lucide-react";
import { cn } from "@/lib/utils";

interface TimelineEvent {
  id: string;
  time: string;
  type: "human" | "acoustic" | "vibration" | "alert" | "train";
  description: string;
  confidence?: number;
  intentContribution?: number;
}

const timelineEvents: TimelineEvent[] = [
  {
    id: "1",
    time: "22:11",
    type: "human",
    description: "Human detected near track",
    confidence: 0.92,
    intentContribution: 0.25,
  },
  {
    id: "2",
    time: "22:14",
    type: "human",
    description: "Repeated loitering (3 min duration)",
    confidence: 0.88,
    intentContribution: 0.15,
  },
  {
    id: "3",
    time: "22:19",
    type: "acoustic",
    description: "Tool-metal acoustic signature detected",
    confidence: 0.81,
    intentContribution: 0.18,
  },
  {
    id: "4",
    time: "22:22",
    type: "vibration",
    description: "Bolt vibration anomaly detected",
    confidence: 0.94,
    intentContribution: 0.22,
  },
  {
    id: "5",
    time: "22:45",
    type: "train",
    description: "Train 12001 ETA: 23 minutes",
    intentContribution: 0.12,
  },
];

const getEventIcon = (type: string) => {
  switch (type) {
    case "human":
      return User;
    case "acoustic":
      return Wrench;
    case "vibration":
      return Activity;
    case "alert":
      return AlertTriangle;
    case "train":
      return Train;
    default:
      return Clock;
  }
};

const getEventColor = (type: string) => {
  switch (type) {
    case "human":
      return "text-sensor-acoustic bg-sensor-acoustic/20 border-sensor-acoustic/30";
    case "acoustic":
      return "text-sensor-vibration bg-sensor-vibration/20 border-sensor-vibration/30";
    case "vibration":
      return "text-status-critical bg-status-critical/20 border-status-critical/30";
    case "train":
      return "text-accent bg-accent/20 border-accent/30";
    default:
      return "text-muted-foreground bg-muted border-border";
  }
};

export function IntentTimeline() {
  const totalIntent = timelineEvents.reduce(
    (sum, event) => sum + (event.intentContribution || 0),
    0
  );

  return (
    <div className="space-y-4">
      {/* Intent Score Summary */}
      <div className="flex items-center justify-between p-3 rounded-lg bg-status-critical/10 border border-status-critical/30">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-status-critical" />
          <span className="text-sm font-medium text-foreground">
            Cumulative Intent Score
          </span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-24 h-2 bg-secondary rounded-full overflow-hidden">
            <div
              className="h-full bg-status-critical rounded-full transition-all duration-500"
              style={{ width: `${Math.min(totalIntent * 100, 100)}%` }}
            />
          </div>
          <span className="text-lg font-bold font-mono text-status-critical">
            {(totalIntent * 100).toFixed(0)}%
          </span>
        </div>
      </div>

      {/* Timeline */}
      <div className="relative pl-6 space-y-0">
        {/* Timeline line */}
        <div className="absolute left-[11px] top-2 bottom-2 w-0.5 bg-border" />

        {timelineEvents.map((event, index) => {
          const Icon = getEventIcon(event.type);
          const colorClass = getEventColor(event.type);

          return (
            <div
              key={event.id}
              className="relative pb-4 last:pb-0 animate-fade-up"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Timeline dot */}
              <div
                className={cn(
                  "absolute -left-6 w-6 h-6 rounded-full border-2 flex items-center justify-center",
                  colorClass
                )}
              >
                <Icon className="w-3 h-3" />
              </div>

              {/* Event content */}
              <div className="ml-4 p-3 rounded-lg bg-card border border-border hover:border-primary/30 transition-colors">
                <div className="flex items-start justify-between mb-1">
                  <span className="font-mono text-xs text-primary font-bold">
                    {event.time}
                  </span>
                  {event.confidence && (
                    <span className="text-[10px] text-muted-foreground">
                      Confidence: {(event.confidence * 100).toFixed(0)}%
                    </span>
                  )}
                </div>
                <p className="text-sm text-foreground">{event.description}</p>
                {event.intentContribution && (
                  <div className="flex items-center gap-2 mt-2">
                    <span className="text-[10px] text-muted-foreground">
                      Intent contribution:
                    </span>
                    <span className="text-xs font-mono font-bold text-status-warning">
                      +{(event.intentContribution * 100).toFixed(0)}%
                    </span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
