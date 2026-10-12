from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from intelligence.fact_packet import FactPacketBuilder
from intelligence.llm import LLMGenerationError, OllamaReportGenerator


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode()


def test_ollama_generator_requests_schema_and_marks_report_as_ollama(bundle) -> None:
    packet = FactPacketBuilder().build(bundle)
    captured: dict = {}

    def fake_urlopen(request, timeout):
        captured["request"] = json.loads(request.data.decode())
        return FakeResponse(
            {
                "response": json.dumps(
                    {
                        "title": "Tiger observation",
                        "narrative": "One tiger was recorded.",
                    }
                )
            }
        )

    with patch("intelligence.llm.generator.urlopen", fake_urlopen):
        report = OllamaReportGenerator("http://127.0.0.1:11434", "llama3.2:1b").generate(packet)

    assert report.generated_by == "ollama"
    assert report.numeric_claims[0].value == 1
    assert captured["request"]["format"]["required"] == ["title", "narrative"]
    assert captured["request"]["options"]["temperature"] == 0


def test_ollama_generator_rejects_a_response_that_does_not_match_the_contract(bundle) -> None:
    packet = FactPacketBuilder().build(bundle)

    with patch(
        "intelligence.llm.generator.urlopen",
        return_value=FakeResponse({"response": json.dumps({"not_a_report": True})}),
    ):
        with pytest.raises(LLMGenerationError):
            OllamaReportGenerator("http://127.0.0.1:11434", "llama3.2:1b").generate(packet)
