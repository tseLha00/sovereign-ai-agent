# A02/A03 — Research log (v0.6)

## Purpose
This log documents:
- **A02:** missing information (research questions)
- **A03:** research evidence used to make decisions and implement the solution

**Date rule (audit trail):**
- The **Date** in each research entry is the day the source was **accessed/checked** (not the day this file was edited).

## Format rules (so it meets A02/A03)
- Each research question has an ID (**Q-xxx**).
- Each research entry has an ID (**R-xxx**) and references at least one question ID.
- Each entry includes: **source**, **date**, **reliability**, **key findings**, and **impact**.
- Prefer primary sources: official docs/repos/model cards.

---

## A02 — Research questions (missing information list)

| ID | Research question | Why needed | Output artifact / decision |
|---|---|---|---|
| Q-001 | What is the official Apertus model artifact format and recommended runtime(s)? | Determines runtime feasibility and integration approach | H01 decision + adapter implementation |
| Q-002 | What is feasible on Mac mini M4 / 16 GB RAM (quantization, memory footprint, expected latency)? | Determines demo feasibility + tradeoffs | H01 decision + H08 baseline |
| Q-003 | Which runtime is best fit: llama.cpp vs Transformers vs Ollama (given constraints)? | Select dependency with least risk and best UX | H01 |
| Q-004 | What is the minimal OpenAI Chat Completions request/response contract to implement? | Prevents overbuilding; ensures compatibility | API models + pytest contract tests |
| Q-005 | What performance metrics matter for UX-first LLM demo? | Ensures correct perf focus | H08 perf script + perf-baselines.md |
| Q-006 | Which frontend UX patterns mitigate unavoidable latency? | Keeps demo “smooth” | frontend UI behavior + acceptance checks |
| Q-007 | Which exact HF Apertus 8B repo will be used, what is the license, and what artifact formats exist (GGUF vs safetensors)? | Compliance + runtime compatibility planning | H01 + implementation plan |
| Q-008 | If HF provides only Transformers/safetensors, what is the conversion path to GGUF and what evidence is required? | Avoid runtime block; plan Sprint 2 risk | H01 validation plan + Sprint 2 plan |

---

## A03 — Research notes (entries)

### R-001 — Environment constraints confirmed
- **Date:** 2026-02-13
- **Related questions:** Q-002
- **Source:** Kickoff meeting notes (internal) — `evidence/meeting-notes/2026-02-13_expert-meeting.md`
- **Reliability:** High (project authority)
- **Key findings:** Target machine = Mac mini M4, 16 GB RAM
- **Impact:** Memory-sensitive inference likely requires quantization; strongly influences H01 + H08.

---

### R-002 — Apertus 8B official source confirmed (Transformers artifacts)
- **Date:** 2026-02-18
- **Related questions:** Q-001, Q-007
- **Source:** Hugging Face model page: https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509
- **Reliability:** High (primary source)
- **Key findings:**
  - Model: `swiss-ai/Apertus-8B-Instruct-2509` (8B)
  - License shown on page: `apache-2.0`
  - Repository is provided for Transformers usage (safetensors/tokenizer), not GGUF
- **Impact:**
  - Defines the official provenance reference for documentation/compliance.
  - Confirms llama.cpp needs GGUF artifacts → select GGUF repo or conversion plan (feeds H01).

---

### R-003 — llama.cpp artifact requirement: GGUF format
- **Date:** 2026-02-18
- **Related questions:** Q-002, Q-003, Q-008
- **Source:** llama.cpp official repository: https://github.com/ggml-org/llama.cpp
- **Reliability:** High (primary source)
- **Key findings:**
  - llama.cpp uses **GGUF** as the standard model file format for local inference.
- **Impact:**
  - Integration path should use GGUF directly when possible (lowest-risk path).

---

### R-004 — Selected GGUF distribution for implementation (ready-to-run artifacts)
- **Date:** 2026-02-18
- **Related questions:** Q-007, Q-008
- **Source:** Hugging Face GGUF repo: https://huggingface.co/unsloth/Apertus-8B-Instruct-2509-GGUF
- **Reliability:** High (primary source)
- **Key findings:**
  - Provides GGUF files suitable for llama.cpp.
  - License shown on repo page: `apache-2.0`
- **Impact:**
  - Enables a direct llama.cpp PoC without conversion work.
  - Baseline file selected for first-run on 16 GB: `Apertus-8B-Instruct-2509-Q4_K_M.gguf`.

---

### R-005 — Minimal OpenAI Chat Completions contract (reference shape)
- **Date:** 2026-02-18
- **Related questions:** Q-004
- **Source:** OpenAI API docs: https://platform.openai.com/docs/api-reference/chat
- **Reliability:** High (primary source)
- **Key findings:**
  - Minimal response fields: `id`, `object`, `created`, `model`, `choices[].message`, `choices[].finish_reason`
- **Impact:**
  - Defines the response schema verified by pytest contract tests in Sprint 1.

---

### R-006 — Performance metrics selection (UX-first)
- **Date:** 2026-02-13
- **Related questions:** Q-005
- **Source:** Kickoff meeting notes (internal) — `evidence/meeting-notes/2026-02-13_expert-meeting.md`
- **Reliability:** High (project authority)
- **Key findings:**
  - Demo focus: UX perceived responsiveness first
  - Metrics to track: latency percentiles (p50/p90/p95) + error rate
- **Impact:**
  - Confirms the KPI set in H08 and the JSON result format used by the perf script.

---

### R-007 — Runtime PoC validated (llama.cpp + GGUF + one prompt)
- **Date:** 2026-02-26
- **Related questions:** Q-001, Q-002, Q-003, Q-007
- **Source:** Local terminal run (`llama-cli`) + evidence stored in repository
- **Reliability:** High (direct evidence)
- **Key findings:**
  - Model file loaded successfully from: `models/Apertus-8B-Instruct-2509-Q4_K_M.gguf`
  - One prompt executed end-to-end and produced a valid response
  - The model responded: *“Hello, I'm Apertus, a helpful assistant created by the SwissAI initiative.”*
  - Prompt throughput and generation throughput were displayed successfully in terminal output
- **Impact:**
  - Confirms the GGUF + llama.cpp path works on the target machine
  - Validates the selected runtime path in H01
  - Reduces Sprint 2 backend integration risk significantly

**Evidence:**
- `evidence/runtime/2026-02-26_llamacpp_run.log`
- `evidence/runtime/2026-02-26_llamacpp_success.png`
- `evidence/runtime/2026-02-26_llamacpp_note.md`

---

## AI / tool usage declaration
Record only what was actually used.

| Date | Tool | What I did | What I used in the project | What I verified myself |
|---|---|---|---|---|
| 2026-02-13 | ChatGPT | Structured A02/A03 template | IDs + structure | Constraints confirmed with supervisor |
| 2026-02-18 | Browser | Checked official HF repo | Official repo + license + artifact type | Verified page values manually |
| 2026-02-18 | Browser | Checked GGUF repo options | Chosen GGUF repo + baseline file | Verified GGUF availability manually |
| 2026-02-18 | Terminal | Ran Sprint 1 perf baseline (`make perf`) | Evidence JSON under `evidence/perf/` | Verified output manually |
| 2026-02-26 | Terminal | Ran official llama.cpp PoC with local GGUF file | Runtime validation evidence | Verified model load and generated response manually |