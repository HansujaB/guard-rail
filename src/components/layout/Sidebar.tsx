import { cn } from "@/lib/utils";
import { Link, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  Train,
  AlertTriangle,
  Plane,
  FileText,
  BarChart3,
  Settings,
  Shield,
  Activity,
  Users,
  LogOut,
} from "lucide-react";

const navigationItems = [
  {
    title: "COMMAND",
    items: [
      { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
      { name: "Track Monitor", href: "/tracks", icon: Train },
      { name: "Alerts", href: "/alerts", icon: AlertTriangle, badge: 3 },
    ],
  },
  {
    title: "SURVEILLANCE",
    items: [
      { name: "Human Activity", href: "/activity", icon: Users },
      { name: "Drone Control", href: "/drones", icon: Plane },
      { name: "Intent Analysis", href: "/intent", icon: Activity },
    ],
  },
  {
    title: "REPORTS",
    items: [
      { name: "Incidents", href: "/incidents", icon: FileText },
      { name: "Analytics", href: "/analytics", icon: BarChart3 },
    ],
  },
  {
    title: "SYSTEM",
    items: [
      { name: "Configuration", href: "/config", icon: Settings },
    ],
  },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 bg-sidebar border-r border-sidebar-border flex flex-col">
      {/* Header */}
      <div className="h-16 flex items-center gap-3 px-4 border-b border-sidebar-border">
        <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
          <Shield className="w-6 h-6 text-primary-foreground" />
        </div>
        <div>
          <h1 className="text-sm font-bold text-sidebar-foreground tracking-wide">
            IRSS COMMAND
          </h1>
          <p className="text-[10px] text-muted-foreground uppercase tracking-widest">
            Railway Safety System
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto scrollbar-control py-4">
        {navigationItems.map((section) => (
          <div key={section.title} className="mb-6">
            <h2 className="px-4 mb-2 text-[10px] font-semibold text-muted-foreground uppercase tracking-widest">
              {section.title}
            </h2>
            <ul className="space-y-1 px-2">
              {section.items.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <li key={item.name}>
                    <Link
                      to={item.href}
                      className={cn(
                        "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-all duration-200",
                        isActive
                          ? "bg-sidebar-accent text-sidebar-primary"
                          : "text-sidebar-foreground/70 hover:text-sidebar-foreground hover:bg-sidebar-accent/50"
                      )}
                    >
                      <item.icon className={cn("w-4 h-4", isActive && "text-primary")} />
                      <span className="flex-1">{item.name}</span>
                      {item.badge && (
                        <span className="px-1.5 py-0.5 text-[10px] font-bold bg-status-critical text-white rounded-full min-w-[18px] text-center">
                          {item.badge}
                        </span>
                      )}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-sidebar-border">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
            <span className="text-xs font-bold text-primary">CR</span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-sidebar-foreground truncate">
              Control Room
            </p>
            <p className="text-[10px] text-muted-foreground truncate">
              NR Division • Delhi
            </p>
          </div>
        </div>
        <Link
          to="/"
          className="flex items-center gap-2 px-3 py-2 rounded-md text-sm text-muted-foreground hover:text-sidebar-foreground hover:bg-sidebar-accent/50 transition-colors"
        >
          <LogOut className="w-4 h-4" />
          <span>Sign Out</span>
        </Link>
      </div>
    </aside>
  );
}
