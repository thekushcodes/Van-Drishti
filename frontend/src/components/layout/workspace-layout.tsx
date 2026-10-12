import { Link, Outlet, useRouterState } from "@tanstack/react-router";
import { useState } from "react";
import {
  LayoutDashboard,
  Video,
  ScanLine,
  FileText,
  ShieldCheck,
  Bell,
  ArrowLeft,
  Menu,
  X,
  AlertTriangle,
  ArrowUpRight,
} from "lucide-react";
import { Brand } from "./public-layout";
import { Button } from "@/components/ui/button";
import { API_URL, useWildlife } from "@/features/wildlife/context";
import { ThemeToggle } from "@/components/theme-toggle";

const items = [
  { to: "/workspace", label: "Overview", icon: LayoutDashboard },
  { to: "/workspace/analysis", label: "Video analysis", icon: Video },
  { to: "/workspace/results", label: "Analysis results", icon: ScanLine },
  { to: "/workspace/intelligence", label: "Intelligence reports", icon: FileText },
  { to: "/workspace/reviews", label: "Review queue", icon: ShieldCheck },
  { to: "/workspace/alerts", label: "Field alerts", icon: Bell },
] as const;
export function WorkspaceLayout() {
  const [open, setOpen] = useState(false);
  const path = useRouterState({ select: (s) => s.location.pathname });
  const { error, setError, reviews, alerts, runId } = useWildlife();
  const current = items.find((i) => i.to === path)?.label || "Overview";
  return (
    <div className="workspace-app">
      <aside className={open ? "workspace-sidebar sidebar-open" : "workspace-sidebar"}>
        <Link to="/">
          <Brand />
        </Link>
        <div className="eyebrow sidebar-label">FIELD WORKSPACE</div>
        <nav aria-label="Workspace navigation">
          {items.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              activeOptions={{ exact: true }}
              activeProps={{ className: "workspace-nav-active" }}
              onClick={() => setOpen(false)}
            >
              <Icon size={19} />
              <span>{label}</span>
              {to === "/workspace/reviews" &&
                reviews.filter((r) => r.status === "open").length > 0 && (
                  <small>{reviews.filter((r) => r.status === "open").length}</small>
                )}
              {to === "/workspace/alerts" && alerts.length > 0 && <small>{alerts.length}</small>}
            </Link>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <span className="eyebrow">CONFIGURED SERVICE</span>
          <code>{API_URL}</code>
          <span className="service-note">Connection not yet verified</span>
          <Link to="/">
            <ArrowLeft size={16} /> Back to website
          </Link>
        </div>
      </aside>
      {open && (
        <Button
          className="sidebar-backdrop"
          variant="ghost"
          onClick={() => setOpen(false)}
          aria-label="Close navigation"
        />
      )}
      <div className="workspace-shell">
        <header className="workspace-topbar">
          <div>
            <Button
              variant="ghost"
              size="icon"
              className="menu-toggle"
              onClick={() => setOpen(!open)}
              aria-label="Toggle navigation"
              aria-expanded={open}
            >
              {open ? <X /> : <Menu />}
            </Button>
            <span className="text-muted-foreground">Workspace</span>
            <span className="text-muted-foreground">/</span>
            <span>{current}</span>
          </div>
          <div className="workspace-header-actions">
            <ThemeToggle />
            <Link to="/" className="editorial-link">
              VanDrishti <ArrowUpRight size={16} />
            </Link>
          </div>
        </header>
        <main className="workspace-content">
          {error && (
            <div className="error-banner" role="alert">
              <AlertTriangle size={22} />
              <div>
                <strong>Something needs your attention</strong>
                <p>{error}</p>
              </div>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setError("")}
                aria-label="Dismiss error"
              >
                <X />
              </Button>
            </div>
          )}
          <Outlet />
          <footer className="workspace-footer">
            <span>VANDRISHTI / FIELD INTELLIGENCE</span>
            <span>{runId ? `RUN ${runId}` : "No active analysis"}</span>
          </footer>
        </main>
      </div>
    </div>
  );
}
