import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Shield, Lock, User, MapPin, ChevronRight, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const divisions = [
  { id: "nr", name: "Northern Railway", region: "Delhi, UP, Punjab" },
  { id: "cr", name: "Central Railway", region: "Mumbai, Maharashtra" },
  { id: "sr", name: "Southern Railway", region: "Chennai, TN, Kerala" },
  { id: "er", name: "Eastern Railway", region: "Kolkata, WB, Bihar" },
];

const roles = [
  { id: "control", name: "Control Room Officer", level: "L1" },
  { id: "admin", name: "Division Admin", level: "L2" },
  { id: "grp", name: "GRP / RPF Officer", level: "L1" },
  { id: "analyst", name: "Security Analyst", level: "L1" },
];

export default function Login() {
  const navigate = useNavigate();
  const [step, setStep] = useState<"credentials" | "division">("credentials");
  const [isLoading, setIsLoading] = useState(false);

  const handleCredentialSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setStep("division");
  };

  const handleDivisionSelect = (divisionId: string) => {
    setIsLoading(true);
    setTimeout(() => {
      navigate("/dashboard");
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-background flex">
      {/* Left Panel - Branding */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-background to-background" />
        <div className="absolute inset-0 grid-pattern opacity-30" />
        
        {/* Content */}
        <div className="relative z-10 flex flex-col justify-between p-12">
          {/* Logo */}
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-primary flex items-center justify-center shadow-lg">
              <Shield className="w-10 h-10 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground tracking-tight">
                IRSS COMMAND
              </h1>
              <p className="text-sm text-muted-foreground">
                Intent-Aware Railway Safety System
              </p>
            </div>
          </div>

          {/* Feature Highlights */}
          <div className="space-y-6">
            <div className="max-w-md">
              <h2 className="text-3xl font-bold text-foreground mb-4 leading-tight">
                Real-Time Intent Intelligence for Railway Security
              </h2>
              <p className="text-muted-foreground">
                Advanced sensor fusion and AI-powered intent analysis to protect India's railway infrastructure.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4 max-w-md">
              {[
                { value: "856", label: "Active Sensors" },
                { value: "24/7", label: "Monitoring" },
                { value: "98.7%", label: "Detection Rate" },
                { value: "<2s", label: "Response Time" },
              ].map((stat) => (
                <div key={stat.label} className="p-4 rounded-lg bg-card/50 border border-border">
                  <p className="text-2xl font-bold font-mono text-primary">{stat.value}</p>
                  <p className="text-xs text-muted-foreground">{stat.label}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Footer */}
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            <span>Ministry of Railways</span>
            <span className="w-1 h-1 rounded-full bg-muted-foreground" />
            <span>Government of India</span>
          </div>
        </div>

        {/* Animated elements */}
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-primary/10 rounded-full blur-3xl" />
        <div className="absolute top-1/4 right-1/4 w-64 h-64 bg-accent/10 rounded-full blur-3xl" />
      </div>

      {/* Right Panel - Login Form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          {step === "credentials" ? (
            <>
              {/* Mobile Logo */}
              <div className="lg:hidden flex items-center gap-3 mb-8">
                <div className="w-12 h-12 rounded-xl bg-primary flex items-center justify-center">
                  <Shield className="w-7 h-7 text-primary-foreground" />
                </div>
                <div>
                  <h1 className="text-lg font-bold text-foreground">IRSS COMMAND</h1>
                  <p className="text-xs text-muted-foreground">Railway Safety System</p>
                </div>
              </div>

              <div className="mb-8">
                <h2 className="text-2xl font-bold text-foreground mb-2">
                  Secure Access
                </h2>
                <p className="text-muted-foreground">
                  Enter your credentials to access the command center
                </p>
              </div>

              <form onSubmit={handleCredentialSubmit} className="space-y-5">
                <div className="space-y-2">
                  <Label htmlFor="username" className="text-sm font-medium">
                    Employee ID
                  </Label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <Input
                      id="username"
                      type="text"
                      placeholder="e.g., NR-12345"
                      className="pl-10 h-11 bg-secondary border-border focus:border-primary"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password" className="text-sm font-medium">
                    Password
                  </Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <Input
                      id="password"
                      type="password"
                      placeholder="••••••••"
                      className="pl-10 h-11 bg-secondary border-border focus:border-primary"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="role" className="text-sm font-medium">
                    Access Role
                  </Label>
                  <select
                    id="role"
                    className="w-full h-11 px-3 rounded-md bg-secondary border border-border text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
                    required
                  >
                    <option value="">Select your role</option>
                    {roles.map((role) => (
                      <option key={role.id} value={role.id}>
                        {role.name} ({role.level})
                      </option>
                    ))}
                  </select>
                </div>

                <Button
                  type="submit"
                  className="w-full h-11 bg-primary hover:bg-primary/90 text-primary-foreground font-medium"
                >
                  Authenticate
                  <ChevronRight className="w-4 h-4 ml-2" />
                </Button>
              </form>

              <div className="mt-6 p-4 rounded-lg bg-status-warning/10 border border-status-warning/30">
                <div className="flex items-start gap-3">
                  <AlertTriangle className="w-5 h-5 text-status-warning flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-foreground">Security Notice</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      This system is for authorized personnel only. All access attempts are logged and monitored.
                    </p>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <>
              <div className="mb-8">
                <h2 className="text-2xl font-bold text-foreground mb-2">
                  Select Division
                </h2>
                <p className="text-muted-foreground">
                  Choose your railway division to continue
                </p>
              </div>

              <div className="space-y-3">
                {divisions.map((division) => (
                  <button
                    key={division.id}
                    onClick={() => handleDivisionSelect(division.id)}
                    disabled={isLoading}
                    className="w-full p-4 rounded-lg bg-card border border-border hover:border-primary/50 hover:bg-secondary/50 transition-all text-left group disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center">
                          <MapPin className="w-5 h-5 text-primary" />
                        </div>
                        <div>
                          <p className="font-medium text-foreground">{division.name}</p>
                          <p className="text-xs text-muted-foreground">{division.region}</p>
                        </div>
                      </div>
                      <ChevronRight className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors" />
                    </div>
                  </button>
                ))}
              </div>

              {isLoading && (
                <div className="mt-6 flex items-center justify-center gap-3 text-muted-foreground">
                  <div className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                  <span className="text-sm">Initializing command center...</span>
                </div>
              )}

              <button
                onClick={() => setStep("credentials")}
                className="mt-6 text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                ← Back to login
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
