import { cn } from "@/lib/utils";
import { cva, type VariantProps } from "class-variance-authority";

const dataPanelVariants = cva(
  "rounded-lg border transition-all duration-300",
  {
    variants: {
      variant: {
        default: "bg-card border-border",
        glass: "glass-panel",
        elevated: "bg-card border-border shadow-lg",
        glow: "bg-card border-primary/30 glow-border",
        danger: "bg-card border-status-critical/30 shadow-[0_0_20px_hsl(var(--status-critical)/0.2)]",
        warning: "bg-card border-status-warning/30 shadow-[0_0_20px_hsl(var(--status-warning)/0.2)]",
      },
      padding: {
        none: "p-0",
        sm: "p-3",
        md: "p-4",
        lg: "p-6",
      },
    },
    defaultVariants: {
      variant: "default",
      padding: "md",
    },
  }
);

interface DataPanelProps extends VariantProps<typeof dataPanelVariants> {
  children: React.ReactNode;
  className?: string;
  title?: string;
  subtitle?: string;
  action?: React.ReactNode;
}

export function DataPanel({ 
  variant, 
  padding, 
  children, 
  className,
  title,
  subtitle,
  action
}: DataPanelProps) {
  return (
    <div className={cn(dataPanelVariants({ variant, padding }), className)}>
      {(title || action) && (
        <div className="flex items-center justify-between mb-4">
          <div>
            {title && (
              <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider">
                {title}
              </h3>
            )}
            {subtitle && (
              <p className="text-xs text-muted-foreground mt-0.5">{subtitle}</p>
            )}
          </div>
          {action}
        </div>
      )}
      {children}
    </div>
  );
}
