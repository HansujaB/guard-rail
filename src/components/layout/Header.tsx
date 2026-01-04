import { Bell, Search, Clock, Wifi } from "lucide-react";
import { StatusBadge } from "../ui/StatusBadge";
import { useState, useEffect } from "react";

export function Header() {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="h-16 bg-card border-b border-border flex items-center justify-between px-6">
      {/* Search */}
      <div className="flex items-center gap-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search tracks, alerts, incidents..."
            className="w-80 h-9 pl-9 pr-4 rounded-md bg-secondary border border-border text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
          />
        </div>
      </div>

      {/* Status & Actions */}
      <div className="flex items-center gap-6">
        {/* System Status */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Wifi className="w-4 h-4 text-status-safe" />
            <span className="text-xs font-medium text-muted-foreground">
              All Systems Online
            </span>
          </div>
          <StatusBadge status="safe" size="sm">LIVE</StatusBadge>
        </div>

        {/* Time */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-secondary">
          <Clock className="w-4 h-4 text-muted-foreground" />
          <span className="font-mono text-sm text-foreground">
            {currentTime.toLocaleTimeString("en-IN", { hour12: false })}
          </span>
          <span className="text-xs text-muted-foreground">IST</span>
        </div>

        {/* Notifications */}
        <button className="relative p-2 rounded-md hover:bg-secondary transition-colors">
          <Bell className="w-5 h-5 text-muted-foreground" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-status-critical rounded-full status-pulse-critical" />
        </button>
      </div>
    </header>
  );
}
