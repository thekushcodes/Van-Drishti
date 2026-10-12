"""Compose M2/M3 evidence into transparent explanations for M5 and reviewers."""

from __future__ import annotations

from intelligence.models import BackendEvidenceBundle, Explanation, XAIResult


class XAIService:
    """References existing Grad-CAM/Re-ID evidence; it does not re-run M2 or M3 models."""

    def build(self, bundle: BackendEvidenceBundle) -> XAIResult:
        explanations: list[Explanation] = []
        for observation in bundle.observations:
            evidence_kinds = ", ".join(sorted({item.kind.value for item in observation.evidence}))
            identity = (
                f"Re-ID linked it to {observation.reid_identity} "
                f"({observation.reid_confidence:.2f})."
                if observation.reid_identity
                else "No Re-ID identity was supplied."
            )
            explanations.append(
                Explanation(
                    event_id=observation.event_id,
                    summary=(
                        f"{observation.species} classification confidence is "
                        f"{observation.detection_confidence:.2f}. {identity} "
                        f"Available evidence: {evidence_kinds or 'none'}."
                    ),
                    species_confidence=observation.detection_confidence,
                    reid_confidence=observation.reid_confidence,
                    evidence=observation.evidence,
                )
            )
        return XAIResult(explanations=explanations)
