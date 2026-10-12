"""Create review work only for low-confidence or numeric-validation cases."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from intelligence.models import BackendEvidenceBundle, NumericValidation, ReviewItem


class ReviewService:
    def __init__(self, low_detection_confidence: float = 0.60, low_reid_confidence: float = 0.65) -> None:
        self.low_detection_confidence = low_detection_confidence
        self.low_reid_confidence = low_reid_confidence

    def create_items(
        self,
        run_id: UUID,
        bundle: BackendEvidenceBundle,
        numeric_validation: NumericValidation,
        system_review_reason: str | None = None,
    ) -> list[ReviewItem]:
        created_at = datetime.now(UTC)
        items: list[ReviewItem] = []
        for observation in bundle.observations:
            if observation.detection_confidence < self.low_detection_confidence:
                items.append(
                    ReviewItem(
                        run_id=run_id,
                        event_id=observation.event_id,
                        reason=(
                            "Detection/species confidence "
                            f"{observation.detection_confidence:.2f} is below "
                            f"the {self.low_detection_confidence:.2f} review threshold."
                        ),
                        created_at=created_at,
                    )
                )
            if (
                observation.reid_confidence is not None
                and observation.reid_confidence < self.low_reid_confidence
            ):
                items.append(
                    ReviewItem(
                        run_id=run_id,
                        event_id=observation.event_id,
                        reason=(
                            f"Re-ID confidence {observation.reid_confidence:.2f} is below "
                            f"the {self.low_reid_confidence:.2f} review threshold."
                        ),
                        created_at=created_at,
                    )
                )
        if numeric_validation.status == "failed":
            items.append(
                ReviewItem(
                    run_id=run_id,
                    reason="Numeric Guard rejected an LLM numeric claim; a safe template report was used.",
                    created_at=created_at,
                )
            )
        if system_review_reason:
            items.append(
                ReviewItem(
                    run_id=run_id,
                    reason=system_review_reason,
                    created_at=created_at,
                )
            )
        return items
