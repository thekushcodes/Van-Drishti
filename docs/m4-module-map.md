# M4 Intelligence module map

## What M4 owns

M4 receives one validated evidence bundle from M1 and returns an intelligence result for M5. The result contains a report, numeric validation, XAI explanations, and any human-review items.

```text
M1 evidence
    -> M4 API
    -> Fact Packet
    -> Report generator
    -> Numeric Guard
    -> XAI explanation
    -> Review queue
    -> M5 dashboard
```

M4 never reads the M1 database and never reruns M2 or M3 models. It uses the evidence references that M1 supplies.

## Code map

| Path | Responsibility | Used by |
| --- | --- | --- |
| `intelligence/models.py` | Defines M4 input, output, report, evidence, XAI, and review data objects. | Every M4 component |
| `intelligence/config.py` | Reads the selected LLM provider, Ollama URL/model, and review thresholds from environment variables. | `service.py` |
| `intelligence/api/app.py` | Provides `/health`, run creation/read, review-list, and review-resolution endpoints. | M1, M5, reviewers |
| `intelligence/service.py` | Runs the complete pipeline and stores runs in the M4-owned in-memory repository. | API |
| `intelligence/fact_packet/builder.py` | Builds traceable facts and verified numeric facts from the M1 bundle. | Pipeline |
| `intelligence/llm/generator.py` | Produces report wording using the safe template or local Ollama. | Pipeline |
| `intelligence/numeric_guard/guard.py` | Compares report numeric claims against verified Fact Packet numeric facts. | Pipeline |
| `intelligence/xai/service.py` | Gives M5 a readable explanation and the original evidence links. | Pipeline, M5 |
| `intelligence/review/service.py` | Creates review items when confidence is low or the local model falls back. | Pipeline, reviewers |
| `contracts/*.schema.json` | Defines the agreed JSON format exchanged between M1, M4, and M5. | M1, M4, M5 |
| `intelligence/tests/` | Proves the component, API, contract, and full-pipeline behaviour. | GitHub Actions |

## Local LLM safety design

`intelligence/llm/generator.py` gives Ollama a strict response schema. The local model writes only a report title and narrative. M4 copies numeric claims directly from the Fact Packet, then Numeric Guard validates them.

This prevents a language model from adding unverified values such as confidence scores as report numeric claims. If the local model is unavailable or returns an invalid response, M4 returns a safe template report and creates a review item.

The behaviour is tested in `intelligence/tests/test_ollama_generator.py`.

## Test map

| Test file | What it proves |
| --- | --- |
| `test_fact_packet_builder.py` | M1 evidence becomes traceable facts. |
| `test_numeric_guard.py` | Unverified or mismatched numeric claims are rejected. |
| `test_ollama_generator.py` | Ollama receives the strict schema and cannot own numeric claims. |
| `test_contract_schemas.py` | Shared JSON contracts remain valid. |
| `test_pipeline.py` | The complete M4 pipeline handles normal and review cases. |
| `test_api.py` | M1 and M5 can use the public API endpoints. |

Run all tests with:

```bash
pytest
```

GitHub runs the same suite through `.github/workflows/m4-tests.yml` for pull requests to `develop` and `main`.

## Reading order for a new teammate

1. Read `README.md` for the project and folder overview.
2. Read `docs/m4-integration.md` for API and contract ownership.
3. Read this file for the code and test map.
4. Open `intelligence/service.py` to follow the complete M4 execution path.
5. Open `intelligence/api/app.py` to see the endpoints used by M1 and M5.
