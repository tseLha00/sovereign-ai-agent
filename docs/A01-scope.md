# A01 — Scope analysis and project method selection (v0.2)

## 1. Context and problem statement
Accenture requires a **local (on-prem) sovereign AI demo** for client workshops: a chatbot powered by the **Apertus LLM (8B)** sourced from Hugging Face, usable through a **web UI** and via an **API compatible with the OpenAI de facto standard** (minimum: Chat Completions-style interface).

Previous work was not started; this project establishes the first working baseline, including documentation, evidence, and a reproducible development setup.

## 2. Stakeholders
- **Sponsor / Product owner:** Accenture (internal demo use)
- **Supervisor:** Enrico Viola
- **Experts:** Yves Kaufmann, Mirio Joël Eggmann
- **End users:** internal workshop facilitators / demo participants

## 3. Project goals (what success looks like)

### 3.1 Primary goal (final demo)
Deliver a working on-prem chatbot demo that:
- runs on the assigned machine (**Mac mini M4, 16GB RAM**)
- provides a usable chat UI
- exposes an OpenAI-style API endpoint for chat
- can later be shown in workshops without fragile manual steps

### 3.2 Acceptance criteria (testable)
The solution is considered successful if the following can be demonstrated:
- **UI usability:** chat UI works on common screen sizes (laptop + desktop) and supports expected basics (send message, display response, show errors, clear/reset chat).
- **API compatibility:** backend provides `POST /v1/chat/completions` with a response shape aligned to OpenAI-style Chat Completions (`id`, `object`, `created`, `model`, `choices.message`).
- **Local inference:** inference runs locally using **Apertus 8B** (no external LLM calls during inference; model download is allowed during setup).
- **Quality baseline:** reproducible commands exist for run + tests + performance check.
- **Performance monitoring:** a repeatable benchmark/perf script exists and stores results for comparison over time.

## 4. Requirements

### 4.1 Functional requirements (initial scope)
- Endpoint: `POST /v1/chat/completions`
- Request: accepts messages array (`system` / `user` / `assistant`)
- Response: returns assistant message content + required metadata (OpenAI-style shape)
- Minimal UI for interacting with the model (chat)

### 4.2 Non-functional requirements
- On-prem inference operation (offline-capable once model artifacts are available locally)
- Stability (no crashes in normal usage)
- UX-first latency: noticeable latency should be reduced by backend optimizations; if unavoidable, it must be mitigated in UX (e.g., “thinking…” indicator).
- Reproducibility: documented run/test/perf commands

## 5. Scope boundaries

### 5.1 In scope (this project)
- Backend scaffold with **adapter architecture** for the inference runtime
- OpenAI-style chat endpoint (`/v1/chat/completions`)
- Performance baseline and repeated measurement (H08)
- Test concept + initial tests and evidence (A12)
- Minimal responsive UI for the demo
- Model integration using **Apertus 8B** from Hugging Face (repo + license documented in A02/A03)

### 5.2 Explicitly out of scope (unless time remains)
- Full security hardening (auth, RBAC, advanced threat modeling)
- Heavy “agent” features, tool execution, complex orchestration
- Fine-tuning / training of the model
- Production-grade infrastructure (Kubernetes, autoscaling, etc.)
- Streaming responses (nice-to-have)

## 6. Constraints and assumptions
- **Hardware constraint:** Mac mini M4, 16GB RAM (influences runtime and model format decisions)
- **Model constraint:** Apertus **8B** is sourced via Hugging Face; exact repository + license are documented in A02/A03
- **IP constraint:** source code and compiled application are treated as Accenture IP unless otherwise stated
- `/v1/models` endpoint: optional until later
- Streaming responses: nice-to-have, not mandatory
- Target users expect a smooth, natural interaction experience (UX prioritized)

## 7. Project method selection: Scrum (2 sprints)

### 7.1 Why Scrum fits this project
This project has a fixed timebox (IPA) and high uncertainty (LLM runtime feasibility, latency, memory limits).
Scrum supports:
- iterative delivery (working demo increments)
- frequent validation (review/retro)
- controlled scope management with clear “done” criteria

### 7.2 Sprint outline (high level)
- **Sprint 1 (baseline):**
  - reproducible backend skeleton
  - OpenAI-style endpoint with mock adapter
  - tests + performance baseline + evidence
  - initial documentation discipline (A01/A02/A03/A04/A05/A12/H01/H08)
- **Sprint 2 (integration + demo):**
  - integrate **Apertus 8B** via chosen runtime
  - UI improvements for multi-device usability
  - stability and UX latency improvements
  - finalize evidence and deliverables

## 8. Deliverables overview (traceability)
- Part 1 deliverables (planning + discipline):
  - A01, A02/A03, A04, A05, A12, H01, H08
- Engineering deliverables:
  - working code, tests, performance results, decision records, and traceable repository evidence
