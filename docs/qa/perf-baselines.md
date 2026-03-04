# Performance baselines (H08 evidence) (v0.2)

## Version history
- **v0.1** — Initial baseline evidence table created with Sprint 1 mock-adapter benchmark results.
- **v0.2** — Clarified benchmark scope, separated mock baseline evidence from real-runtime functional validation, and aligned the interpretation with the actual project state.

## Purpose
This document records the available repeatable benchmark runs and links them to the raw JSON evidence files.

## Baseline runs

| Date | Adapter | Requests | Concurrency | p50 (ms) | p90 (ms) | p95 (ms) | Errors | Evidence JSON |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 2026-02-18 13:32 | mock | 100 | 10 | 5 | 10 | 11 | 0 | `evidence/perf/2026-02-18_1332_results.json` |
| 2026-02-19 04:23 | mock | 100 | 10 | 6 | 14 | 26 | 0 | `evidence/perf/2026-02-19_0423_results.json` |

## Summary
- Both recorded benchmark runs were executed with the **mock adapter**
- Status codes in both runs were successful
- The recorded results provide a stable baseline for backend/API overhead

## Throughput
- 2026-02-18 13:32 → `214.15 rps`
- 2026-02-19 04:23 → `403.19 rps`

## Interpretation
These values:
- are valid for the mock adapter
- show that the backend path and benchmark mechanism work
- do **not** measure the full generation latency of the real Apertus runtime

## Real-runtime note
The real `llama.cpp` runtime was validated functionally, but no directly comparable repeatable benchmark JSON has yet been added to this table.

Therefore:
- benchmark evidence = currently **mock only**
- functional runtime evidence = documented separately in screenshots and runtime logs

## Related functional evidence
- `evidence/screenshots/2026-02-26_llamacpp_success.png`
- `evidence/screenshots/2026-02-26_api_llamacpp_curl_success.png`
- `evidence/screenshots/2026-02-26_ui_real_runtime.png`

## Evidence source
- `evidence/perf/2026-02-18_1332_results.json`
- `evidence/perf/2026-02-19_0423_results.json`