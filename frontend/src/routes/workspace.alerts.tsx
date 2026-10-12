import { createFileRoute } from "@tanstack/react-router";
import { AlertsPage } from "@/features/wildlife/registers";
import { pageHead } from "@/lib/page-head";
export const Route = createFileRoute("/workspace/alerts")({
  head: () =>
    pageHead(
      "Field alerts — VanDrishti",
      "Field alerts for wildlife footage and field intelligence in the VanDrishti workspace.",
    ),
  component: AlertsPage,
});
