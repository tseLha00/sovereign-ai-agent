# A02/A03 — Research log (v0.1)

## Purpose
This log documents the **missing information (A02)** and the **research evidence (A03)** used to make decisions and implement the solution.

## Format rules (so it meets A02/A03)
- Each research question has an ID (**Q-xxx**).
- Each research entry has an ID (**R-xxx**) and references at least one question ID.
- Each entry includes: source, date, reliability, key findings, and impact on decisions/implementation.
- Sources should prefer official documentation, vendor repositories, and primary sources.

---

## A02 — Research questions (missing information list)

| ID | Research question | Why needed | Output artifact / decision |
|---|---|---|---|
| Q-001 | What is the official Apertus model artifact format and recommended runtime(s)? | Determines runtime feasibility and integration approach | H01 decision + adapter implementation |
| Q-002 | What is feasible on Mac mini M4 / 16 GB RAM (quantization, memory footprint, expected latency)? | Determines whether the demo is feasible and what tradeoffs are needed | H01 decision + H08 perf baseline |
| Q-003 | Which runtime is best fit: llama.cpp vs Transformers vs Ollama (for this project constraints)? | Select dependency with least risk and best UX | H01 |
| Q-004 | What is the minimal OpenAI Chat Completions compatible request/response shape to implement? | Prevents overbuilding, ensures compatibility | backend API contract + tests |
| Q-005 | What performance metrics matter for UX-focused LLM demo (latency distributions, error rate, throughput)? | Aligns perf monitoring with supervisor expectations | H08 perf script + perf-baselines.md |
| Q-006 | Which frontend UX patterns mitigate unavoidable latency (thinking state, streaming later, progressive rendering)? | Ensures “smooth, natural” interaction even under constraints | frontend UI work + acceptance criteria |

---

## A03 — Research notes (entries)

### R-001 — Environment constraints confirmed
- **Date:** 2026-02-13  
- **Related questions:** Q-002  
- **Source:** Supervisor meeting notes (internal)  
- **Reliability:** High (project authority)  
- **Key findings:** Target machine = Mac mini M4, 16 GB RAM  
- **Impact:** Strongly favors quantized inference; runtime must be Apple Silicon-friendly; influences H01 and H08 baseline.

---

### R-002 — Apertus: official model/runtime guidance (TODO)
- **Date:** (fill)  
- **Related questions:** Q-001, Q-003  
- **Source:** (official Apertus repository/docs or internal Accenture link)  
- **Reliability:** (High if official, Medium if secondary)  
- **Key findings:**
  - Model artifact format(s): …
  - Supported runtime(s): …
  - Any macOS/Apple Silicon notes: …
- **Impact (H01/implementation):**
  - Confirms whether llama.cpp is compatible or not.
  - Determines adapter interface requirements and model loading pipeline.

---

### R-003 — llama.cpp on Apple Silicon: feasibility and constraints (TODO)
- **Date:** (fill)  
- **Related questions:** Q-002, Q-003  
- **Source:** llama.cpp docs / GitHub README / release notes / benchmark reports  
- **Reliability:** High for official repo; Medium for third-party benches  
- **Key findings:**
  - Supported formats (GGUF, etc): …
  - Quantization options and tradeoffs: …
  - Expected performance on Apple Silicon: …
- **Impact:**
  - Strengthens or weakens provisional H01 direction.
  - Informs H08 perf test parameters (payload size, concurrency, etc.).

---

### R-004 — Minimal OpenAI Chat Completions contract (TODO)
- **Date:** (fill)  
- **Related questions:** Q-004  
- **Source:** OpenAI API documentation (Chat Completions), or official spec references  
- **Reliability:** High (primary source)  
- **Key findings:**
  - Required request fields: model, messages…
  - Minimal response fields: id, object, created, model, choices[0].message…
  - Optional fields: usage, finish_reason, streaming  
- **Impact:**
  - Defines request/response models in FastAPI.
  - Drives pytest contract tests.

---

### R-005 — UX-oriented performance metrics for LLM APIs (TODO)
- **Date:** (fill)  
- **Related questions:** Q-005  
- **Source:** engineering blog posts + official docs + internal best practices  
- **Reliability:** Medium (unless primary/internal)  
- **Key findings:**
  - KPIs: p50/p90/p95 latency, error rate, stability
  - Why throughput is secondary when UX is priority
- **Impact:**
  - Confirms H08 focus: latency percentiles + errors + stability.
  - Defines baseline recording format (JSON) and tracking in perf-baselines.md.

---

### R-006 — Frontend latency-mitigation patterns (TODO)
- **Date:** (fill)  
- **Related questions:** Q-006  
- **Source:** UX guidance + known chat UI patterns (reliable design refs preferred)  
- **Reliability:** Medium  
- **Key findings:**
  - “Thinking…” indicator patterns
  - disable send while pending; show partial updates if streaming later
  - retry/error states that feel smooth
- **Impact:**
  - Acceptance criteria for frontend tasks and demo UX.

---

## AI / tool usage declaration
Record only what you actually used.

| Date | Tool | Prompt / what I asked | What I used in the project | What I verified myself |
|---|---|---|---|---|
| 2026-02-13 | ChatGPT | Help structure A02/A03 and create research template | Template structure + IDs | Supervisor constraints + repo structure checked |
