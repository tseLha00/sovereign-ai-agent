# A02/A03 — Research log (v0.3)

## Purpose
This log documents the **missing information (A02)** and the **research evidence (A03)** used to make decisions and implement the solution.

## Format rules (so it meets A02/A03)
- Each research question has an ID (**Q-xxx**).
- Each research entry has an ID (**R-xxx**) and references at least one question ID.
- Each entry includes: **source**, **date**, **reliability**, **key findings**, and **impact** on decisions/implementation.
- Sources should prefer official documentation, vendor repositories, and primary sources.

---

## A02 — Research questions (missing information list)

| ID | Research question | Why needed | Output artifact / decision |
|---|---|---|---|
| Q-001 | What is the official Apertus model artifact format and recommended runtime(s)? | Determines runtime feasibility and integration approach | H01 decision + adapter implementation |
| Q-002 | What is feasible on Mac mini M4 / 16 GB RAM (quantization, memory footprint, expected latency)? | Determines demo feasibility and required tradeoffs | H01 decision + H08 perf baseline |
| Q-003 | Which runtime is best fit: llama.cpp vs Transformers vs Ollama (for this project constraints)? | Select dependency with least risk and best UX | H01 |
| Q-004 | What is the minimal OpenAI Chat Completions compatible request/response shape to implement? | Prevents overbuilding, ensures compatibility | backend API contract + tests |
| Q-005 | What performance metrics matter for UX-focused LLM demo (latency distributions, error rate, throughput)? | Aligns monitoring with supervisor expectations | H08 perf script + perf results |
| Q-006 | Which frontend UX patterns mitigate unavoidable latency (thinking state, streaming later, progressive rendering)? | Ensures smooth interaction under latency | frontend UI + acceptance criteria |
| Q-007 | Which exact HF Apertus 8B repo will be used, what is the license, and what artifact formats are provided (GGUF vs safetensors)? | Compliance + runtime compatibility planning | H01 + integration plan |
| Q-008 | If HF provides only Transformers/safetensors, what is the conversion path to GGUF and what evidence is required? | Avoids runtime block + plans Sprint 2 | H01 validation + Sprint 2 plan |

---

## A03 — Research notes (entries)

### R-001 — Environment constraints confirmed
- **Date:** 2026-02-13
- **Related questions:** Q-002
- **Source:** Supervisor/expert kickoff meeting notes (internal)
- **Reliability:** High (project authority)
- **Key findings:** Target machine = Mac mini M4, 16 GB RAM
- **Impact:** Requires memory-sensitive inference; quantization likely required; strongly influences H01 and H08.

---

### R-002 — Apertus 8B official source confirmed (Transformers artifacts)
- **Date:** 2026-02-18
- **Related questions:** Q-001, Q-007
- **Source:** (HF model page) https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509
- **Reliability:** High (primary source)
- **Key findings:**
  - Model: Apertus-8B-Instruct-2509 (8B)
  - License shown on page: apache-2.0
  - Repository indicates Transformers/safetensors (not GGUF)
- **Impact:**
  - Fixes the “official model reference” for documentation/compliance.
  - Confirms llama.cpp requires a GGUF artifact source OR a conversion plan.

---

### R-003 — llama.cpp runtime requirement: GGUF format
- **Date:** 2026-02-18
- **Related questions:** Q-002, Q-003, Q-008
- **Source:** (llama.cpp official repo) https://github.com/ggml-org/llama.cpp
- **Reliability:** High (primary source)
- **Key findings:**
  - llama.cpp uses GGUF as the standard model file format for local inference.
- **Impact:**
  - Integration plan should use GGUF directly when possible to reduce risk/time.

---

### R-004 — Selected GGUF distribution for implementation (ready-to-run)
- **Date:** 2026-02-18
- **Related questions:** Q-007, Q-008
- **Source:** (HF GGUF repo) https://huggingface.co/unsloth/Apertus-8B-Instruct-2509-GGUF
- **Reliability:** High (primary source)
- **Key findings:**
  - Provides GGUF files suitable for llama.cpp usage.
  - License shown on repo: apache-2.0 (verify on page)
- **Impact:**
  - Enables direct llama.cpp PoC without conversion work.
  - Chosen baseline file for first run on 16 GB: **Apertus-8B-Instruct-2509-Q4_K_M.gguf** (memory-friendly baseline).

---

### R-005 — Minimal OpenAI Chat Completions contract (reference shape)
- **Date:** 2026-02-18
- **Related questions:** Q-004
- **Source:** (OpenAI API docs) https://platform.openai.com/docs/api-reference/chat
- **Reliability:** High (primary source)
- **Key findings:**
  - Response includes: `id`, `object`, `created`, `model`, `choices[]` with `message` + `finish_reason`.
- **Impact:**
  - Defines the response schema used by FastAPI and verified by pytest contract tests.

---

### R-006 — PoC run evidence plan (llama.cpp + GGUF + one prompt)
- **Date:** 2026-02-19
- **Related questions:** Q-001, Q-002, Q-003, Q-007
- **Source:** local terminal run + screenshots/logs (evidence in repo)
- **Reliability:** High (direct evidence)
- **Key findings (to fill after run):**
  - GGUF download succeeded
  - llama.cpp loaded model successfully (or error encountered)
  - One prompt executed end-to-end; latency observed qualitatively
- **Impact:**
  - Finalizes the “artifact compatibility path” proof for H01 and reduces Sprint 2 integration risk.

**Evidence files (repo-root):**
- `evidence/poc/` (screenshots/logs)
- example: `evidence/poc/2026-02-19_llamacpp_run.log`
- example: `evidence/poc/2026-02-19_llamacpp_success.png`

---

## AI / tool usage declaration

| Date | Tool | Prompt / what I asked | What I used in the project | What I verified myself |
|---|---|---|---|---|
| 2026-02-13 | ChatGPT | Help structure A02/A03 and create research template | Template structure + IDs | Supervisor constraints + repo structure checked |
| 2026-02-18 | Browser | Check HF Apertus repo + license + artifacts | Selected official repo + noted artifact format | Verified license string + file list manually |
| 2026-02-18 | Browser | Check GGUF repo + file options | Selected GGUF repo + baseline file name | Verified license string + GGUF availability manually |
| 2026-02-19 | Terminal | Run llama.cpp PoC | PoC evidence logs/screenshots | Verified output manually |
