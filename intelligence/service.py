"""The M4 application service: Fact Packet -> LLM -> Numeric Guard -> XAI -> Review."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from intelligence.config import Settings
from intelligence.fact_packet import FactPacketBuilder
from intelligence.llm import (
    LLMGenerationError,
    OllamaReportGenerator,
    ReportGenerator,
    TemplateReportGenerator,
)
from intelligence.models import BackendEvidenceBundle, IntelligenceRun, ReviewItem
from intelligence.numeric_guard import NumericGuard
from intelligence.review import ReviewService
from intelligence.xai import XAIService


class RunNotFoundError(KeyError):
    pass


class InMemoryRunRepository:
    """Replace with an M4-owned persistence adapter when durable storage is provisioned.

    This intentionally does not connect to M1's database; M1/M4 communicate by contract.
    """

    def __init__(self) -> None:
        self._runs: dict[UUID, IntelligenceRun] = {}

    def save(self, run: IntelligenceRun) -> IntelligenceRun:
        self._runs[run.run_id] = run
        return run

    def get(self, run_id: UUID) -> IntelligenceRun:
        try:
            return self._runs[run_id]
        except KeyError as exc:
            raise RunNotFoundError(str(run_id)) from exc

    def review_items(self, status: str | None = None) -> list[ReviewItem]:
        items = [item for run in self._runs.values() for item in run.review_items]
        return [item for item in items if status is None or item.status == status]

    def resolve_review_item(self, review_id: UUID, resolution_note: str) -> ReviewItem:
        for run_id, run in self._runs.items():
            for index, item in enumerate(run.review_items):
                if item.review_id == review_id:
                    resolved = item.model_copy(
                        update={"status": "resolved", "resolution_note": resolution_note}
                    )
                    self._runs[run_id] = run.model_copy(
                        update={
                            "review_items": [
                                resolved if candidate.review_id == review_id else candidate
                                for candidate in run.review_items
                            ]
                        }
                    )
                    return resolved
        raise RunNotFoundError(str(review_id))


class IntelligenceService:
    def __init__(
        self,
        generator: ReportGenerator | None = None,
        repository: InMemoryRunRepository | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.settings = settings or Settings.from_environment()
        self.generator = generator or self._generator_from_settings(self.settings)
        self.repository = repository or InMemoryRunRepository()
        self.fact_packet_builder = FactPacketBuilder()
        self.numeric_guard = NumericGuard()
        self.xai_service = XAIService()
        self.review_service = ReviewService(
            low_detection_confidence=self.settings.low_detection_confidence,
            low_reid_confidence=self.settings.low_reid_confidence,
        )

    @staticmethod
    def _generator_from_settings(settings: Settings) -> ReportGenerator:
        if settings.llm_provider == "template":
            return TemplateReportGenerator()
        if settings.llm_provider == "ollama":
            return OllamaReportGenerator(settings.ollama_url, model=settings.ollama_model)
        raise ValueError("M4_LLM_PROVIDER must be either 'template' or 'ollama'")

    def create_run(self, bundle: BackendEvidenceBundle) -> IntelligenceRun:
        packet = self.fact_packet_builder.build(bundle)
        system_review_reason: str | None = None
        try:
            generated_report = self.generator.generate(packet)
            numeric_validation = self.numeric_guard.validate(generated_report, packet)
            report = generated_report
        except LLMGenerationError:
            # A local-model outage must not make M1's API call fail or expose an
            # unvalidated result. M5 receives a deterministic report and a review task.
            report = TemplateReportGenerator(generated_by="fallback_template").generate(packet)
            numeric_validation = self.numeric_guard.validate(report, packet)
            system_review_reason = (
                "Local LLM was unavailable or returned an invalid report. "
                "A safe template report was used; verify before operational use."
            )

        if numeric_validation.status == "failed":
            # The unsafe report is never exposed as the completed report.
            report = TemplateReportGenerator(generated_by="fallback_template").generate(packet)

        run_id = uuid4()
        review_items = self.review_service.create_items(
            run_id, bundle, numeric_validation, system_review_reason
        )
        run = IntelligenceRun(
            run_id=run_id,
            created_at=datetime.now(UTC),
            status="requires_review" if review_items else "complete",
            fact_packet=packet,
            report=report,
            numeric_validation=numeric_validation,
            xai=self.xai_service.build(bundle),
            review_items=review_items,
        )
        return self.repository.save(run)

    def get_run(self, run_id: UUID) -> IntelligenceRun:
        return self.repository.get(run_id)

    def get_review_items(self, status: str | None = None) -> list[ReviewItem]:
        return self.repository.review_items(status)

    def resolve_review_item(self, review_id: UUID, resolution_note: str) -> ReviewItem:
        return self.repository.resolve_review_item(review_id, resolution_note)
