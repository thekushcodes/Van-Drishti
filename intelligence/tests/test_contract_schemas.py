from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from intelligence.fact_packet import FactPacketBuilder
from intelligence.models import ReviewItem
from intelligence.service import IntelligenceService
from intelligence.xai import XAIService


CONTRACTS = Path(__file__).resolve().parents[2] / "contracts"


def validate_contract(filename: str, payload: dict) -> None:
    schema = json.loads((CONTRACTS / filename).read_text())
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    assert list(validator.iter_errors(payload)) == []


def test_m1_input_matches_shared_backend_evidence_contract(evidence_payload: dict) -> None:
    validate_contract("backend_evidence.schema.json", evidence_payload)


def test_m4_outputs_match_shared_contracts(bundle) -> None:
    packet = FactPacketBuilder().build(bundle)
    run = IntelligenceService().create_run(bundle)

    validate_contract("fact_packet.schema.json", packet.model_dump(mode="json"))
    validate_contract("report.schema.json", run.report.model_dump(mode="json"))
    validate_contract("xai.schema.json", XAIService().build(bundle).model_dump(mode="json"))

    review = ReviewItem(
        run_id=run.run_id,
        reason="Example only",
        created_at=run.created_at,
    )
    validate_contract("review.schema.json", review.model_dump(mode="json"))
