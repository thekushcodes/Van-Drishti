import { createFileRoute } from "@tanstack/react-router";
import { IntelligencePage } from "@/features/wildlife/results";
import { pageHead } from "@/lib/page-head";
export const Route = createFileRoute("/workspace/intelligence")({
  head: () =>
    pageHead(
      "Intelligence reports — VanDrishti",
      "Intelligence reports for wildlife footage and field intelligence in the VanDrishti workspace.",
    ),
  component: IntelligencePage,
});
