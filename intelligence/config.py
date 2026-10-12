"""Small environment-backed settings for the independently deployable M4 service."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    llm_provider: str = "template"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    low_detection_confidence: float = 0.60
    low_reid_confidence: float = 0.65

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            llm_provider=os.getenv("M4_LLM_PROVIDER", "template").lower(),
            ollama_url=os.getenv("M4_OLLAMA_URL", "http://localhost:11434"),
            ollama_model=os.getenv("M4_OLLAMA_MODEL", "llama3.2"),
            low_detection_confidence=float(os.getenv("M4_LOW_DETECTION_CONFIDENCE", "0.60")),
            low_reid_confidence=float(os.getenv("M4_LOW_REID_CONFIDENCE", "0.65")),
        )
