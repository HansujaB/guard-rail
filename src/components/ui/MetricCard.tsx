import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  label: string;
  value: string | number;
  unit?: string;
  icon?: LucideIcon;
  trend?: "up" | "down" | "neutral";
  trendValue?: string;
  status?: "safe" | "warning" | "critical" | "info";
  className?: string;
}

export function MetricCard({
  label,
  value,
  unit,
  icon: Icon,
  trend,
  trendValue,
  status,
  className,
}: MetricCardProps) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-lg border bg-card p-4 transition-all duration-300 hover:border-primary/50",
        status === "critical" && "border-status-critical/50 bg-status-critical/5",
        status === "warning" && "border-status-warning/50 bg-status-warning/5",
        status === "safe" && "border-status-safe/50 bg-status-safe/5",
        className
      )}
    >
      {/* Background glow effect */}
      {status && (
        <div
          className={cn(
            "absolute -top-1/2 -right-1/2 w-full h-full rounded-full blur-3xl opacity-10",
            status === "critical" && "bg-status-critical",
            status === "warning" && "bg-status-warning",
            status === "safe" && "bg-status-safe"
          )}
        />
      )}

      <div className="relative flex items-start justify-between">
        <div className="space-y-1">
          <p className="text-xs text-muted-foreground uppercase tracking-wider font-medium">
            {label}
          </p>
          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-bold font-mono text-foreground">
              {value}
            </span>
            {unit && (
              <span className="text-sm text-muted-foreground">{unit}</span>
            )}
          </div>
          {trend && trendValue && (
            <div
              className={cn(
                "flex items-center gap-1 text-xs font-medium",
                trend === "up" && "text-status-safe",
                trend === "down" && "text-status-critical",
                trend === "neutral" && "text-muted-foreground"
              )}
            >
              <span>
                {trend === "up" && "↑"}
                {trend === "down" && "↓"}
                {trend === "neutral" && "→"}
              </span>
              {trendValue}
            </div>
          )}
        </div>
        {Icon && (
          <div
            className={cn(
              "p-2 rounded-lg",
              status === "critical" && "bg-status-critical/20 text-status-critical",
              status === "warning" && "bg-status-warning/20 text-status-warning",
              status === "safe" && "bg-status-safe/20 text-status-safe",
              !status && "bg-primary/20 text-primary"
            )}
          >
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
    </div>
  );
}
