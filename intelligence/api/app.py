"""M4 HTTP boundary. M1 posts evidence; M5 reads reports and review work here."""

from __future__ import annotations

from uuid import UUID

from fastapi import FastAPI, HTTPException, Query, status

from intelligence.models import BackendEvidenceBundle, IntelligenceRun, ReviewItem, ReviewResolution
from intelligence.service import IntelligenceService, RunNotFoundError


def create_app(service: IntelligenceService | None = None) -> FastAPI:
    app = FastAPI(title="VanDrishti M4 Intelligence API", version="0.1.0")
    app.state.intelligence_service = service or IntelligenceService()

    @app.get("/health", tags=["service"])
    def health() -> dict[str, str]:
        return {"status": "ok", "module": "M4-intelligence"}

    @app.post(
        "/api/v1/intelligence/runs",
        response_model=IntelligenceRun,
        status_code=status.HTTP_201_CREATED,
        tags=["M1 to M4"],
        summary="Create an M4 intelligence run from M1 evidence.",
    )
    def create_intelligence_run(bundle: BackendEvidenceBundle) -> IntelligenceRun:
        return app.state.intelligence_service.create_run(bundle)

    @app.get(
        "/api/v1/intelligence/runs/{run_id}",
        response_model=IntelligenceRun,
        tags=["M4 to M5"],
        summary="Read a completed M4 result for the dashboard.",
    )
    def get_intelligence_run(run_id: UUID) -> IntelligenceRun:
        try:
            return app.state.intelligence_service.get_run(run_id)
        except RunNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Intelligence run not found") from exc

    @app.get(
        "/api/v1/intelligence/review-items",
        response_model=list[ReviewItem],
        tags=["M4 to M5"],
        summary="List M4 review queue entries for the dashboard or reviewer.",
    )
    def list_review_items(status_filter: str | None = Query(default=None, alias="status")) -> list[ReviewItem]:
        if status_filter not in {None, "open", "resolved"}:
            raise HTTPException(status_code=422, detail="status must be open or resolved")
        return app.state.intelligence_service.get_review_items(status_filter)

    @app.post(
        "/api/v1/intelligence/review-items/{review_id}/resolve",
        response_model=ReviewItem,
        tags=["review"],
        summary="Record a human review decision without altering M1/M2/M3 evidence.",
    )
    def resolve_review_item(review_id: UUID, resolution: ReviewResolution) -> ReviewItem:
        try:
            return app.state.intelligence_service.resolve_review_item(
                review_id, resolution.resolution_note
            )
        except RunNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Review item not found") from exc

    return app


app = create_app()
