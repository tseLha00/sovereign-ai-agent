# Sprint 1 Review + Retro — 2026-02-19

## Participants
- Supervisor: Enrico Viola
- Apprentice: Tsering Lhamo Anodunkhartsang

## Sprint 1 goal
Deliver a working baseline + evidence discipline:
- backend skeleton + adapter architecture (mock)
- `/health` endpoint
- `POST /v1/chat/completions` OpenAI-style shape
- contract tests (pytest)
- perf script + stored JSON result
- documentation: A01/A02-A03/A04/A05/A12/H01/H08

## Demo / evidence shown
- Backend running locally:
  - `/health` returns OK
  - `/v1/chat/completions` returns stable OpenAI-style response shape
- Tests:
  - `make test` passes (pytest contract tests)
- Performance:
  - `make perf` produces JSON under `evidence/perf/`

(Reference exact files:)
- `evidence/perf/<timestamp>_results.json`
- `evidence/screenshots/` (optional)
- `docs/` (A01/A02-A03/A04/A05/A12/H01/H08)

## What went well
- Clear scope + clean baseline delivered early.
- Evidence discipline established (perf JSON, test runs).
- Runtime decision direction clarified (llama.cpp + GGUF path).

## What didn’t go well / friction
- Early setup friction (git identity/auth).
- Perf run initially failed due to backend not running (fixed via documentation).

## Improvements for Sprint 2
- Timebox runtime integration steps (download GGUF, run llama.cpp, wire adapter).
- Add minimal UI improvements early (thinking state, errors, reset).
- Keep evidence paths at repo root consistent.

## Action items (Sprint 2 backlog seed)
- PoC: llama.cpp + GGUF + one prompt with screenshot/log.
- Adapter: real inference integration behind existing API.
- UI: responsive chat + latency mitigation + error handling.
- Compare perf results baseline vs real inference.
