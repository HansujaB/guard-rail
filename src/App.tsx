import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import TrackDetail from "./pages/TrackDetail";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/tracks" element={<TrackDetail />} />
          {/* Placeholder routes */}
          <Route path="/alerts" element={<Dashboard />} />
          <Route path="/activity" element={<Dashboard />} />
          <Route path="/drones" element={<Dashboard />} />
          <Route path="/intent" element={<Dashboard />} />
          <Route path="/incidents" element={<Dashboard />} />
          <Route path="/analytics" element={<Dashboard />} />
          <Route path="/config" element={<Dashboard />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
