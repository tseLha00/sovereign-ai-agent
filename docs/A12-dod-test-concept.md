# A12 — Definition of Done (DoD) and test concept (v0.4)

## Version history
- **v0.1** — Initial Definition of Done and test concept created for Sprint 1 baseline (run, tests, perf, and evidence).
- **v0.2** — Clarified test levels, evidence storage, and alignment with the current backend and frontend baseline.
- **v0.3** — Updated the DoD with the real llama.cpp backend path, current automated test evidence, and final UI smoke-check evidence.
- **v0.4** — Formalized manual end-to-end smoke validation and added one automated browser-based UI smoke test.

## 1. Definition of Done (global)
A backlog item is considered **Done** when all applicable points are satisfied:

### Engineering
- Code is committed and pushed to the repository
- The solution is runnable with documented commands
- Tests pass (`make test`, `pytest`, `npx playwright test`, or equivalent)
- If the change affects performance, a perf check is run and results are stored

### Documentation & evidence
- Evidence is stored when relevant (screenshot/log/result JSON)
- Criteria-related documents are updated if the change impacts scope/decisions/research
- The GitHub issue is updated with a short completion comment including evidence links

---

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

---

## 3. Current validation status
The project has now been validated beyond the Sprint 1 baseline.

### Current confirmed status
- Automated backend tests pass locally (`pytest`)
- `GET /health` returns `200 {"status":"ok"}`
- `POST /v1/chat/completions` returns a valid response using the real `llama.cpp` adapter
- The frontend UI loads successfully and supports:
  - message sending
  - clear/reset
  - language selection
  - temperature selection
- One automated browser smoke test passes (`npx playwright test`)

### Evidence
- `evidence/screenshots/2026-02-26_backend_make_test_pass.png`
- `evidence/screenshots/2026-02-26_backend_health_200_ok.png`
- `evidence/screenshots/2026-02-26_api_llamacpp_curl_success.png`
- `evidence/screenshots/2026-02-26_ui_real_runtime.png`
- `evidence/screenshots/2026-02-26_frontend_language_temperature_controls.png`

Browser test evidence:
- terminal output from `npx playwright test`
- test file: `frontend/e2e/ui-smoke.spec.ts`

---

## 4. Test concept

### 4.1 Test levels

**Unit / component-level checks**
- adapter selection/factory logic (if present)
- request validation and response mapping helpers (if present)
- response cleanup behavior in the `LlamaCppAdapter` as implemented

**Contract / API tests (pytest)**
- `/health` returns 200 and expected body
- `/v1/chat/completions` returns:
  - `object = "chat.completion"`
  - `id`, `created`, `model`
  - `choices[0].message.role = "assistant"`
  - `choices[0].message.content` is a non-empty string
- invalid requests return the expected error handling / schema validation behavior

**Manual end-to-end smoke test**
- backend starts locally
- `/health` responds correctly
- frontend loads through `/ui/`
- user can send a message
- assistant response is rendered in the chat
- clear/reset works
- language selector and temperature selector are visible and usable

**Automated browser smoke test (Playwright)**
- opens `/ui/`
- checks page title / visible UI content
- enters a message
- intercepts the API request with a mocked response
- confirms the user message and assistant reply are rendered
- confirms clear/reset returns the UI to initial state

---

### 4.2 Test data and determinism
- For the mock adapter: deterministic output to keep tests stable
- For the real model: tests validate schema and non-empty output (not exact wording)
- For the browser smoke test: the chat completion response is mocked so the UI test remains deterministic and does not depend on live model generation

---

## 5. Formalized manual E2E smoke test procedure

### Goal
Demonstrate that the complete local demo path works from browser UI to backend response.

### Preconditions
- backend dependencies installed
- server started locally
- frontend served through backend under `/ui/`

### Procedure
1. Start the backend locally.
2. Open the browser at `http://127.0.0.1:8000/ui/`.
3. Verify that the page title and initial assistant greeting are visible.
4. Enter a test message in the input field.
5. Submit the message.
6. Verify that:
   - the user message appears in the chat,
   - an assistant response appears,
   - no blocking error is shown.
7. Verify that the language dropdown is visible and can be changed.
8. Verify that the temperature dropdown is visible and can be changed.
9. Click **Clear**.
10. Verify that the chat resets to the initial greeting state.

### Expected result
The demo UI remains usable and the basic conversation flow works without a crash.

### Manual smoke evidence
- `evidence/screenshots/2026-02-26_ui_real_runtime.png`
- `evidence/screenshots/2026-02-26_frontend_clear_chat_success.png`
- `evidence/screenshots/2026-02-26_frontend_language_temperature_controls.png`

---

## 6. Execution (reproducible commands)
- Run backend (default): `make run`
- Run backend (real adapter): `make run-real` *(or the project’s dedicated real-runtime command if defined)*
- Run tests: `make test`
- Run pytest directly: `pytest -q`
- Run perf: `make perf`
- Run browser smoke test: `npx playwright test`

---

## 7. Evidence storage
Evidence is kept in the repository to ensure traceability:

- Backend tests: `backend/tests/`
- Browser smoke tests: `frontend/e2e/`
- Performance results: `evidence/perf/YYYY-MM-DD_HHMM_results.json`
- Runtime logs / notes: `evidence/runtime/`
- Screenshots: `evidence/screenshots/`

---

## 8. Conclusion
The project now has:
- automated backend validation,
- repeatable performance baseline evidence,
- formalized manual end-to-end smoke validation,
- and one automated browser smoke test.

For the defined IPA demo scope, this is a **solid and defensible QA level**.