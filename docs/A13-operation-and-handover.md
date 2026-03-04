# A13 — Operation, handover and known limitations (v0.1)

## Version history
- **v0.1** — Initial operation, handover, and limitation overview created for the final demo state.

## 1. Purpose
This document describes how the implemented demo is started, operated, validated, and handed over in its current state.

It documents:
- required local prerequisites
- reproducible run and test commands
- what is included in the delivered scope
- current limitations and deferred items
- what a technical reviewer needs to know to run the solution

## 2. Delivered implementation state
The delivered solution includes:
- a FastAPI backend
- an OpenAI-style endpoint: `POST /v1/chat/completions`
- a local `llama.cpp` adapter for real inference with Apertus 8B (GGUF)
- a browser-served frontend UI at `/ui/`
- automated tests for the current backend baseline
- stored evidence for runtime, API, tests, and UI

The delivered solution is a **local demo baseline**, not a production deployment.

## 3. Preconditions for operation

### 3.1 Hardware / platform
- Target machine: **Mac mini M4**
- RAM: **16 GB**
- Operating mode: **local execution**

### 3.2 Software prerequisites
- Python environment with project dependencies installed
- `llama.cpp` CLI available locally as `llama-cli`
- Local GGUF model file available at:
  - `models/Apertus-8B-Instruct-2509-Q4_K_M.gguf`

### 3.3 Environment variables
The following environment variables are used by the backend:
- `LLM_BACKEND`
  - `mock` for baseline/testing
  - `llamacpp` for real local inference
- `LLAMA_CPP_MODEL_PATH`
  - optional override for the model file path
- `LLAMA_CPP_BIN`
  - optional override for the `llama.cpp` CLI binary name/path

## 4. Reproducible operation

### 4.1 Start backend with mock adapter
```bash
make run