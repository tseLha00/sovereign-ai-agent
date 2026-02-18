# H01 — Component dependency analysis and selection (v0.2)

## 1. Purpose of this decision
The project depends on choosing an inference runtime that can run the **Apertus LLM locally** on the target machine.
This decision impacts:
- performance and UX latency
- memory feasibility (16 GB RAM)
- integration complexity and maintainability
- model format compatibility and deployment story

## 2. System components and interfaces
- **Frontend:** web-based chat UI (responsive, common chat features)
- **Backend API:** OpenAI-style endpoints (FastAPI)
- **Inference runtime:** executes the model locally behind an adapter (`adapter.chat(...)`)
- **Model artifacts:** model weights + format (likely quantized)
- **Observability:** logs + performance baseline script results + error reporting
- **Execution:** local run first; containerization optional later if feasible

## 3. Environment constraints (confirmed)
- Target machine: **Mac mini M4**
- RAM: **16 GB**
Implications:
- memory-sensitive inference; quantization likely required
- performance/latency must be monitored with a benchmark (H08)

## 4. Options considered (inference runtime)

### Option A — llama.cpp
**Pros**
- optimized C/C++; strong for quantized models
- commonly used for local inference on limited memory
- good basis for repeatable deployment and performance comparisons

**Cons / uncertainties**
- requires verifying Apertus model compatibility (format + tokenizer)
- integration effort (wrapping, parameters, error handling)

### Option B — PyTorch + Transformers
**Pros**
- fastest iteration for experimentation
- flexible for debugging model behavior and features

**Cons / uncertainties**
- may exceed RAM constraints or be slow for larger models on 16 GB
- packaging/deployment story may become heavier

### Option C — Ollama (if acceptable)
**Pros**
- fast setup for local demos; convenient model management
- can improve demo UX quickly

**Cons / uncertainties**
- abstraction may limit control
- policy/licensing and “Accenture IP” implications must be clarified
- model availability/compatibility for Apertus must be verified

## 5. Selection criteria (ranked)
1) **Runs reliably on target machine (M4/16 GB)**  
2) **Compatible with Apertus artifacts** (format + tokenizer + quantization)
3) **UX/latency feasible** (or mitigatable with UI patterns)
4) **Maintainable integration** with the adapter architecture
5) **Repeatable setup/deployment** for demo usage
6) **Compliance/IP constraints** acceptable for internal demo

## 6. Current decision status
- **Provisional direction:** llama.cpp
- **Reason:** best match for on-device inference constraints and quantized runtime story
- **Not yet final because:** Apertus format compatibility must be verified on the target machine

## 7. Validation plan (what must happen to finalize the decision)
To confirm the runtime choice, a minimal PoC must be run on the target machine:
- Load an Apertus-compatible model artifact (or the closest available format)
- Execute one prompt end-to-end and collect:
  - success/failure notes
  - latency observation
  - memory feasibility (qualitative; no strict numeric benchmark required)

Evidence to attach:
- command log / notes (A02/A03 research log)
- any runtime output or screenshots (evidence folder)
- updated decision record with final recommendation

## 8. Risks and fallbacks
- **Risk:** chosen runtime cannot load Apertus artifacts  
  **Mitigation:** define a fallback path (e.g., Transformers baseline) and document the tradeoff.
- **Risk:** latency is noticeable and cannot be fully optimized  
  **Mitigation:** UX mitigation in UI (“thinking…”, streaming later, partial rendering) + perf monitoring (H08)

## 9. Decision deadline
Final runtime decision is targeted by:
- **Milestone M2 (Sprint 2 early)**  
after the compatibility check on the target machine.
