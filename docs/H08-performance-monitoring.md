# H08 — Performance & stability monitoring (v0.2)

## Version history
- **v0.1** — Initial UX-first performance monitoring strategy defined (KPIs, benchmark script, result storage, and optimization policy).
- **v0.2** — Clarified that current formal perf baselines are mock-adapter only, while real llama.cpp runtime is functionally validated through smoke checks and screenshot evidence.

## 1. Goal (UX-first)
Performance monitoring focuses on what matters for a demo:
- the interaction must feel smooth and natural
- if latency cannot be removed, it must be mitigated by UX patterns

Priority order (aligned with supervisor guidance):
1) UX perceived responsiveness
2) Latency
3) Stability

## 2. KPIs

### Primary KPIs
- **Latency distribution:** p50, p90, p95 (ms)
- **Stability:** error rate, timeouts, non-200 responses

### Secondary KPIs
- Throughput (requests/sec)
- CPU usage and memory footprint (qualitative during early phases)

## 3. Measurement mechanisms

### 3.1 Benchmark script
- Script: `backend/qa/perf/run_perf.py` (repeatable)
- Endpoint: `POST /v1/chat/completions`
- Configurable parameters: requests, concurrency, payload size

### 3.2 Result storage
Each run stores a timestamped JSON file:
- `evidence/perf/YYYY-MM-DD_HHMM_results.json`

### 3.3 Logging
Backend should log at least:
- endpoint
- status code
- latency per request
- error details for failures

## 4. Current baseline status
Current measured baselines are based on the **mock adapter**.
This is useful to establish:
- framework overhead
- request path stability
- reproducible benchmark execution

The real `llama.cpp` runtime is already **functionally validated** through:
- successful standalone model loading
- successful backend API response
- successful frontend UI interaction

However, a formal real-runtime performance comparison should only be added once a timestamped benchmark JSON is stored under `evidence/perf/`.

**Functional validation evidence:**
- `evidence/screenshots/2026-02-26_llamacpp_success.png`
- `evidence/screenshots/2026-02-26_api_llamacpp_curl_success.png`
- `evidence/screenshots/2026-02-26_ui_real_runtime.png`

## 5. Regular checks
- Baseline after major backend changes
- After real adapter integration
- Before sprint review / demo

## 6. Optimization policy

### Backend actions
- reduce unnecessary processing overhead
- improve runtime configuration
- keep request handling stable

### Frontend UX mitigations
- show “thinking…” indicator immediately
- disable send while pending
- show clear error states
- add streaming later only if needed