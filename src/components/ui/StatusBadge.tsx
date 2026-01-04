import { cn } from "@/lib/utils";
import { cva, type VariantProps } from "class-variance-authority";

const statusBadgeVariants = cva(
  "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium font-mono uppercase tracking-wider transition-all",
  {
    variants: {
      status: {
        safe: "bg-status-safe/20 text-status-safe border border-status-safe/30 status-pulse-safe",
        warning: "bg-status-warning/20 text-status-warning border border-status-warning/30 status-pulse-warning",
        critical: "bg-status-critical/20 text-status-critical border border-status-critical/30 status-pulse-critical",
        info: "bg-status-info/20 text-status-info border border-status-info/30",
        neutral: "bg-muted text-muted-foreground border border-border",
      },
      size: {
        sm: "text-[10px] px-2 py-0.5",
        md: "text-xs px-2.5 py-1",
        lg: "text-sm px-3 py-1.5",
      },
    },
    defaultVariants: {
      status: "neutral",
      size: "md",
    },
  }
);

interface StatusBadgeProps extends VariantProps<typeof statusBadgeVariants> {
  children: React.ReactNode;
  className?: string;
  showDot?: boolean;
}

export function StatusBadge({ 
  status, 
  size, 
  children, 
  className,
  showDot = true 
}: StatusBadgeProps) {
  return (
    <span className={cn(statusBadgeVariants({ status, size }), className)}>
      {showDot && (
        <span 
          className={cn(
            "w-1.5 h-1.5 rounded-full",
            status === "safe" && "bg-status-safe",
            status === "warning" && "bg-status-warning",
            status === "critical" && "bg-status-critical",
            status === "info" && "bg-status-info",
            status === "neutral" && "bg-muted-foreground"
          )}
        />
      )}
      {children}
    </span>
  );
}
