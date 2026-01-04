# IRSS COMMAND - Intent-Aware Railway Safety System

Real-time intent intelligence platform for railway security monitoring and threat detection.

## Project Overview

IRSS COMMAND is an advanced railway security monitoring system that uses AI-powered intent analysis, sensor fusion, and real-time analytics to detect and prevent threats to railway infrastructure. The system monitors track segments, analyzes sensor data, and provides actionable intelligence for security teams.

## Features

- **Real-time Monitoring**: Live dashboard with sensor data, alerts, and system status
- **Intent Analysis**: AI-powered threat detection based on multi-sensor data fusion
- **Track Monitoring**: Geographic visualization of track segments with status indicators
- **Alert Management**: Real-time alert feed with severity classification and intent scores
- **Sensor Analytics**: Vibration, acoustic, temperature, and pressure monitoring
- **Drone Control**: Integration with surveillance drone systems
- **Human Activity Detection**: AI-based monitoring of human presence and behavior
- **Incident Management**: Historical incident tracking and analysis

## Technology Stack

This project is built with:

- **Frontend Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Components**: shadcn-ui (Radix UI primitives)
- **Styling**: Tailwind CSS
- **Routing**: React Router DOM
- **State Management**: TanStack Query (React Query)
- **Charts**: Recharts
- **Icons**: Lucide React

## Getting Started

### Prerequisites

- Node.js (v18 or higher recommended)
- npm or yarn package manager

### Installation

1. Clone the repository:
```bash
git clone <YOUR_REPO_URL>
cd guard-rail
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:8080`

### Build for Production

```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
guard-rail/
├── public/           # Static assets
├── src/
│   ├── components/   # React components
│   │   ├── dashboard/    # Dashboard-specific components
│   │   ├── layout/       # Layout components (Header, Sidebar, etc.)
│   │   └── ui/           # Reusable UI components
│   ├── pages/        # Page components (Dashboard, Login, etc.)
│   ├── hooks/        # Custom React hooks
│   └── lib/          # Utility functions
├── index.html
└── package.json
```

## Current Status

**Frontend**: Partially complete
- ✅ Dashboard page
- ✅ Track Detail page
- ✅ Login page (UI only, authentication not implemented)
- ✅ Layout components (Header, Sidebar)
- ⚠️ Authentication: UI present but backend integration needed (low priority)
- ⚠️ Missing pages: Alerts, Activity, Drones, Intent, Incidents, Analytics, Config (currently redirect to Dashboard)

**Backend**: Not implemented
- See `BACKEND_ARCHITECTURE.md` for detailed backend requirements

## Development

### Linting

```bash
npm run lint
```

## License

[Add your license here]

## Contact

[Add contact information here]
