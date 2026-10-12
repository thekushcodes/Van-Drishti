import { Link } from "@tanstack/react-router";
import { ArrowUpRight, ShieldCheck } from "lucide-react";
import { API_URL, useWildlife } from "./context";
import { Heading, Empty, Status } from "./shared";

export function ResultsPage() {
  const { result, runId } = useWildlife();
  const confidence = result?.detections?.average_confidence;
  return (
    <>
      <Heading
        eyebrow="02 / ANALYSIS EVIDENCE"
        title="Detection results."
        description={
          result
            ? `Evidence returned for analysis run ${runId}.`
            : "The details behind every detection."
        }
      />
      {!result ? (
        <Empty
          title="No results yet"
          description="Analyse a field recording to see its species detections and processed footage."
        />
      ) : (
        <>
          <div className="metrics-grid">
            <article>
              <span>Total detections</span>
              <strong>{result.detections?.total ?? "—"}</strong>
            </article>
            <article>
              <span>Average confidence</span>
              <strong>
                {typeof confidence === "number" && Number.isFinite(confidence)
                  ? `${(confidence * 100).toFixed(1)}%`
                  : "—"}
              </strong>
            </article>
            <article>
              <span>Species detected</span>
              <strong>
                {result.detections?.species_counts
                  ? Object.values(result.detections.species_counts).filter((n) => n > 0).length
                  : "—"}
              </strong>
            </article>
            <article>
              <span>Run status</span>
              <Status severity="success">{result.status || "Not supplied"}</Status>
            </article>
          </div>
          <section className="data-section">
            <div className="eyebrow">SPECIES BREAKDOWN</div>
            <h2>Detection profile</h2>
            {result.detections?.species_counts ? (
              Object.entries(result.detections.species_counts).map(([species, count]) => (
                <div className="species-row" key={species}>
                  <span className="species-code">{species.slice(0, 3).toUpperCase()}</span>
                  <strong>{species}</strong>
                  <span>{count} detections</span>
                </div>
              ))
            ) : (
              <p className="text-muted-foreground">
                No species counts were included in this response.
              </p>
            )}
          </section>
          {result.output_video ? (
            <section className="data-section">
              <div className="eyebrow">PROCESSED EVIDENCE</div>
              <h2>Analysed recording</h2>
              <video
                className="result-video"
                controls
                preload="metadata"
                playsInline
                src={`${API_URL}${result.output_video}`}
              >
                Your browser does not support video playback.
              </video>
            </section>
          ) : (
            <section className="data-section">
              <h2>Processed recording unavailable</h2>
              <p>The response did not include an output video.</p>
            </section>
          )}
          <div className="result-links">
            <Link to="/workspace/intelligence">
              Intelligence report <ArrowUpRight size={18} />
            </Link>
            <Link to="/workspace/reviews">
              Review queue <ArrowUpRight size={18} />
            </Link>
            <Link to="/workspace/alerts">
              Field alerts <ArrowUpRight size={18} />
            </Link>
          </div>
        </>
      )}
    </>
  );
}
export function IntelligencePage() {
  const { result, runId } = useWildlife();
  const report = result?.intelligence;
  return (
    <>
      <Heading
        eyebrow="03 / M4 INTELLIGENCE"
        title="Intelligence reports."
        description="Read the assessment. Return to the evidence."
      />
      {!result ? (
        <Empty
          title="No intelligence report yet"
          description="Complete an analysis to retrieve the intelligence included in its result."
        />
      ) : report ? (
        <article className="intelligence-report">
          <div className="report-meta">
            <span className="eyebrow">ANALYSIS RUN / {runId}</span>
            <Status>{report.status || "Available"}</Status>
          </div>
          <h2>{report.title || "Intelligence report"}</h2>
          <div className="report-narrative">{report.narrative || "No narrative was returned."}</div>
          <div className="notice-box">
            <ShieldCheck size={22} />
            <p>
              Machine-generated assessment. Verify source evidence before taking operational action.
            </p>
          </div>
          <Link className="editorial-link" to="/workspace/results">
            Inspect source evidence <ArrowUpRight size={18} />
          </Link>
        </article>
      ) : (
        <div className="empty-state">
          <h2>No report was returned</h2>
          <p>This run’s response did not include an intelligence assessment.</p>
          <Link className="editorial-link" to="/workspace/results">
            View detection results <ArrowUpRight size={18} />
          </Link>
        </div>
      )}
    </>
  );
}
