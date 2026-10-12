import { createFileRoute } from "@tanstack/react-router";
import { OverviewPage } from "@/features/wildlife/analysis";
import { pageHead } from "@/lib/page-head";
export const Route = createFileRoute("/workspace/")({
  head: () =>
    pageHead(
      "Overview — VanDrishti",
      "Overview for wildlife footage and field intelligence in the VanDrishti workspace.",
    ),
  component: OverviewPage,
});
