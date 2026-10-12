"""Build a traceable M4 Fact Packet from the M1-owned evidence contract."""

from __future__ import annotations

from datetime import UTC, datetime

from intelligence.models import BackendEvidenceBundle, Fact, FactPacket, NumericFact


class FactPacketBuilder:
    """Converts M1 evidence into facts without changing their meaning or values."""

    def build(self, bundle: BackendEvidenceBundle) -> FactPacket:
        facts: list[Fact] = []
        numeric_facts: list[NumericFact] = []

        for count in bundle.counts:
            label = f"unique_{count.species.lower()}_individuals"
            numeric_facts.append(
                NumericFact(label=label, value=count.unique_individuals, unit="animals")
            )
            facts.append(
                Fact(
                    category="count",
                    statement=(
                        f"M1 recorded {count.unique_individuals} unique "
                        f"{count.species} individual(s) in this window."
                    ),
                )
            )

        for observation in bundle.observations:
            facts.append(
                Fact(
                    category="sighting",
                    statement=(
                        f"{observation.species} was detected at "
                        f"{observation.timestamp.isoformat()} with detection confidence "
                        f"{observation.detection_confidence:.2f}."
                    ),
                    source_event_ids=[observation.event_id],
                )
            )
            if observation.reid_identity:
                facts.append(
                    Fact(
                        category="identity",
                        statement=(
                            f"Event {observation.event_id} was associated with "
                            f"identity {observation.reid_identity} at Re-ID confidence "
                            f"{observation.reid_confidence:.2f}."
                        ),
                        source_event_ids=[observation.event_id],
                    )
                )

        for alert in bundle.alerts:
            facts.append(
                Fact(category="alert", statement=f"{alert.severity}: {alert.message}"))

        evidence = [
            evidence_ref
            for observation in bundle.observations
            for evidence_ref in observation.evidence
        ]
        return FactPacket(
            source_id=bundle.source_id,
            created_at=datetime.now(UTC),
            window_start=bundle.window_start,
            window_end=bundle.window_end,
            location=bundle.location,
            facts=facts,
            numeric_facts=numeric_facts,
            evidence=evidence,
        )
