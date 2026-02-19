# Project documentation index (traceability)

## Project
**Name:** Sovereign AI agent demo (Apertus)  
**Goal:** On-prem chatbot demo using Apertus LLM (8B) with an OpenAI-style API surface and a minimal responsive UI.

## How to navigate
- **Criteria documents:** `docs/` (Axx + Hxx)
- **Decisions:** `docs/decisions/`
- **Evidence (runs, logs, screenshots):** `evidence/`
- **Work journal:** `docs/journal/`
- **Code:** `backend/` and `frontend/` (frontend TBD)

## Criteria → where it is covered
| Criteria | Document | Evidence (if applicable) |
|---|---|---|
| A01 | `docs/A01-scope.md` | `evidence/meeting-notes/` (kickoff/decisions notes) |
| A02/A03 | `docs/A02-A03-research-log.md` | sources linked inside the log |
| A04 | `docs/A04-timeplan.md` + Excel Gantt | `planning/Timeplan.xlsx` (or wherever stored) |
| A05 | `docs/A05-risk-log.md` | Soll/Ist in timeplan + issue history + deviations table |
| A12 | `docs/A12-dod-test-concept.md` | `evidence/tests/` (optional) + `backend/tests/` |
| H01 | `docs/decisions/H01-runtime-decision.md` | research refs + PoC evidence when done |
| H08 | `docs/H08-performance-monitoring.md` | `evidence/perf/*.json` |

## Versioning rules
- Documents use semantic versions in the title: **v0.1 / v0.2 / v0.3**
- Decisions: update by appending a new “Decision update” section (keep history).
- Evidence files are timestamped (e.g., `YYYY-MM-DD_HHMM_results.json`).
