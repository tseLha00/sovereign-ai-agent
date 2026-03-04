# Project documentation index (traceability) (v0.3)

## Version history
- **v0.1** — Initial traceability index created to map criteria, evidence, code, and documentation locations.
- **v0.2** — Refined repository map, evidence references, and documentation navigation for clearer audit traceability.
- **v0.3** — Added final QA coverage, browser-based UI smoke test traceability, and aligned the index with the current repository structure.

## Project
**Name:** Sovereign AI agent demo (Apertus)  
**Goal:** On-prem chatbot demo using Apertus LLM (8B) with:
- OpenAI-style API surface (minimum: `POST /v1/chat/completions`)
- minimal responsive UI
- traceable QA evidence (backend tests, performance baselines, manual UI validation, automated browser smoke test)

## Repository map
- **Docs (criteria + decisions):** `docs/`
- **Backend code:** `backend/`
- **Frontend UI assets:** `frontend/` (served by backend at `/ui/`)
- **Evidence (runs/logs/screenshots):** `evidence/`
- **Browser E2E tests:** `frontend/e2e/`
- **Playwright config:** `frontend/config/playwright.config.ts`
- **Node test config:** `package.json`
- **Model files (local only):** `models/` (do not commit large weights)

## How to navigate
- Criteria documents: `docs/`
- Decisions: `docs/decisions/`
- Evidence: `evidence/`
- Work journal: `docs/journal/`
- Backend tests: `backend/tests/`
- Frontend browser smoke test: `frontend/e2e/`

## Criteria → coverage map

| Criteria | Document | Evidence |
|---|---|---|
| A01 | `docs/A01-scope.md` | kickoff notes under `evidence/meeting-notes/` |
| A02/A03 | `docs/A02-A03-research-log.md` | research sources + runtime/API/UI evidence linked inside log |
| A04 | `docs/A04-timeplan.md` + Excel in `docs/planning/` | timeplan file(s) |
| A05 | `docs/A05-risk-log.md` | meeting notes + runtime evidence + test evidence + commits |
| A12 | `docs/A12-dod-test-concept.md` | `backend/tests/` + `frontend/e2e/` + screenshots |
| H01 | `docs/decisions/H01-runtime-decision.md` | runtime PoC + backend/API/UI validation evidence |
| H08 | `docs/H08-performance-monitoring.md` + `docs/qa/perf-baselines.md` | results in `evidence/perf/` |

## QA / validation overview
The project currently demonstrates four validation layers:

1. **Backend automated API tests (`pytest`)**
   - health endpoint
   - request validation
   - OpenAI-style response shape
   - adapter behavior / error handling as implemented

2. **Performance baseline**
   - repeatable benchmark script
   - timestamped JSON results under `evidence/perf/`

3. **Manual end-to-end smoke validation**
   - backend startup
   - `/health`
   - real `POST /v1/chat/completions`
   - frontend UI behavior in browser

4. **Automated browser smoke test (Playwright)**
   - page loads
   - user message is sent
   - mocked assistant reply is rendered
   - clear action resets the chat

## Versioning rules
- Documents use semantic versions in the title: v0.1 / v0.2 / v0.3
- Decisions: append new sections; keep history.
- Evidence files are timestamped when possible (example): `evidence/perf/YYYY-MM-DD_HHMM_results.json`
- Screenshots should use descriptive names (example): `YYYY-MM-DD_frontend_mui_chat_success.png`

## Notes for final transfer to A4
This markdown documentation is the working source.
For the final A4 document:
- keep the same structure,
- rewrite headings into a more natural narrative style where appropriate,
- keep evidence references explicit,
- and preserve traceability between requirement, implementation, and proof.