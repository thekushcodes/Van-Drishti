import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowUpRight } from "lucide-react";
import { ContentPage } from "@/components/layout/content-page";
import { Button } from "@/components/ui/button";
import { pageHead } from "@/lib/page-head";
export const Route = createFileRoute("/how-it-works")({
  head: () =>
    pageHead(
      "From footage to insight — VanDrishti",
      "Follow the wildlife footage workflow: upload, detection, evidence, intelligence and human verification.",
    ),
  component: WorkflowPage,
});
function WorkflowPage() {
  return (
    <ContentPage
      eyebrow="FROM FOOTAGE TO FIELD INSIGHT"
      title="Make every observation matter."
      description="A straightforward path from a wildlife recording to evidence you can review."
    >
      <section className="content-band">
        <div className="content-list">
          {[
            [
              "01 / UPLOAD",
              "Start with field footage",
              "Choose a video recording from your device, or drop it into the upload area. Your selected file is shown before you begin.",
            ],
            [
              "02 / ANALYSE",
              "Follow the wildlife",
              "The service receives your footage, creates an analysis run, and processes it using the existing wildlife detection pipeline.",
            ],
            [
              "03 / UNDERSTAND",
              "Inspect the evidence",
              "Explore the actual species counts, model confidence and processed video returned for the run. Read the accompanying M4 intelligence assessment when available.",
            ],
            [
              "04 / VERIFY",
              "Keep people in the loop",
              "Inspect field alerts and the review queue. Record an explicit resolution note for findings that require human verification.",
            ],
          ].map(([n, t, d]) => (
            <article key={n}>
              <div className="eyebrow mb-4">{n}</div>
              <h2>{t}</h2>
              <p>{d}</p>
            </article>
          ))}
        </div>
        <div className="mt-10">
          <Button variant="field" size="lg" asChild>
            <Link to="/workspace/analysis">
              Start analysing <ArrowUpRight />
            </Link>
          </Button>
        </div>
      </section>
    </ContentPage>
  );
}
