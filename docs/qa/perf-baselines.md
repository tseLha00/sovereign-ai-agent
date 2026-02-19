# Performance baselines (H08 evidence) (v0.1)

This document contains **actual baseline runs** and links to the raw JSON evidence under `evidence/perf/`.

## Baseline runs

| Date             | Adapter | Requests | Concurrency | p50 (ms) | p90 (ms) | p95 (ms) | Errors | Evidence JSON |
|------------------|---|---:|---:|---------:|---------:|---------:|-------:|---|
| 2026-02-18 13:32 | mock | 100 | 10 |        5 |       10 |       11 |      0 | `evidence/perf/2026-02-18_1332_results.json` |
| 2026-02-19 09:23 | mock | 100 | 10 |        6 |       14 |       26 |      0 | `evidence/perf/2026-02-19_0423_results.json` |

- Status codes for both runs: {"200": 100}
- Throughput:
    - 2026-02-18 13:32 → 214.15 rps
    - 2026-02-19 09:23 → 403.19 rps

## How to fill the table
Open the JSON file and copy:
- `latency_ms.median` → p50
- `latency_ms.p90` → p90
- `latency_ms.p95` → p95
- `errors` and `status_codes`

## Notes
- Sprint 1 baselines are expected to be **mock adapter** (framework overhead baseline).
- After real runtime integration (Sprint 2), add a new row with adapter = `llamacpp` (or equivalent).
