from intelligence.llm import LLMGenerationError, ReportGenerator, TemplateReportGenerator
from intelligence.models import FactPacket, IntelligenceReport, NumericClaim
from intelligence.service import IntelligenceService


def test_end_to_end_pipeline_returns_report_and_xai(bundle) -> None:
    # Unit tests must not depend on whether a developer has Ollama enabled in .env.
    run = IntelligenceService(generator=TemplateReportGenerator()).create_run(bundle)

    assert run.status == "complete"
    assert run.numeric_validation.status == "passed"
    assert run.report.generated_by == "template"
    assert run.report.numeric_claims[0].value == 1
    assert run.xai.explanations[0].event_id == "event-001"
    assert run.xai.explanations[0].evidence[1].kind.value == "species_heatmap"


class IncorrectNumberGenerator:
    def generate(self, packet: FactPacket) -> IntelligenceReport:
        return IntelligenceReport(
            title="Incorrect generated report",
            narrative="It claims a number not present in the facts.",
            numeric_claims=[NumericClaim(label="unique_tiger_individuals", value=99, unit="animals")],
            generated_by="template",
        )


def test_numeric_failure_uses_safe_fallback_and_enters_review(bundle) -> None:
    run = IntelligenceService(generator=IncorrectNumberGenerator()).create_run(bundle)

    assert run.status == "requires_review"
    assert run.numeric_validation.status == "failed"
    assert run.report.generated_by == "fallback_template"
    assert run.report.numeric_claims[0].value == 1
    assert any("Numeric Guard" in item.reason for item in run.review_items)


class UnavailableGenerator:
    def generate(self, packet: FactPacket) -> IntelligenceReport:
        raise LLMGenerationError("Ollama is unavailable")


def test_llm_outage_returns_safe_report_and_review_item(bundle) -> None:
    run = IntelligenceService(generator=UnavailableGenerator()).create_run(bundle)

    assert run.status == "requires_review"
    assert run.report.generated_by == "fallback_template"
    assert run.numeric_validation.status == "passed"
    assert any("Local LLM was unavailable" in item.reason for item in run.review_items)
