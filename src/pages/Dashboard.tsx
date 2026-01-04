import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { DataPanel } from "@/components/ui/DataPanel";
import { MetricCard } from "@/components/ui/MetricCard";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { RailwayMap } from "@/components/dashboard/RailwayMap";
import { AlertFeed } from "@/components/dashboard/AlertFeed";
import { SystemStatus } from "@/components/dashboard/SystemStatus";
import { IntentTimeline } from "@/components/dashboard/IntentTimeline";
import {
  AlertTriangle,
  Shield,
  Train,
  Activity,
  Plane,
  Users,
  ChevronRight,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <DashboardLayout>
      {/* Header Section */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Command Center</h1>
          <p className="text-sm text-muted-foreground">
            Northern Railway Division • Real-time monitoring active
          </p>
        </div>
        <div className="flex items-center gap-3">
          <StatusBadge status="critical">3 ACTIVE ALERTS</StatusBadge>
          <Button variant="outline" size="sm">
            View All Alerts
            <ChevronRight className="w-4 h-4 ml-1" />
          </Button>
        </div>
      </div>

      {/* System Status Bar */}
      <div className="mb-6">
        <SystemStatus />
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <MetricCard
          label="Active Threats"
          value={2}
          icon={AlertTriangle}
          status="critical"
          trend="up"
          trendValue="2 new"
        />
        <MetricCard
          label="Track Segments"
          value={847}
          unit="/ 856"
          icon={Shield}
          status="safe"
        />
        <MetricCard
          label="Running Trains"
          value={124}
          icon={Train}
          trend="neutral"
          trendValue="On schedule"
        />
        <MetricCard
          label="Drones Active"
          value={8}
          icon={Plane}
          status="info"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Map Section - Takes 2 columns */}
        <div className="xl:col-span-2 space-y-6">
          <DataPanel
            title="Track Network Overview"
            subtitle="Click any segment for detailed analysis"
            variant="elevated"
          >
            <RailwayMap onSegmentClick={(segment) => navigate("/tracks")} />
          </DataPanel>

          {/* Intent Timeline for Selected Alert */}
          <DataPanel
            title="Active Threat Analysis"
            subtitle="TS-004 • Ghaziabad-Meerut Section"
            variant="danger"
            action={
              <StatusBadge status="critical" size="lg">
                HIGH RISK
              </StatusBadge>
            }
          >
            <IntentTimeline />
          </DataPanel>
        </div>

        {/* Alerts Panel - Takes 1 column */}
        <div className="space-y-6">
          <DataPanel
            title="Live Alert Feed"
            subtitle="Sorted by severity & time"
            variant="glow"
            action={
              <span className="live-indicator text-xs text-muted-foreground">
                Live
              </span>
            }
          >
            <AlertFeed />
          </DataPanel>

          {/* Quick Actions */}
          <DataPanel title="Quick Actions" variant="default">
            <div className="grid grid-cols-2 gap-3">
              <button className="p-4 rounded-lg bg-secondary border border-border hover:border-primary/50 transition-all text-left group">
                <Plane className="w-5 h-5 text-primary mb-2" />
                <p className="text-sm font-medium text-foreground">
                  Dispatch Drone
                </p>
                <p className="text-[10px] text-muted-foreground">
                  To TS-004
                </p>
              </button>
              <button className="p-4 rounded-lg bg-secondary border border-border hover:border-primary/50 transition-all text-left group">
                <Users className="w-5 h-5 text-accent mb-2" />
                <p className="text-sm font-medium text-foreground">
                  Alert GRP
                </p>
                <p className="text-[10px] text-muted-foreground">
                  Send team
                </p>
              </button>
              <button className="p-4 rounded-lg bg-secondary border border-border hover:border-primary/50 transition-all text-left group">
                <Train className="w-5 h-5 text-status-warning mb-2" />
                <p className="text-sm font-medium text-foreground">
                  Speed Alert
                </p>
                <p className="text-[10px] text-muted-foreground">
                  Restrict zone
                </p>
              </button>
              <button className="p-4 rounded-lg bg-secondary border border-border hover:border-primary/50 transition-all text-left group">
                <Activity className="w-5 h-5 text-sensor-vibration mb-2" />
                <p className="text-sm font-medium text-foreground">
                  Run Analysis
                </p>
                <p className="text-[10px] text-muted-foreground">
                  Full intent scan
                </p>
              </button>
            </div>
          </DataPanel>
        </div>
      </div>
    </DashboardLayout>
  );
}
