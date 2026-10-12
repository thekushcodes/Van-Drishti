# VanDrishti M4: integration boundary and GitHub ownership

This module implements the final simple architecture only. Its fixed hand-off is:

```text
M2 detection/species -> M3 tracking/Re-ID/counting -> M1 backend
                                                     |
                                                     | POST M1 evidence bundle
                                                     v
Fact Packet -> Local LLM -> Numeric Guard -> XAI -> Review Queue
                                                     |
                                                     | GET completed run / review queue
                                                     v
                                                M5 dashboard
```

## API ownership and flow

| From | Endpoint / contract | To | Purpose |
| --- | --- | --- | --- |
| M1 | `POST /api/v1/intelligence/runs` with `contracts/backend_evidence.schema.json` | M4 | Submit a stored evidence bundle. |
| M4 | `GET /api/v1/intelligence/runs/{run_id}` | M5 | Retrieve the report, numeric validation, XAI evidence, and review state. |
| M4 | `GET /api/v1/intelligence/review-items?status=open` | M5/reviewer | Display the human review queue. |
| M5/reviewer | `POST /api/v1/intelligence/review-items/{review_id}/resolve` | M4 | Record the human decision. |

M4 never reads M1's database and never re-runs M2 or M3 models. It preserves their evidence references (for example, a Grad-CAM image or Re-ID similarity result) in its XAI output.

## Local Ollama report contract

When `M4_LLM_PROVIDER=ollama`, M4 sends the Fact Packet to the local Ollama
server at `M4_OLLAMA_URL`. It supplies the exact JSON schema of the report
payload and uses deterministic generation, so a small local model must return
the required title and narrative fields. M4 owns the `generated_by: "ollama"`
marker and copies numeric claims only from the Fact Packet before Numeric Guard
verifies them. An unavailable or malformed local-model response uses the safe
template fallback and creates a review item.

## Contracts

`contracts/` is shared integration surface, not a private M4 implementation detail.

- `backend_evidence.schema.json` is the M1 -> M4 input.
- `fact_packet.schema.json`, `report.schema.json`, `xai.schema.json`, and `review.schema.json` are M4 outputs consumed by M5.
- A contract change needs an agreed pull request, updates to producers and consumers, and passing contract tests before merging.

## Feature-branch ownership

The initial bootstrap can be committed to `feature/m4-llm`. Subsequent work should remain inside these ownership boundaries:

| Feature branch | Owned paths | Pull-request checks |
| --- | --- | --- |
| `feature/m4-llm` | `intelligence/fact_packet/`, `intelligence/llm/`, `intelligence/api/`, input/report contracts | fact-packet, LLM, API and contract tests |
| `feature/m4-xai` | `intelligence/xai/`, `contracts/xai.schema.json` | XAI and contract tests |
| `feature/m4-review` | `intelligence/numeric_guard/`, `intelligence/review/`, `contracts/review.schema.json` | guard, review, API and contract tests |

Each branch follows `feature/* -> pull request -> develop -> integration test -> main`. Do not push directly to `main`. A branch may update another branch's owned contract only with the affected owner’s approval.
