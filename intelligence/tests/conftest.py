from __future__ import annotations

from copy import deepcopy

import pytest

from intelligence.models import BackendEvidenceBundle


@pytest.fixture
def evidence_payload() -> dict:
    return {
        "source_id": "m1-bundle-2026-10-03-001",
        "generated_at": "2026-10-03T12:30:00Z",
        "window_start": "2026-10-03T12:00:00Z",
        "window_end": "2026-10-03T12:30:00Z",
        "camera_id": "cam-north-01",
        "location": "North forest corridor",
        "observations": [
            {
                "event_id": "event-001",
                "timestamp": "2026-10-03T12:05:00Z",
                "species": "tiger",
                "detection_confidence": 0.94,
                "track_id": "track-001",
                "reid_identity": "tiger-17",
                "reid_confidence": 0.88,
                "evidence": [
                    {
                        "evidence_id": "frame-001",
                        "kind": "frame",
                        "uri": "m1://evidence/frame-001.jpg",
                        "description": "Source camera frame",
                    },
                    {
                        "evidence_id": "gradcam-001",
                        "kind": "species_heatmap",
                        "uri": "m2://evidence/gradcam-001.png",
                        "description": "M2 species Grad-CAM overlay",
                    },
                    {
                        "evidence_id": "reid-001",
                        "kind": "reid_similarity",
                        "uri": "m3://evidence/reid-001.json",
                        "description": "M3 Re-ID similarity evidence",
                    },
                ],
            }
        ],
        "counts": [{"species": "tiger", "unique_individuals": 1}],
        "alerts": [],
    }


@pytest.fixture
def bundle(evidence_payload: dict) -> BackendEvidenceBundle:
    return BackendEvidenceBundle.model_validate(deepcopy(evidence_payload))
