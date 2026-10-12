import { useRef, useState } from "react";
import { Link, useNavigate } from "@tanstack/react-router";
import {
  Upload,
  ScanLine,
  FileVideo,
  X,
  LoaderCircle,
  ArrowUpRight,
  RotateCcw,
  Check,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useWildlife } from "./context";
import { Heading, formatBytes, Status } from "./shared";

export function AnalysisPage() {
  const {
    video,
    setVideo,
    selectVideo,
    loading,
    phase,
    handleAnalyze,
    startNewAnalysis,
    result,
    runId,
  } = useWildlife();
  const input = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const navigate = useNavigate();
  return (
    <>
      <Heading
        eyebrow="01 / VIDEO INGESTION"
        title="Analyse field footage."
        description="A closer look at what your camera captured."
        action={
          <Button
            variant="outline"
            disabled={loading}
            onClick={() => {
              startNewAnalysis();
              if (input.current) input.current.value = "";
            }}
          >
            <RotateCcw />
            New analysis
          </Button>
        }
      />
      <section className="analysis-section">
        <div className="section-top">
          <div>
            <h2>Begin with a recording</h2>
            <p className="text-muted-foreground mt-2">
              Upload wildlife footage for detection and intelligence analysis.
            </p>
          </div>
          <span className="eyebrow">VIDEO INPUT</span>
        </div>
        <div
          className={`drop-zone ${dragging ? "drop-zone-active" : ""}`}
          onDragOver={(e) => {
            e.preventDefault();
            if (!loading) setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragging(false);
            selectVideo(e.dataTransfer.files[0]);
          }}
        >
          <input
            ref={input}
            type="file"
            accept="video/*"
            className="sr-only"
            aria-label="Choose wildlife video"
            disabled={loading}
            onChange={(e) => selectVideo(e.target.files?.[0])}
          />
          {video ? (
            <div className="selected-file">
              <FileVideo size={34} />
              <div>
                <strong>{video.name}</strong>
                <p>
                  {formatBytes(video.size)} · {loading ? phase : "Ready for analysis"}
                </p>
              </div>
              <Button
                variant="ghost"
                size="icon"
                disabled={loading}
                aria-label="Remove video"
                onClick={() => {
                  setVideo(null);
                  if (input.current) input.current.value = "";
                }}
              >
                <X />
              </Button>
            </div>
          ) : (
            <>
              <Upload size={35} strokeWidth={1.3} />
              <h3>Drop your footage here</h3>
              <p>or choose a video from your device</p>
              <Button variant="outline" onClick={() => input.current?.click()} disabled={loading}>
                Browse files <ArrowUpRight />
              </Button>
              <small>Video files · Formats supported by your analysis service</small>
            </>
          )}
        </div>
        <div className="upload-actions">
          <span className="text-muted-foreground">
            {video ? "Your original footage stays unchanged." : "No file selected"}
          </span>
          <Button
            variant="field"
            size="lg"
            disabled={!video || loading}
            onClick={async () => {
              const success = await handleAnalyze();
              if (success) navigate({ to: "/workspace/results" });
            }}
          >
            {loading ? <LoaderCircle className="spin" /> : <ScanLine />}
            {loading ? phase : "Upload and analyse"}
          </Button>
        </div>
        {loading && (
          <div className="processing-notice" role="status">
            <LoaderCircle className="spin" />
            <div>
              <strong>{phase}</strong>
              <p>Keep this page open while the service processes your recording.</p>
            </div>
          </div>
        )}
        {result && !loading && (
          <div className="processing-notice">
            <Check />
            <span>Run {runId} is ready.</span>
            <Button variant="link" asChild>
              <Link to="/workspace/results">
                View results <ArrowUpRight />
              </Link>
            </Button>
          </div>
        )}
      </section>
      <section className="analysis-next">
        <div className="eyebrow">WHAT COMES NEXT</div>
        <div className="steps-grid">
          {[
            ["01", "Species detections", "See the counts and confidence returned by the model."],
            ["02", "Processed evidence", "Play the analysed recording when it is available."],
            ["03", "Intelligence & review", "Inspect assessments, alerts and review items."],
          ].map(([n, t, d]) => (
            <article key={n}>
              <span>{n}</span>
              <h3>{t}</h3>
              <p>{d}</p>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
export function OverviewPage() {
  const { result, runId, reviews, alerts } = useWildlife();
  return (
    <>
      <Heading
        eyebrow="FIELD OPERATIONS / OVERVIEW"
        title="A closer look at the wild."
        description="Your footage, evidence and intelligence in one workspace."
        action={
          <Button variant="field" asChild>
            <Link to="/workspace/analysis">
              Analyse footage <ArrowUpRight />
            </Link>
          </Button>
        }
      />
      <section className="overview-lead">
        <div className="eyebrow">{result ? "CURRENT ANALYSIS" : "READY WHEN YOU ARE"}</div>
        <h2>
          {result ? "The evidence is ready for review." : "Every insight begins with observation."}
        </h2>
        <p>
          {result
            ? `Analysis run ${runId}`
            : "Bring a field recording into the workspace. Follow the evidence from species detection to an informed assessment."}
        </p>
        {result ? (
          <Status severity="success">{result.status || "Completed"}</Status>
        ) : (
          <Link className="editorial-link" to="/workspace/analysis">
            Start your first analysis <ArrowUpRight size={18} />
          </Link>
        )}
      </section>
      {result && (
        <div className="metrics-grid">
          <article>
            <span>Total detections</span>
            <strong>{result.detections?.total ?? "—"}</strong>
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
            <span>Open reviews</span>
            <strong>{reviews.filter((r) => r.status === "open").length}</strong>
          </article>
          <article>
            <span>Field alerts</span>
            <strong>{alerts.length}</strong>
          </article>
        </div>
      )}
      <div className="overview-destinations">
        {[
          {
            to: "/workspace/results",
            n: "01",
            t: "Analysis results",
            d: "Species counts, confidence and processed footage.",
          },
          {
            to: "/workspace/intelligence",
            n: "02",
            t: "Intelligence reports",
            d: "Read the assessment generated for your recording.",
          },
          {
            to: "/workspace/reviews",
            n: "03",
            t: "Human review",
            d: "Inspect findings and record a resolution.",
          },
          {
            to: "/workspace/alerts",
            n: "04",
            t: "Field alerts",
            d: "Review severity and source evidence.",
          },
        ].map(({ to, n, t, d }) => (
          <Link
            key={to}
            to={
              to as
                | "/workspace/results"
                | "/workspace/intelligence"
                | "/workspace/reviews"
                | "/workspace/alerts"
            }
          >
            <span className="eyebrow">{n}</span>
            <div>
              <h3>{t}</h3>
              <p>{d}</p>
            </div>
            <ArrowUpRight size={22} />
          </Link>
        ))}
      </div>
    </>
  );
}
