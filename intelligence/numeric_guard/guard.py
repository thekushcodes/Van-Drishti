"""Ensure every reported number comes from a named Fact Packet numeric fact."""

from __future__ import annotations

from intelligence.models import FactPacket, IntelligenceReport, NumericDiscrepancy, NumericValidation


class NumericGuard:
    def validate(self, report: IntelligenceReport, packet: FactPacket) -> NumericValidation:
        expected = {(fact.label, fact.unit): fact.value for fact in packet.numeric_facts}
        discrepancies: list[NumericDiscrepancy] = []

        for claim in report.numeric_claims:
            key = (claim.label, claim.unit)
            fact_value = expected.get(key)
            if fact_value is None:
                discrepancies.append(
                    NumericDiscrepancy(
                        label=claim.label,
                        claimed_value=claim.value,
                        expected_value=None,
                        unit=claim.unit,
                        reason="No matching numeric fact exists in the Fact Packet.",
                    )
                )
            elif claim.value != fact_value:
                discrepancies.append(
                    NumericDiscrepancy(
                        label=claim.label,
                        claimed_value=claim.value,
                        expected_value=fact_value,
                        unit=claim.unit,
                        reason="Claimed value differs from the Fact Packet.",
                    )
                )

        return NumericValidation(
            status="failed" if discrepancies else "passed", discrepancies=discrepancies
        )
