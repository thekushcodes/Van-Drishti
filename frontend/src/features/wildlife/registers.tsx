import { useState } from "react";
import { Search, AlertTriangle, Clock, Check, LoaderCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { useWildlife, type Review } from "./context";
import { Heading, Empty, Status } from "./shared";

export function AlertsPage() {
  const { result, alerts } = useWildlife();
  const [search, setSearch] = useState("");
  const [severity, setSeverity] = useState("all");
  const filtered = alerts.filter(
    (a) =>
      (severity === "all" || String(a.severity || "unknown").toLowerCase() === severity) &&
      `${a.message} ${a.alert_id} ${a.severity}`
        .toLowerCase()
        .includes(search.toLowerCase().trim()),
  );
  return (
    <>
      <Heading
        eyebrow="MONITORING / NOTIFICATIONS"
        title="Field alerts."
        description="Review the signals that need a closer look."
        action={result ? <Status>{alerts.length} returned</Status> : undefined}
      />
      {!result ? (
        <Empty
          title="No analysis selected"
          description="Complete a video analysis to retrieve its field alerts."
        />
      ) : (
        <section className="register-section">
          <div className="filter-bar">
            <label className="search-field">
              <Search size={18} />
              <input
                aria-label="Search alerts"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search messages or alert IDs"
              />
            </label>
            <select
              aria-label="Filter alerts by severity"
              value={severity}
              onChange={(e) => setSeverity(e.target.value)}
            >
              <option value="all">All severities</option>
              {[
                ...new Set([
                  "critical",
                  "high",
                  "medium",
                  "moderate",
                  "low",
                  ...alerts.map((a) => String(a.severity || "unknown").toLowerCase()),
                ]),
              ].map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
          {filtered.length ? (
            filtered.map((a) => (
              <article className="alert-record" key={a.alert_id}>
                <AlertTriangle size={24} />
                <div>
                  <div className="record-topline">
                    <Status severity={a.severity}>{a.severity || "Unknown severity"}</Status>
                    <span className="eyebrow">ALERT / {a.alert_id}</span>
                  </div>
                  <p>{a.message || "No alert description was supplied."}</p>
                  <small>
                    <Clock size={14} />
                    {a.created_at ? new Date(a.created_at).toLocaleString() : "Time not provided"}
                  </small>
                </div>
              </article>
            ))
          ) : (
            <div className="register-empty">
              <Check size={28} />
              <h2>{alerts.length ? "No matching alerts" : "No alerts returned"}</h2>
              <p>
                {alerts.length
                  ? "Try a different search or severity."
                  : "The service returned no alerts for this run. This does not establish the absence of threats."}
              </p>
            </div>
          )}
          <div className="register-bottom">
            <span>
              Showing {filtered.length} of {alerts.length} alerts
            </span>
            <Button
              variant="ghost"
              onClick={() => {
                setSearch("");
                setSeverity("all");
              }}
            >
              Clear filters
            </Button>
          </div>
        </section>
      )}
    </>
  );
}
export function ReviewsPage() {
  const { result, reviews, resolveReview, resolvingId } = useWildlife();
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("all");
  const [selected, setSelected] = useState<Review | null>(null);
  const [note, setNote] = useState("");
  const [failure, setFailure] = useState(false);
  const filtered = reviews.filter(
    (r) =>
      (status === "all" || r.status === status) &&
      `${r.reason} ${r.review_id} ${r.status}`.toLowerCase().includes(search.toLowerCase().trim()),
  );
  return (
    <>
      <Heading
        eyebrow="VERIFICATION / HUMAN OVERSIGHT"
        title="Review queue."
        description="Bring human judgement to the evidence."
        action={
          result ? (
            <Status severity="warning">
              {reviews.filter((r) => r.status === "open").length} open
            </Status>
          ) : undefined
        }
      />
      {!result ? (
        <Empty
          title="No analysis selected"
          description="Analyse a recording to retrieve its review items."
        />
      ) : (
        <section className="register-section">
          <div className="filter-bar">
            <label className="search-field">
              <Search size={18} />
              <input
                aria-label="Search reviews"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search reasons or review IDs"
              />
            </label>
            <select
              aria-label="Filter reviews by status"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              <option value="all">All statuses</option>
              <option value="open">Open</option>
              <option value="resolved">Resolved</option>
            </select>
          </div>
          {filtered.length ? (
            filtered.map((r) => (
              <article className="review-record" key={r.review_id}>
                <div>
                  <div className="record-topline">
                    <span className="eyebrow">REVIEW / {r.review_id}</span>
                    <Status severity={r.status}>{r.status || "Unknown"}</Status>
                  </div>
                  <p>{r.reason || "No review reason was supplied."}</p>
                </div>
                {r.status === "open" && (
                  <Button
                    variant="outline"
                    onClick={() => {
                      setSelected(r);
                      setNote("");
                      setFailure(false);
                    }}
                  >
                    <Check />
                    Resolve item
                  </Button>
                )}
              </article>
            ))
          ) : (
            <div className="register-empty">
              <Check size={28} />
              <h2>{reviews.length ? "No matching items" : "Review queue is clear"}</h2>
              <p>
                {reviews.length
                  ? "Try a different search or status."
                  : "No review items were returned for this analysis run."}
              </p>
            </div>
          )}
          <div className="register-bottom">
            <span>
              Showing {filtered.length} of {reviews.length} items
            </span>
            <Button
              variant="ghost"
              onClick={() => {
                setSearch("");
                setStatus("all");
              }}
            >
              Clear filters
            </Button>
          </div>
        </section>
      )}
      <Dialog
        open={selected !== null}
        onOpenChange={(open) => {
          if (!open && resolvingId === null) setSelected(null);
        }}
      >
        <DialogContent>
          <DialogTitle>Resolve review item</DialogTitle>
          <DialogDescription>
            Record your assessment before resolving review {selected?.review_id}.
          </DialogDescription>
          <p>{selected?.reason}</p>
          <form
            onSubmit={async (e) => {
              e.preventDefault();
              if (!selected) return;
              const success = await resolveReview(selected, note);
              if (success) setSelected(null);
              else setFailure(true);
            }}
          >
            <label className="form-label" htmlFor="resolution-note">
              Resolution note
            </label>
            <textarea
              id="resolution-note"
              required
              value={note}
              onChange={(e) => setNote(e.target.value)}
              rows={4}
              placeholder="Describe the evidence and your decision…"
              disabled={resolvingId !== null}
            />
            {failure && (
              <p className="text-destructive mt-2" role="alert">
                Could not resolve this item. Your note is preserved; please retry.
              </p>
            )}
            <div className="dialog-actions">
              <Button
                type="button"
                variant="outline"
                disabled={resolvingId !== null}
                onClick={() => setSelected(null)}
              >
                Cancel
              </Button>
              <Button variant="field" type="submit" disabled={!note.trim() || resolvingId !== null}>
                {resolvingId !== null ? <LoaderCircle className="spin" /> : <Check />}
                {resolvingId !== null ? "Resolving…" : "Confirm resolution"}
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </>
  );
}
