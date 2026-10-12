import { createFileRoute } from "@tanstack/react-router";
import { AnalysisPage } from "@/features/wildlife/analysis";
import { pageHead } from "@/lib/page-head";
export const Route = createFileRoute("/workspace/analysis")({
  head: () =>
    pageHead(
      "Video analysis — VanDrishti",
      "Video analysis for wildlife footage and field intelligence in the VanDrishti workspace.",
    ),
  component: AnalysisPage,
});
