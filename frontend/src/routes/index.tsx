import { createFileRoute, Link } from "@tanstack/react-router";
import {
  ArrowRight,
  ArrowUpRight,
  ScanLine,
  Footprints,
  FileText,
  ShieldCheck,
  ChevronDown,
} from "lucide-react";
import { PublicLayout } from "@/components/layout/public-layout";
import { Button } from "@/components/ui/button";
import { pageHead } from "@/lib/page-head";
import { WildlifeCover } from "@/components/layout/wildlife-cover";

export const Route = createFileRoute("/")({
  head: () =>
    pageHead(
      "VanDrishti — A clearer view of the wild",
      "Turn wildlife camera footage into species detections, intelligence reports and evidence for conservation.",
    ),
  component: Home,
});

function Home() {
  return (
    <PublicLayout>
      <section className="home-hero">
        <WildlifeCover priority />
        <div className="hero-shade" />
        <div className="hero-content">
          <div className="eyebrow hero-eyebrow">
            <span className="small-rule" /> WILDLIFE INTELLIGENCE. CONSERVATION FIRST.
          </div>
          <h1>
            VanDrishti
            <span>
              A clearer view
              <br />
              of the <em>wild.</em>
            </span>
          </h1>
          <p>
            From a moment in the forest to meaningful insight.
            <br className="desktop-break" /> Wildlife detection and intelligence, built for those
            <br className="desktop-break" /> who protect what matters.
          </p>
          <div className="hero-actions">
            <Button variant="field" size="lg" asChild>
              <Link to="/workspace/analysis">
                Start analysing <ArrowUpRight />
              </Link>
            </Button>
            <Button variant="cinema" size="lg" asChild>
              <Link to="/platform">
                Explore the platform <ArrowRight />
              </Link>
            </Button>
          </div>
        </div>
        <div className="hero-bottom">
          <span>OBSERVE. UNDERSTAND. PROTECT.</span>
          <Link to="/how-it-works">
            A closer look <ChevronDown size={15} />
          </Link>
        </div>
      </section>
      <section className="intro-band">
        <div className="eyebrow">PURPOSE, NOT JUST PROCESSING</div>
        <div>
          <h2>
            Every frame holds a story.
            <br />
            <em>Make it count.</em>
          </h2>
          <p>
            Camera traps capture the forest. VanDrishti connects the dots — turning footage into
            evidence that helps you understand wildlife and make informed conservation decisions.
          </p>
        </div>
        <Link className="editorial-link" to="/about">
          Our perspective <ArrowUpRight size={18} />
        </Link>
      </section>
      <section className="capabilities-band">
        <div className="section-top">
          <div>
            <div className="eyebrow">THE PLATFORM</div>
            <h2>Insight for the field.</h2>
          </div>
          <Link to="/platform" className="editorial-link">
            Explore capabilities <ArrowUpRight size={18} />
          </Link>
        </div>
        <div className="capability-grid">
          {[
            {
              icon: ScanLine,
              title: "Wildlife detection",
              text: "Identify species in camera-trap footage with YOLO-based video analysis.",
            },
            {
              icon: Footprints,
              title: "Species insights",
              text: "Understand detected wildlife through species counts and processed evidence.",
            },
            {
              icon: FileText,
              title: "Actionable intelligence",
              text: "Read the M4 assessment alongside the footage that informs it.",
            },
            {
              icon: ShieldCheck,
              title: "Human oversight",
              text: "Inspect field alerts and resolve findings that need a closer look.",
            },
          ].map(({ icon: Icon, title, text }, i) => (
            <article key={title}>
              <span className="capability-number">0{i + 1}</span>
              <Icon size={26} strokeWidth={1.4} />
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>
      <section className="workflow-band">
        <div className="eyebrow">FROM FOOTAGE TO FIELD INSIGHT</div>
        <h2>A recording. A clearer understanding.</h2>
        <div className="steps-grid">
          {[
            [
              "01",
              "Bring the footage",
              "Upload a wildlife recording from your camera trap or field camera.",
            ],
            [
              "02",
              "Let the evidence emerge",
              "Run detection and retrieve the processed footage and species results.",
            ],
            [
              "03",
              "Make an informed decision",
              "Review intelligence, inspect alerts, and verify the evidence.",
            ],
          ].map(([n, t, d]) => (
            <article key={n}>
              <span>{n}</span>
              <h3>{t}</h3>
              <p>{d}</p>
            </article>
          ))}
        </div>
        <Button variant="field" size="lg" asChild>
          <Link to="/workspace/analysis">
            Analyse your footage <ArrowUpRight />
          </Link>
        </Button>
      </section>
    </PublicLayout>
  );
}
