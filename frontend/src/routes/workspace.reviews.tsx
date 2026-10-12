import { createFileRoute } from "@tanstack/react-router";
import { ReviewsPage } from "@/features/wildlife/registers";
import { pageHead } from "@/lib/page-head";
export const Route = createFileRoute("/workspace/reviews")({
  head: () =>
    pageHead(
      "Review queue — VanDrishti",
      "Review queue for wildlife footage and field intelligence in the VanDrishti workspace.",
    ),
  component: ReviewsPage,
});
