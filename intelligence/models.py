"""Pydantic models implementing the M1-to-M4 and M4-to-M5 contracts."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvidenceKind(str, Enum):
    DETECTION_BOX = "detection_box"
    SPECIES_HEATMAP = "species_heatmap"
    REID_SIMILARITY = "reid_similarity"
    FRAME = "frame"
    OTHER = "other"


class EvidenceReference(ContractModel):
    evidence_id: str = Field(min_length=1)
    kind: EvidenceKind
    uri: str = Field(min_length=1)
    description: str | None = None


class Observation(ContractModel):
    event_id: str = Field(min_length=1)
    timestamp: datetime
    species: str = Field(min_length=1)
    detection_confidence: float = Field(ge=0, le=1)
    track_id: str | None = None
    reid_identity: str | None = None
    reid_confidence: float | None = Field(default=None, ge=0, le=1)
    evidence: list[EvidenceReference] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_reid_confidence_with_identity(self) -> "Observation":
        if self.reid_identity and self.reid_confidence is None:
            raise ValueError("reid_confidence is required when reid_identity is supplied")
        return self


class SpeciesCount(ContractModel):
    species: str = Field(min_length=1)
    unique_individuals: int = Field(ge=0)


class Alert(ContractModel):
    alert_id: str = Field(min_length=1)
    severity: Literal["low", "medium", "high"]
    message: str = Field(min_length=1)


class BackendEvidenceBundle(ContractModel):
    """The M1 API payload delivered to M4."""

    source_id: str = Field(min_length=1)
    generated_at: datetime
    window_start: datetime
    window_end: datetime
    camera_id: str | None = None
    location: str | None = None
    observations: list[Observation] = Field(default_factory=list)
    counts: list[SpeciesCount] = Field(default_factory=list)
    alerts: list[Alert] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_window(self) -> "BackendEvidenceBundle":
        if self.window_end < self.window_start:
            raise ValueError("window_end must be at or after window_start")
        return self


class Fact(ContractModel):
    fact_id: UUID = Field(default_factory=uuid4)
    category: Literal["sighting", "identity", "count", "alert"]
    statement: str = Field(min_length=1)
    source_event_ids: list[str] = Field(default_factory=list)


class NumericFact(ContractModel):
    fact_id: UUID = Field(default_factory=uuid4)
    label: str = Field(min_length=1)
    value: float
    unit: str = Field(min_length=1)


class FactPacket(ContractModel):
    packet_id: UUID = Field(default_factory=uuid4)
    source_id: str
    created_at: datetime
    window_start: datetime
    window_end: datetime
    location: str | None = None
    facts: list[Fact]
    numeric_facts: list[NumericFact]
    evidence: list[EvidenceReference]


class NumericClaim(ContractModel):
    label: str = Field(min_length=1)
    value: float
    unit: str = Field(min_length=1)


class IntelligenceReport(ContractModel):
    title: str = Field(min_length=1)
    narrative: str = Field(min_length=1)
    numeric_claims: list[NumericClaim] = Field(default_factory=list)
    generated_by: Literal["template", "ollama", "fallback_template"]


class NumericDiscrepancy(ContractModel):
    label: str
    claimed_value: float
    expected_value: float | None = None
    unit: str
    reason: str


class NumericValidation(ContractModel):
    status: Literal["passed", "failed"]
    discrepancies: list[NumericDiscrepancy] = Field(default_factory=list)


class Explanation(ContractModel):
    event_id: str
    summary: str
    species_confidence: float = Field(ge=0, le=1)
    reid_confidence: float | None = Field(default=None, ge=0, le=1)
    evidence: list[EvidenceReference] = Field(default_factory=list)


class XAIResult(ContractModel):
    explanations: list[Explanation] = Field(default_factory=list)


class ReviewItem(ContractModel):
    review_id: UUID = Field(default_factory=uuid4)
    run_id: UUID
    event_id: str | None = None
    reason: str
    status: Literal["open", "resolved"] = "open"
    created_at: datetime
    resolution_note: str | None = None


class ReviewResolution(ContractModel):
    resolution_note: str = Field(min_length=1)


class IntelligenceRun(ContractModel):
    run_id: UUID = Field(default_factory=uuid4)
    created_at: datetime
    status: Literal["complete", "requires_review"]
    fact_packet: FactPacket
    report: IntelligenceReport
    numeric_validation: NumericValidation
    xai: XAIResult
    review_items: list[ReviewItem] = Field(default_factory=list)
