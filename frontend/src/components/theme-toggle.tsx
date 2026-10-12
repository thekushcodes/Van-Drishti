import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";

const ThemeContext = createContext({ dark: false, toggle: () => {} });

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [dark, setDark] = useState(false);
  useEffect(() => {
    let preference: string | null = null;
    try { preference = localStorage.getItem("vandrishti-theme"); } catch { /* Storage may be disabled. */ }
    const next = preference ? preference === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;
    setDark(next);
    document.documentElement.classList.toggle("dark", next);
  }, []);
  function toggle() {
    const next = !dark;
    setDark(next);
    document.documentElement.classList.toggle("dark", next);
    try { localStorage.setItem("vandrishti-theme", next ? "dark" : "light"); } catch { /* Keep session preference. */ }
  }
  return <ThemeContext.Provider value={{ dark, toggle }}>{children}</ThemeContext.Provider>;
}

export function ThemeToggle() {
  const { dark, toggle } = useContext(ThemeContext);
  const label = dark ? "Switch to light theme" : "Switch to dark theme";
  return (
    <Button variant="ghost" size="icon" className="theme-toggle" onClick={toggle} aria-label={label} title={label} aria-pressed={dark}>
      <span className="theme-icon" key={dark ? "sun" : "moon"}>
        {dark ? <Sun /> : <Moon />}
      </span>
    </Button>
  );
}