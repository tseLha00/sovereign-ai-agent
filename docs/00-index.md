# Project documentation index (traceability) (v0.2)

## Project
**Name:** Sovereign AI agent demo (Apertus)  
**Goal:** On-prem chatbot demo using Apertus LLM (8B) with:
- OpenAI-style API surface (minimum: `POST /v1/chat/completions`)
- minimal responsive UI

## Repository map
- **Docs (criteria + decisions):** `docs/`
- **Backend code:** `backend/`
- **Frontend UI assets:** `frontend/` (served by backend at `/ui/`)
- **Evidence (runs/logs/screenshots):** `evidence/`
- **Model files (local only):** `models/` (do not commit large weights)

## How to navigate
- Criteria documents: `docs/` (Axx + Hxx)
- Decisions: `docs/decisions/`
- Evidence: `evidence/`
- Work journal: `docs/journal/`

## Criteria → coverage map
| Criteria | Document | Evidence |
|---|---|---|
| A01 | `docs/A01-scope.md` | kickoff notes under `evidence/meeting-notes/` |
| A02/A03 | `docs/A02-A03-research-log.md` | sources linked inside log |
| A04 | `docs/A04-timeplan.md` + Excel in `docs/planning/` | timeplan file(s) |
| A05 | `docs/A05-risk-log.md` | meeting notes + perf JSON + commits |
| A12 | `docs/A12-dod-test-concept.md` | tests in `backend/tests/` |
| H01 | `docs/decisions/H01-runtime-decision.md` | research log + runtime PoC evidence when executed |
| H08 | `docs/H08-performance-monitoring.md` | results in `docs/qa/perf-baselines.md` + `evidence/perf/` |

## Versioning rules
- Documents use semantic versions in the title: v0.1 / v0.2 / v0.3
- Decisions: append new sections; keep history.
- Evidence files are timestamped (example): `evidence/perf/YYYY-MM-DD_HHMM_results.json`
