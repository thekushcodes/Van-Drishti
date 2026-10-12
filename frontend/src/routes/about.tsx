import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowUpRight } from "lucide-react";
import { ContentPage } from "@/components/layout/content-page";
import { pageHead } from "@/lib/page-head";
export const Route = createFileRoute("/about")({
  head: () =>
    pageHead(
      "Our purpose — VanDrishti",
      "Conservation-first wildlife intelligence, grounded in evidence and human judgement.",
    ),
  component: AboutPage,
});
function AboutPage() {
  return (
    <ContentPage
      eyebrow="OUR PURPOSE"
      title="For a world worth watching."
      description="Better understanding is the beginning of better protection."
    >
      <section className="purpose-band">
        <h2>
          Conservation first.
          <br />
          Evidence always.
        </h2>
        <div>
          <p>
            The forest is full of moments we rarely see. Camera traps make those moments visible —
            but a recording is only the beginning. Understanding what it contains takes time,
            attention and context.
          </p>
          <p>
            VanDrishti brings wildlife video analysis, intelligence reports and human review into a
            single workspace. Its purpose is to help turn footage into information that can support
            more informed wildlife monitoring.
          </p>
          <p>
            Technology should support judgement, not replace it. Every assessment belongs beside the
            source evidence, and every uncertain finding deserves a closer look.
          </p>
          <Link to="/platform" className="editorial-link">
            Discover the platform <ArrowUpRight size={18} />
          </Link>
        </div>
      </section>
    </ContentPage>
  );
}
