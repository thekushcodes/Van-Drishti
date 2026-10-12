from fastapi.testclient import TestClient

from intelligence.api.app import create_app
from intelligence.llm import TemplateReportGenerator
from intelligence.service import IntelligenceService


def template_client() -> TestClient:
    """Keep contract/API tests independent of a developer's local LLM configuration."""
    return TestClient(create_app(IntelligenceService(generator=TemplateReportGenerator())))


def test_m1_to_m4_then_m4_to_m5_api_flow(evidence_payload: dict) -> None:
    client = template_client()

    health = client.get("/health")
    created = client.post("/api/v1/intelligence/runs", json=evidence_payload)

    assert health.status_code == 200
    assert created.status_code == 201
    body = created.json()
    assert body["status"] == "complete"
    assert body["report"]["numeric_claims"][0]["value"] == 1

    fetched = client.get(f"/api/v1/intelligence/runs/{body['run_id']}")
    assert fetched.status_code == 200
    assert fetched.json()["fact_packet"]["source_id"] == evidence_payload["source_id"]


def test_review_api_exposes_and_resolves_low_confidence_case(evidence_payload: dict) -> None:
    evidence_payload["observations"][0]["detection_confidence"] = 0.40
    client = template_client()
    created = client.post("/api/v1/intelligence/runs", json=evidence_payload)

    assert created.status_code == 201
    assert created.json()["status"] == "requires_review"
    review_id = created.json()["review_items"][0]["review_id"]

    queue = client.get("/api/v1/intelligence/review-items?status=open")
    resolved = client.post(
        f"/api/v1/intelligence/review-items/{review_id}/resolve",
        json={"resolution_note": "Field team verified the sighting."},
    )

    assert len(queue.json()) == 1
    assert resolved.status_code == 200
    assert resolved.json()["status"] == "resolved"


def test_api_rejects_invalid_m1_contract_and_invalid_review_filter(evidence_payload: dict) -> None:
    client = template_client()
    evidence_payload.pop("source_id")

    invalid_bundle = client.post("/api/v1/intelligence/runs", json=evidence_payload)
    invalid_filter = client.get("/api/v1/intelligence/review-items?status=waiting")

    assert invalid_bundle.status_code == 422
    assert invalid_filter.status_code == 422
