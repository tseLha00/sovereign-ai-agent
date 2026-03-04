# Work journal — Day 05 (2026-02-20)

## Focus of the day
Start of Sprint 2: move from the Sprint 1 mock baseline to the real runtime integration path.

## Planned work
- Continue runtime integration preparation for the real model
- Refine adapter structure for `llama.cpp`
- Prepare next implementation steps for real inference through the existing API
- Continue documentation updates for Sprint 2 progress

## Work completed
- Reviewed the existing adapter architecture from Sprint 1 (`base.py`, `factory.py`, `mock.py`)
- Prepared the transition from the mock adapter to the real `llama.cpp` adapter while keeping the same OpenAI-style API contract
- Worked on the implementation approach for `LlamaCppAdapter`, including:
  - model path handling
  - prompt construction from chat messages
  - subprocess execution strategy for `llama-cli`
  - response cleanup approach for terminal output
- Verified that the backend structure still supports replacing the adapter without changing the public endpoint
- Updated project documentation so that Sprint 2 work remains traceable and aligned with H01/A02-A03

## Problems / deviations
- No major blocker, but the work required more design attention than expected because the runtime output from `llama.cpp` is noisier than a normal API response and needs cleanup before it can be returned to the frontend.

## Decisions made
- The OpenAI-style response shape must remain unchanged even after switching from mock to real inference.
- Response extraction and sanitization must be handled inside the adapter, not in the endpoint logic.

## What I learned today
- A stable adapter boundary is important because it lets me replace the inference backend without rewriting the API.
- Local LLM runtime integration is not only about “running the model”; output cleaning and predictable response formatting are part of the engineering work.

## Evidence / references
- Backend source files under `backend/src/sai_backend/adapters/`
- Decision document: `docs/decisions/H01-runtime-decision.md`
- Related scope / tracking docs updated during Sprint 2 preparation