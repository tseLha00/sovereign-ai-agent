# H08 — Performance & stability monitoring (v0.1)

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

### 3.2 Result storage (traceable evidence)
Each run stores a timestamped JSON file:
- `evidence/perf/YYYY-MM-DD_HHMM_results.json`

The JSON includes:
- timestamp, URL
- requests, concurrency, total time, throughput
- success/errors + status codes
- latency metrics (min/mean/median/p90/p95/max)

### 3.3 Logging
Backend should log at least:
- endpoint, status code
- latency per request (ms)
- error stack traces for failures

## 4. Baseline and comparison strategy
### Baseline
- Create an initial baseline using the **mock adapter** (to measure framework overhead and request handling).
- After integrating real inference, create a second baseline (real adapter).

### How to compare
- Compare latency percentiles and error rate between versions.
- If the p95 latency increases noticeably after a change, investigate before continuing.

## 5. Regular checks (when to run)
- End of Day 1: baseline created (mock adapter)
- After major backend changes (routing, adapter, runtime integration)
- After integrating the real model/runtime
- Before sprint review / demo run

## 6. Optimization policy (what actions to take)
If performance issues are detected:
### Backend actions
- profile request handling overhead
- reduce unnecessary processing and logging overhead
- adjust model/runtime parameters where applicable
- ensure timeouts and concurrency settings are sane

### Frontend UX mitigations
If latency cannot be fully removed:
- show “thinking…” indicator immediately
- disable send button while pending (or allow queueing with clear state)
- show partial results (streaming) later if implemented
- show clear error states + retry affordance
