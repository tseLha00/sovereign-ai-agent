# Performance baselines (H08 evidence) (v0.2)

## Version history
- **v0.1** — Initial baseline evidence table created with Sprint 1 mock-adapter benchmark results.
- **v0.2** — Clarified interpretation of mock-adapter baseline results and separated them from real-runtime functional validation evidence.

This document contains **actual baseline runs** and links to the raw JSON evidence under `evidence/perf/`.

## Baseline runs

| Date             | Adapter | Requests | Concurrency | p50 (ms) | p90 (ms) | p95 (ms) | Errors | Evidence JSON |
|------------------|---|---:|---:|---------:|---------:|---------:|-------:|---|
| 2026-02-18 13:32 | mock | 100 | 10 | 5 | 10 | 11 | 0 | `evidence/perf/2026-02-18_1332_results.json` |
| 2026-02-19 04:23 | mock | 100 | 10 | 6 | 14 | 26 | 0 | `evidence/perf/2026-02-19_0423_results.json` |

## Summary
- Status codes for both runs: `{"200": 100}`
- Throughput:
  - 2026-02-18 13:32 → `214.15 rps`
  - 2026-02-19 04:23 → `403.19 rps`

## Interpretation
These Sprint 1 baselines are **mock-adapter measurements**.
They measure:
- backend/API handling overhead
- request/response path stability
- application responsiveness without real model generation cost

They do **not** yet represent full real-model inference latency.

## Next planned comparison
After the real `llama.cpp` adapter is integrated into the backend, an additional benchmark run will be added for comparison.

## Evidence source
- `evidence/perf/2026-02-18_1332_results.json`
- `evidence/perf/2026-02-19_0423_results.json`