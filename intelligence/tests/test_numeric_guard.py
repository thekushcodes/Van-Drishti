from intelligence.fact_packet import FactPacketBuilder
from intelligence.models import IntelligenceReport, NumericClaim
from intelligence.numeric_guard import NumericGuard


def test_numeric_guard_passes_when_all_report_claims_match_facts(bundle) -> None:
    packet = FactPacketBuilder().build(bundle)
    report = IntelligenceReport(
        title="Validated report",
        narrative="One tiger was recorded.",
        numeric_claims=[NumericClaim(label="unique_tiger_individuals", value=1, unit="animals")],
        generated_by="template",
    )

    validation = NumericGuard().validate(report, packet)

    assert validation.status == "passed"
    assert validation.discrepancies == []


def test_numeric_guard_rejects_unfounded_or_changed_numbers(bundle) -> None:
    packet = FactPacketBuilder().build(bundle)
    report = IntelligenceReport(
        title="Unsafe report",
        narrative="Three tigers were recorded.",
        numeric_claims=[NumericClaim(label="unique_tiger_individuals", value=3, unit="animals")],
        generated_by="template",
    )

    validation = NumericGuard().validate(report, packet)

    assert validation.status == "failed"
    assert validation.discrepancies[0].expected_value == 1
    assert validation.discrepancies[0].claimed_value == 3
