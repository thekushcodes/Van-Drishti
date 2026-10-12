from intelligence.fact_packet import FactPacketBuilder


def test_fact_packet_retains_m1_source_and_traceable_evidence(bundle) -> None:
    packet = FactPacketBuilder().build(bundle)

    assert packet.source_id == "m1-bundle-2026-10-03-001"
    assert packet.location == "North forest corridor"
    assert packet.numeric_facts[0].label == "unique_tiger_individuals"
    assert packet.numeric_facts[0].value == 1
    assert len(packet.evidence) == 3
    assert any(fact.source_event_ids == ["event-001"] for fact in packet.facts)
