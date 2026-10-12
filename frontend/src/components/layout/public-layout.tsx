import { Link } from "@tanstack/react-router";
import { useState, type ReactNode } from "react";
import { ArrowUpRight, Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";

export function Brand() {
  return (
    <span className="brand-lockup">
      <svg viewBox="0 0 40 40" width="35" height="35" aria-hidden="true">
        <path
          d="M5 27 16 8l9 19M17 27l9-17 10 17M5 32h31"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        />
        <circle cx="20" cy="28" r="3" fill="currentColor" />
      </svg>
      <span>
        VanDrishti<small>WILDLIFE INTELLIGENCE</small>
      </span>
    </span>
  );
}
export function PublicLayout({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="public-site">
      <header className="public-header">
        <Link to="/" aria-label="VanDrishti home">
          <Brand />
        </Link>
        <nav
          className={open ? "public-nav public-nav-open" : "public-nav"}
          aria-label="Main navigation"
          onClick={() => setOpen(false)}
        >
          <Link to="/" activeProps={{ className: "active" }}>
            Home
          </Link>
          <Link to="/platform" activeProps={{ className: "active" }}>
            The platform
          </Link>
          <Link to="/how-it-works" activeProps={{ className: "active" }}>
            How it works
          </Link>
          <Link to="/about" activeProps={{ className: "active" }}>
            Our purpose
          </Link>
        </nav>
        <div className="header-actions">
          <ThemeToggle />
          <Button variant="field" asChild>
            <Link to="/workspace">
              Open workspace <ArrowUpRight />
            </Link>
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="menu-toggle"
            aria-label={open ? "Close menu" : "Open menu"}
            aria-expanded={open}
            onClick={() => setOpen(!open)}
          >
            {open ? <X /> : <Menu />}
          </Button>
        </div>
      </header>
      <main>{children}</main>
      <footer className="public-footer">
        <div>
          <Link to="/">
            <Brand />
          </Link>
          <p>A clearer view. A better-informed future for the wild.</p>
        </div>
        <nav aria-label="Footer navigation">
          <Link to="/platform">The platform</Link>
          <Link to="/how-it-works">How it works</Link>
          <Link to="/about">Our purpose</Link>
          <Link to="/workspace/analysis">
            Start analysing <ArrowUpRight size={14} />
          </Link>
        </nav>
        <div className="footer-bottom">
          <span>© {new Date().getFullYear()} VanDrishti</span>
          <span>OBSERVE. UNDERSTAND. PROTECT.</span>
        </div>
      </footer>
    </div>
  );
}
