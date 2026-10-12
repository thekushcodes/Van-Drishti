import { createFileRoute } from "@tanstack/react-router";
import { ResultsPage } from "@/features/wildlife/results";
import { pageHead } from "@/lib/page-head";
export const Route = createFileRoute("/workspace/results")({
  head: () =>
    pageHead(
      "Analysis results — VanDrishti",
      "Analysis results for wildlife footage and field intelligence in the VanDrishti workspace.",
    ),
  component: ResultsPage,
});
