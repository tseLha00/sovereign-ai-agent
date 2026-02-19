# H01 — Component dependency analysis and selection (v0.4)

## 1. Purpose of this decision
The project depends on choosing an inference runtime that can run the **Apertus LLM locally** on the target machine.
This decision impacts:
- performance and UX latency
- memory feasibility (16 GB RAM)
- integration complexity and maintainability
- model artifact format compatibility and deployment story

## 2. System components and interfaces
- **Frontend:** web-based chat UI (responsive, common chat features)
- **Backend API:** OpenAI-style endpoints (FastAPI)
- **Inference runtime:** executes the model locally behind an adapter (`adapter.chat(...)`)
- **Model artifacts:** Apertus **8B** artifacts sourced from Hugging Face
- **Observability:** logs + performance baseline script results + error reporting
- **Execution:** local run first; containerization optional later if feasible

## 3. Environment constraints (confirmed)
- Target machine: **Mac mini M4**
- RAM: **16 GB**
Implications:
- memory-sensitive inference; quantization required
- latency must be monitored and improved with UX-first approach (H08)

## 4. Options considered (inference runtime)

### Option A — llama.cpp
**Pros**
- optimized C/C++; strong for quantized inference
- runs well on Apple Silicon with GGUF artifacts
- clear story for reproducible local demos

**Cons / uncertainties**
- requires GGUF artifacts; Transformers-only repos need GGUF distribution or conversion
- integration effort: wrapper, parameters, error handling

### Option B — PyTorch + Transformers
**Pros**
- direct compatibility with Hugging Face safetensors
- fast experimentation/debugging

**Cons / uncertainties**
- may exceed RAM/latency expectations for 8B on 16 GB
- heavier deployment story

### Option C — Ollama (optional)
**Pros**
- fast local setup for demos
**Cons / uncertainties**
- model availability/compatibility must be verified
- less control over integration details

## 5. Selection criteria (ranked)
1) **Runs reliably on target machine (M4/16 GB)**
2) **Compatible with Apertus 8B artifacts** (format + tokenizer + quantization)
3) **UX/latency feasible** (or mitigatable via UX patterns)
4) **Maintainable integration** with the adapter architecture
5) **Repeatable setup/deployment** for demo usage
6) **Compliance/IP constraints** acceptable for internal demo

## 6. Decision
- **Selected inference runtime:** **llama.cpp**
- **Reason:**
  - best fit for Apple Silicon + limited RAM constraints
  - supports quantized GGUF inference and a clean local demo story
  - aligns with UX-first performance approach (H08)

## 7. Selected model source + artifact path
We separate **official source repo** (documentation/compliance reference) from **runnable artifact repo** (GGUF).

### 7.1 Official model source (documentation reference)
- Repo: `swiss-ai/Apertus-8B-Instruct-2509`
- Used for: model identification, license reference, provenance in A02/A03.

### 7.2 Runnable llama.cpp artifacts (GGUF)
- Repo: `unsloth/Apertus-8B-Instruct-2509-GGUF`
- Initial file: `Apertus-8B-Instruct-2509-Q4_K_M.gguf`
- Rationale: direct llama.cpp loading; Q4_K_M is a safe baseline on 16GB.

## 8. Validation plan (evidence required)
To finalize and prove the runtime + artifact path:
- Download the selected GGUF file
- Run a minimal local inference command (one prompt)
- Capture evidence:
  - command used
  - success/failure output
  - qualitative latency notes (first-token time + total time observed)
  - any errors and mitigation steps

Evidence to store:
- A02/A03 entries updated (R-002/R-003)
- terminal output screenshot or log in `evidence/runtime/`
- follow-up note in this decision record (append “Validation result” section)

## 9. Risks and fallbacks
- **Risk:** GGUF artifact quality/behavior differs from expectations  
  **Mitigation:** try a second quant level (Q5_K_M) or alternative GGUF distribution; document changes.
- **Risk:** performance/latency too high  
  **Mitigation:** reduce context length, adjust params, add frontend “thinking…” UX; record in H08 baselines.
- **Fallback:** PyTorch + Transformers as last resort if GGUF path blocks progress.
