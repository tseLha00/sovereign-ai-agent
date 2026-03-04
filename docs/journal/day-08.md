# Work journal — Day 08 (2026-02-26)

## Focus of the day
Major implementation and validation day: finalize the real runtime path and validate backend + frontend with evidence.

## Planned work
- Validate `llama.cpp` runtime locally
- Verify backend endpoint with the real adapter
- Finalize the MUI-based frontend demo UI
- Collect screenshots and runtime evidence
- Update documentation with real implementation evidence

## Work completed
- Ran the official `llama.cpp` proof of concept locally with the selected GGUF model
- Confirmed the model loads and responds successfully to a minimal prompt
- Validated the backend with the real adapter by calling `POST /v1/chat/completions`
- Confirmed that the backend returns `200 OK` with the expected OpenAI-style response shape while using real inference
- Finalized the browser-based frontend demo UI served at `/ui/`
- Implemented / validated frontend features:
  - chat display
  - sending messages
  - clear/reset chat
  - language selector
  - temperature selector
  - MUI component-based rendering
- Collected and organized screenshot evidence for:
  - runtime success
  - backend health/API success
  - test pass output
  - frontend UI success
  - language and temperature controls
  - clear/reset behavior
- Updated documentation so that the real runtime integration is reflected in:
  - A02/A03
  - A05
  - A12
  - H01

## Problems / deviations
- During validation, I observed that raw runtime diagnostics could leak into the UI if response cleaning was not strict enough.
- This required additional refinement of the response extraction logic.

## Decisions made
- Only cleaned assistant text may be returned from the adapter.
- The collected screenshots must be curated so only the strongest and least redundant evidence remains in the final documentation.

## What I learned today
- Evidence collection must happen immediately after successful runs; otherwise it becomes difficult to reconstruct clean proof later.
- The same feature may need several validation angles: runtime, backend API, UI behavior, and automated tests.

## Evidence / references
- `evidence/runtime/2026-02-26_llamacpp_run.log`
- `evidence/runtime/2026-02-26_llamacpp_note.md`
- `evidence/screenshots/2026-02-26_llamacpp_success.png`
- `evidence/screenshots/2026-02-26_api_llamacpp_curl_success.png`
- `evidence/screenshots/2026-02-26_backend_health_200_ok.png`
- `evidence/screenshots/2026-02-26_backend_make_test_pass.png`
- `evidence/screenshots/2026-02-26_frontend_language_temperature_controls.png`
- `evidence/screenshots/2026-02-26_frontend_clear_chat_success.png`
- `evidence/screenshots/2026-02-26_ui_real_runtime.png`