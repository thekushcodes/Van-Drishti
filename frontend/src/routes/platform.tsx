import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowUpRight } from "lucide-react";
import { ContentPage } from "@/components/layout/content-page";
import { pageHead } from "@/lib/page-head";
export const Route = createFileRoute("/platform")({
  head: () =>
    pageHead(
      "The platform — VanDrishti",
      "Wildlife video detection, processed evidence, M4 intelligence and human review.",
    ),
  component: PlatformPage,
});
function PlatformPage() {
  return (
    <ContentPage
      eyebrow="THE VANDRISHTI PLATFORM"
      title="Observe closely. Understand deeply."
      description="An evidence-led workspace for the people behind wildlife conservation."
    >
      <section className="content-band">
        <div className="content-list">
          {[
            {
              t: "Wildlife video analysis",
              d: "Bring camera-trap footage into the detection pipeline. YOLO-based analysis identifies wildlife and returns species counts and model confidence.",
              to: "/workspace/analysis",
              a: "Analyse footage",
            },
            {
              t: "Evidence you can inspect",
              d: "Watch processed footage when available and examine the results returned for each analysis run. No invented detections. No substituted demonstration data.",
              to: "/workspace/results",
              a: "View analysis results",
            },
            {
              t: "Intelligence with context",
              d: "Read the M4 intelligence narrative together with its report status and original analysis evidence. Keep human judgement at the centre of every decision.",
              to: "/workspace/intelligence",
              a: "Open intelligence reports",
            },
            {
              t: "A human in the loop",
              d: "Review alerts by severity and inspect items requiring verification. Record a resolution note to close a review through the existing service.",
              to: "/workspace/reviews",
              a: "Open review queue",
            },
          ].map(({ t, d, to, a }) => (
            <article key={t}>
              <h2>{t}</h2>
              <p>{d}</p>
              <Link
                className="editorial-link"
                to={
                  to as
                    | "/workspace/analysis"
                    | "/workspace/results"
                    | "/workspace/intelligence"
                    | "/workspace/reviews"
                }
              >
                {a}
                <ArrowUpRight size={18} />
              </Link>
            </article>
          ))}
        </div>
      </section>
      <section className="purpose-band">
        <h2>
          Honest about
          <br />
          what’s available.
        </h2>
        <div>
          <p>
            Individual animal re-identification, live camera connections and emergency dispatch are
            not connected to the current analysis workflow. VanDrishti does not present simulated
            activity as live monitoring.
          </p>
          <Link to="/workspace" className="editorial-link">
            Enter the workspace <ArrowUpRight size={18} />
          </Link>
        </div>
      </section>
    </ContentPage>
  );
}
