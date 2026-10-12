import { Link } from "@tanstack/react-router";
import { ArrowUpRight, ScanLine } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { ReactNode } from "react";

export function Heading({
  eyebrow,
  title,
  description,
  action,
}: {
  eyebrow: string;
  title: string;
  description: string;
  action?: ReactNode;
}) {
  return (
    <div className="page-heading">
      <div>
        <div className="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      {action}
    </div>
  );
}
export function Empty({ title, description }: { title: string; description: string }) {
  return (
    <div className="empty-state">
      <ScanLine size={36} strokeWidth={1.3} />
      <h2>{title}</h2>
      <p>{description}</p>
      <Button variant="field" asChild>
        <Link to="/workspace/analysis">
          Analyse footage <ArrowUpRight />
        </Link>
      </Button>
    </div>
  );
}
export function Status({
  children,
  severity = "neutral",
}: {
  children: ReactNode;
  severity?: string | undefined;
}) {
  const kind = ["critical", "high", "danger"].includes(severity)
    ? "danger"
    : ["moderate", "medium", "open", "warning"].includes(severity)
      ? "warning"
      : ["success", "resolved", "low"].includes(severity)
        ? "success"
        : "neutral";
  return (
    <span className={`status status-${kind}`}>
      <span />
      {children}
    </span>
  );
}
export function formatBytes(bytes: number) {
  return bytes < 1024 * 1024
    ? `${(bytes / 1024).toFixed(0)} KB`
    : `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
