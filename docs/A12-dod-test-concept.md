# A12 — Definition of Done (DoD) and test concept (v0.3)

## Version history
- **v0.1** — Initial Definition of Done and test concept created for Sprint 1 baseline (run, tests, perf, and evidence).
- **v0.2** — Clarified test levels, evidence storage, and alignment with the current backend and frontend baseline.
- **v0.3** — Updated the DoD with the real llama.cpp backend path, current automated test evidence, and final UI smoke-check evidence.

## 1. Definition of Done (global)
A backlog item is considered **Done** when all applicable points are satisfied:

### Engineering
- Code is committed and pushed to the repository
- The solution is runnable with documented commands
- Tests pass (`make test` or equivalent)
- If the change affects performance, a perf check is run and results are stored

### Documentation & evidence
- Evidence is stored when relevant (screenshot/log/result JSON)
- Criteria-related documents are updated if the change impacts scope/decisions/research
- The GitHub issue is updated with a short completion comment including evidence links

## 2. Sprint 1 DoD (baseline exit criteria)
Sprint 1 is complete when the following can be demonstrated on the development environment:

### Backend baseline
- Service starts locally with a reproducible command (e.g., `make run`)
- `GET /health` returns `200 {"status":"ok"}`
- `POST /v1/chat/completions` returns an OpenAI-style response shape (non-streaming baseline)
- Adapter abstraction exists (mock adapter used initially)

### Quality baseline
- Contract/API tests exist and pass:
  - `/health`
  - `/v1/chat/completions` response shape
- Performance script runs and stores results under `evidence/perf/` (timestamped JSON)

- ### Current validation status
- Automated tests pass locally (`pytest -q`)
- `GET /health` returns `200 {"status":"ok"}`
- `POST /v1/chat/completions` returns a valid response using the real `llama.cpp` adapter
- The frontend UI loads successfully and supports:
  - message sending
  - clear/reset
  - language selection
  - temperature selection

Evidence:
- `evidence/screenshots/2026-02-26_backend_make_test_pass.png`
- `evidence/screenshots/2026-02-26_backend_health_200_ok.png`
- `evidence/screenshots/2026-02-26_api_llamacpp_curl_success.png`
- `evidence/screenshots/2026-02-26_ui_real_runtime.png`
- `evidence/screenshots/2026-02-26_frontend_language_temperature_controls.png`

## 3. Test concept

### 3.1 Test levels
**Unit tests**
- adapter selection/factory logic (if present)
- request validation and response mapping helpers (if present)

**Contract / API tests (pytest)**
- `/health` returns 200 and expected body
- `/v1/chat/completions` returns:
  - `object = "chat.completion"`
  - `id`, `created`, `model`
  - `choices[0].message.role = "assistant"`
  - `choices[0].message.content` is a non-empty string

**Manual acceptance checks (smoke tests)**
- A user can send a message and receives a response
- Errors are shown in a user-friendly way (status code + readable message)
- UI interaction feels responsive (thinking indicator if needed)

### 3.2 Test data and determinism
- For the mock adapter: deterministic output to keep tests stable
- For the real model: tests validate schema and non-empty output (not exact wording)

## 4. Execution (reproducible commands)
- Run backend: `make run`
- Run tests: `make test`
- Run perf: `make perf`

## 5. Evidence storage
Evidence is kept in the repository to ensure traceability:
- Tests: `backend/tests/`
- Perf results: `evidence/perf/YYYY-MM-DD_HHMM_results.json`
- Issue completion comments: include links to commits and evidence files
