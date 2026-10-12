import { createContext, useContext, useState, type ReactNode } from "react";

export const API_URL = import.meta.env["VITE_API_URL"] || "http://127.0.0.1:8001";
export type Review = { review_id: string | number; status?: string; reason?: string };
export type Alert = {
  alert_id: string | number;
  severity?: string;
  message?: string;
  created_at?: string;
};
export type AnalysisResult = {
  status?: string;
  output_video?: string;
  detections?: {
    total?: number;
    average_confidence?: number;
    species_counts?: Record<string, number>;
  };
  intelligence?: { title?: string; status?: string; narrative?: string };
};

function useWildlifeState() {
  const [video, setVideo] = useState<File | null>(null);
  const [runId, setRunId] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(false);
  const [phase, setPhase] = useState("");
  const [error, setError] = useState("");
  const [resolvingId, setResolvingId] = useState<Review["review_id"] | null>(null);
  function selectVideo(file?: File) {
    if (!file || loading) return;
    if (!file.type.startsWith("video/")) {
      setError("Choose a valid video file.");
      return;
    }
    setVideo(file);
    setError("");
  }
  function startNewAnalysis() {
    if (loading) return;
    setVideo(null);
    setRunId(null);
    setResult(null);
    setReviews([]);
    setAlerts([]);
    setError("");
    setPhase("");
  }
  async function handleAnalyze() {
    if (loading) return false;
    if (!video) {
      setError("Choose a video file before starting analysis.");
      return false;
    }
    setLoading(true);
    setError("");
    setResult(null);
    setReviews([]);
    setAlerts([]);
    setRunId(null);
    try {
      setPhase("Uploading footage…");
      const formData = new FormData();
      formData.append("video", video);
      const uploadResponse = await fetch(`${API_URL}/api/v1/analysis-runs/upload`, {
        method: "POST",
        body: formData,
      });
      if (!uploadResponse.ok) throw new Error(`Video upload failed (${uploadResponse.status}).`);
      const uploadData = await uploadResponse.json();
      const analysisRunId = uploadData.analysis_run_id;
      if (!analysisRunId) throw new Error("The server did not return an analysis run ID.");
      setRunId(analysisRunId);
      setPhase("Analysing footage…");
      // Compatibility fix: the supplied App used stale React runId state here.
      // Keep POST /process unchanged; use the ID returned by this upload.
      const analyzeResponse = await fetch(
        `${API_URL}/api/v1/analysis-runs/${analysisRunId}/process`,
        { method: "POST" },
      );
      if (!analyzeResponse.ok)
        throw new Error(`Video analysis failed: ${await analyzeResponse.text()}`);
      setPhase("Retrieving results…");
      const resultResponse = await fetch(`${API_URL}/api/v1/analysis-runs/${analysisRunId}/result`);
      if (!resultResponse.ok) throw new Error("Could not retrieve the analysis result.");
      const resultData = await resultResponse.json();
      setResult(resultData);
      const [reviewResponse, alertResponse] = await Promise.all([
        fetch(`${API_URL}/api/v1/reviews?run_id=${analysisRunId}`),
        fetch(`${API_URL}/api/v1/alerts?run_id=${analysisRunId}`),
      ]);
      const warnings: string[] = [];
      if (reviewResponse.ok) {
        const data = await reviewResponse.json();
        setReviews(Array.isArray(data) ? data : []);
      } else warnings.push("The review queue could not be loaded.");
      if (alertResponse.ok) {
        const data = await alertResponse.json();
        setAlerts(Array.isArray(data) ? data : []);
      } else warnings.push("Field alerts could not be loaded.");
      if (warnings.length) setError(`Analysis completed. ${warnings.join(" ")}`);
      setPhase("Analysis complete");
      return true;
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message === "Failed to fetch"
            ? "Could not reach the analysis service. Check that your configured backend is running and permits this website to connect."
            : err.message
          : "An unexpected error occurred.",
      );
      setPhase("");
      return false;
    } finally {
      setLoading(false);
    }
  }
  async function resolveReview(review: Review, note: string) {
    if (!note.trim() || resolvingId !== null) return false;
    setResolvingId(review.review_id);
    setError("");
    try {
      const response = await fetch(`${API_URL}/api/v1/reviews/${review.review_id}/resolve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resolution_note: note.trim() }),
      });
      if (!response.ok) throw new Error(await response.text());
      setReviews((current) => current.filter((item) => item.review_id !== review.review_id));
      return true;
    } catch (err) {
      setError(
        `Could not resolve review: ${err instanceof Error ? err.message : "An unexpected error occurred."}`,
      );
      return false;
    } finally {
      setResolvingId(null);
    }
  }
  return {
    video,
    setVideo,
    runId,
    result,
    reviews,
    alerts,
    loading,
    phase,
    error,
    setError,
    resolvingId,
    selectVideo,
    startNewAnalysis,
    handleAnalyze,
    resolveReview,
  };
}
const WildlifeContext = createContext<ReturnType<typeof useWildlifeState> | null>(null);
export function WildlifeProvider({ children }: { children: ReactNode }) {
  return <WildlifeContext.Provider value={useWildlifeState()}>{children}</WildlifeContext.Provider>;
}
export function useWildlife() {
  const context = useContext(WildlifeContext);
  if (!context) throw new Error("Wildlife workspace provider is missing.");
  return context;
}
