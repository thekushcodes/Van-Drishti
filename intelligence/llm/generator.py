"""Report-generator interface and local implementations for M4."""

from __future__ import annotations

import json
from typing import Protocol
from urllib.error import URLError
from urllib.request import Request, urlopen

from intelligence.models import FactPacket, IntelligenceReport, NumericClaim


class LLMGenerationError(RuntimeError):
    """Raised when the configured local LLM cannot produce the report contract."""


class ReportGenerator(Protocol):
    def generate(self, packet: FactPacket) -> IntelligenceReport: ...


# A schema is sent to Ollama instead of the weaker `format: "json"` instruction.
# It keeps small local models focused on wording only. M4 owns every numeric
# claim by copying it from the Fact Packet, so model-invented numeric values
# cannot cross the M4 report boundary.
OLLAMA_REPORT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "title": {"type": "string", "minLength": 1},
        "narrative": {"type": "string", "minLength": 1},
    },
    "required": ["title", "narrative"],
}


class TemplateReportGenerator:
    """Deterministic local report generator used by default and as the safe fallback."""

    def __init__(self, generated_by: str = "template") -> None:
        if generated_by not in {"template", "fallback_template"}:
            raise ValueError("Template reports must use template or fallback_template")
        self.generated_by = generated_by

    def generate(self, packet: FactPacket) -> IntelligenceReport:
        location = f" at {packet.location}" if packet.location else ""
        count_sentences = [
            f"{int(fact.value) if fact.value.is_integer() else fact.value} {fact.unit} "
            f"for {fact.label.replace('_', ' ')}"
            for fact in packet.numeric_facts
        ]
        summary = "; ".join(count_sentences) if count_sentences else "No count facts were supplied"
        narrative = (
            f"VanDrishti observation summary{location}: {summary}. "
            f"The report is based on {len(packet.facts)} traceable fact(s) and "
            f"{len(packet.evidence)} evidence reference(s)."
        )
        return IntelligenceReport(
            title="VanDrishti observation report",
            narrative=narrative,
            numeric_claims=[
                NumericClaim(label=fact.label, value=fact.value, unit=fact.unit)
                for fact in packet.numeric_facts
            ],
            generated_by=self.generated_by,
        )


class OllamaReportGenerator:
    """Uses a local Ollama server only; it never sends facts to a cloud service."""

    def __init__(self, base_url: str, model: str = "llama3.2", timeout_seconds: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    def generate(self, packet: FactPacket) -> IntelligenceReport:
        prompt = {
            "instruction": (
                "Create a concise wildlife observation title and narrative using only the fact packet. "
                "Return only JSON matching the supplied response schema. "
                "Do not return numeric_claims: M4 supplies verified numeric claims itself."
            ),
            "fact_packet": packet.model_dump(mode="json"),
        }
        request = Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(
                {
                    "model": self.model,
                    "prompt": json.dumps(prompt),
                    "format": OLLAMA_REPORT_SCHEMA,
                    "options": {"temperature": 0},
                    "stream": False,
                }
            ).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:  # nosec B310 -- local URL set by deployer
                response_body = json.loads(response.read().decode())
            generated = json.loads(response_body["response"])
            generated["numeric_claims"] = [
                {"label": fact.label, "value": fact.value, "unit": fact.unit}
                for fact in packet.numeric_facts
            ]
            generated["generated_by"] = "ollama"
            return IntelligenceReport.model_validate(generated)
        except (KeyError, TypeError, ValueError, URLError, OSError) as exc:
            raise LLMGenerationError(f"Local Ollama report generation failed: {exc}") from exc
