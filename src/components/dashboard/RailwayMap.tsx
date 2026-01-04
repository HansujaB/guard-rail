import { useState } from "react";
import { cn } from "@/lib/utils";

interface TrackSegment {
  id: string;
  name: string;
  status: "normal" | "suspicious" | "danger";
  x: number;
  y: number;
  width: number;
  sensors: number;
  lastUpdate: string;
}

const mockTrackSegments: TrackSegment[] = [
  { id: "TS-001", name: "Delhi-Ghaziabad Section A", status: "normal", x: 50, y: 120, width: 180, sensors: 12, lastUpdate: "2 min ago" },
  { id: "TS-002", name: "Delhi-Ghaziabad Section B", status: "normal", x: 230, y: 120, width: 150, sensors: 8, lastUpdate: "1 min ago" },
  { id: "TS-003", name: "Ghaziabad Junction", status: "suspicious", x: 380, y: 100, width: 60, sensors: 6, lastUpdate: "30 sec ago" },
  { id: "TS-004", name: "Ghaziabad-Meerut Section", status: "danger", x: 440, y: 80, width: 200, sensors: 15, lastUpdate: "LIVE" },
  { id: "TS-005", name: "Delhi-Faridabad Section", status: "normal", x: 100, y: 200, width: 160, sensors: 10, lastUpdate: "3 min ago" },
  { id: "TS-006", name: "Faridabad-Palwal Section", status: "normal", x: 260, y: 220, width: 180, sensors: 14, lastUpdate: "5 min ago" },
  { id: "TS-007", name: "Delhi-Rohtak Section A", status: "normal", x: 30, y: 60, width: 120, sensors: 9, lastUpdate: "2 min ago" },
  { id: "TS-008", name: "Delhi-Rohtak Section B", status: "suspicious", x: 150, y: 40, width: 140, sensors: 11, lastUpdate: "45 sec ago" },
];

interface RailwayMapProps {
  onSegmentClick?: (segment: TrackSegment) => void;
}

export function RailwayMap({ onSegmentClick }: RailwayMapProps) {
  const [hoveredSegment, setHoveredSegment] = useState<string | null>(null);
  const [selectedSegment, setSelectedSegment] = useState<string | null>(null);

  const handleClick = (segment: TrackSegment) => {
    setSelectedSegment(segment.id);
    onSegmentClick?.(segment);
  };

  return (
    <div className="relative w-full h-[400px] bg-secondary/30 rounded-lg border border-border overflow-hidden map-container">
      {/* Grid Background */}
      <div className="absolute inset-0 grid-pattern opacity-50" />
      
      {/* Scan line effect */}
      <div className="absolute inset-0 scan-line pointer-events-none" />

      {/* Map SVG */}
      <svg className="absolute inset-0 w-full h-full" viewBox="0 0 700 300">
        {/* Central Station */}
        <circle cx="180" cy="140" r="20" className="fill-primary/30 stroke-primary stroke-2" />
        <text x="180" y="145" textAnchor="middle" className="fill-primary text-[10px] font-bold">NDLS</text>
        
        {/* Track Segments */}
        {mockTrackSegments.map((segment) => (
          <g key={segment.id}>
            {/* Track Line */}
            <rect
              x={segment.x}
              y={segment.y}
              width={segment.width}
              height={8}
              rx={4}
              className={cn(
                "cursor-pointer transition-all duration-300 track-segment",
                segment.status === "normal" && "fill-track-normal/60 stroke-track-normal",
                segment.status === "suspicious" && "fill-track-suspicious/60 stroke-track-suspicious status-pulse-warning",
                segment.status === "danger" && "fill-track-danger/60 stroke-track-danger status-pulse-critical",
                hoveredSegment === segment.id && "brightness-125",
                selectedSegment === segment.id && "stroke-[3]"
              )}
              strokeWidth={1.5}
              onClick={() => handleClick(segment)}
              onMouseEnter={() => setHoveredSegment(segment.id)}
              onMouseLeave={() => setHoveredSegment(null)}
            />
            
            {/* Sensor Nodes */}
            {Array.from({ length: Math.min(4, segment.sensors) }).map((_, i) => (
              <circle
                key={i}
                cx={segment.x + (segment.width / 5) * (i + 1)}
                cy={segment.y + 4}
                r={3}
                className={cn(
                  "transition-all",
                  segment.status === "normal" && "fill-track-normal",
                  segment.status === "suspicious" && "fill-track-suspicious animate-pulse",
                  segment.status === "danger" && "fill-track-danger animate-pulse"
                )}
              />
            ))}
          </g>
        ))}

        {/* Moving Train */}
        <g className="animate-pulse">
          <rect x="280" y="116" width="30" height="16" rx={3} className="fill-accent stroke-accent-foreground" />
          <text x="295" y="127" textAnchor="middle" className="fill-accent-foreground text-[8px] font-bold">12001</text>
        </g>

        {/* Drone Icon */}
        <g>
          <circle cx="460" cy="60" r={12} className="fill-status-info/30 stroke-status-info stroke-2 status-pulse-warning" />
          <text x="460" y="64" textAnchor="middle" className="fill-status-info text-[8px]">🚁</text>
        </g>
      </svg>

      {/* Hover Tooltip */}
      {hoveredSegment && (
        <div className="absolute bottom-4 left-4 bg-card border border-border rounded-lg p-3 shadow-lg animate-fade-up z-10">
          {(() => {
            const segment = mockTrackSegments.find(s => s.id === hoveredSegment);
            if (!segment) return null;
            return (
              <>
                <div className="flex items-center gap-2 mb-2">
                  <span className={cn(
                    "w-2 h-2 rounded-full",
                    segment.status === "normal" && "bg-track-normal",
                    segment.status === "suspicious" && "bg-track-suspicious",
                    segment.status === "danger" && "bg-track-danger"
                  )} />
                  <span className="text-xs font-bold text-foreground">{segment.id}</span>
                  <span className="text-xs text-muted-foreground">|</span>
                  <span className="text-xs text-muted-foreground">{segment.name}</span>
                </div>
                <div className="flex items-center gap-4 text-[10px] text-muted-foreground">
                  <span>{segment.sensors} sensors</span>
                  <span>Updated: {segment.lastUpdate}</span>
                </div>
              </>
            );
          })()}
        </div>
      )}

      {/* Legend */}
      <div className="absolute top-4 right-4 bg-card/90 backdrop-blur border border-border rounded-lg p-3">
        <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider mb-2">Status</p>
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-sm bg-track-normal" />
            <span className="text-[10px] text-muted-foreground">Normal</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-sm bg-track-suspicious" />
            <span className="text-[10px] text-muted-foreground">Suspicious</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-sm bg-track-danger" />
            <span className="text-[10px] text-muted-foreground">High Risk</span>
          </div>
        </div>
      </div>
    </div>
  );
}
