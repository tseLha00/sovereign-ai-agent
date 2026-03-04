# H08 — Performance & stability monitoring (v0.2)

## Version history
- **v0.1** — Initial UX-first performance monitoring strategy defined (KPIs, benchmark script, result storage, and optimization policy).
- **v0.2** — Added current validation status, clarified the difference between mock baselines and real-runtime validation, and documented current limitations honestly.

## 1. Goal (UX-first)
Performance monitoring focuses on what matters for a demo:
- the interaction should feel smooth and understandable
- latency should be observed and reduced where practical
- if latency cannot be removed, it should be mitigated through UX

Priority order:
1. perceived responsiveness
2. latency
3. stability

## 2. KPIs

### Primary KPIs
- latency distribution: p50, p90, p95 (ms)
- error rate
- timeout rate
- non-200 response rate

### Secondary KPIs
- throughput (requests per second)
- qualitative observations about memory use and runtime behavior

## 3. Measurement mechanisms

### 3.1 Benchmark script
- Script: `backend/qa/perf/run_perf.py`
- Endpoint under test: `POST /v1/chat/completions`
- Purpose: repeatable baseline comparisons over time

### 3.2 Result storage
Each benchmark run stores a timestamped JSON file:
- `evidence/perf/YYYY-MM-DD_HHMM_results.json`

### 3.3 Logging
The backend should make it possible to observe:
- endpoint usage
- status codes
- request success/failure
- overall runtime behavior during validation

## 4. Current validated status

### 4.1 Mock-adapter baseline
Repeatable benchmark runs exist for the mock adapter.
These are valid for:
- framework overhead
- request-path stability
- basic responsiveness of the backend without real model generation

### 4.2 Real-runtime status
The real `llama.cpp` runtime has been validated functionally:
- model load works
- API responses work
- UI requests work

However:
- a stable, repeatable **real-runtime performance benchmark** has not yet been recorded as a comparable JSON baseline in the same way as the mock runs

This means:
- the project currently has **functional validation** for real inference
- but only **benchmark evidence** for the mock adapter

## 5. Interpretation
This is acceptable for the delivered demo baseline as long as it is documented honestly:
- the solution is technically usable
- the performance-monitoring concept exists
- baseline measurement infrastructure exists
- a production-grade or fully comparable real-runtime performance series remains future work

## 6. Optimization policy

### Backend-side actions
- keep prompt size limited where practical
- reduce avoidable processing overhead
- harden error handling and response cleanup

### Frontend-side mitigations
- show immediate UI feedback
- keep controls clear and predictable
- avoid overwhelming the user during waiting phases

## 7. Next measurement step
The next recommended performance step is:
- run an explicitly documented real-runtime benchmark with the `llama.cpp` adapter
- store the result under `evidence/perf/`
- compare it against the existing mock baseline

## 8. Evidence references
- `evidence/perf/2026-02-18_1332_results.json`
- `evidence/perf/2026-02-19_0423_results.json`
- functional runtime validation: `evidence/screenshots/2026-02-26_llamacpp_success.png`