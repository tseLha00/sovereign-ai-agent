# A05 — Progress and risk tracking (v0.6)

## Version history
- **v0.1** — Initial progress-tracking, deviation log, and risk-register structure created.
- **v0.2** — Added audit anchors (kickoff and Sprint 1 review/retro) and aligned evidence references.
- **v0.3** — Refined deviation handling and clarified risk mitigations for runtime, latency, and licensing.
- **v0.4** — Added runtime PoC path issue and resolution, updated risk statuses after llama.cpp validation, and improved audit-trail precision.
- **v0.5** — Added completed backend/API/UI validation evidence, removed outdated local file-path references, and updated open risks to reflect the implemented demo state.
- **v0.6** — Added formalized QA completion status including automated browser smoke testing and updated remaining risks for final handover/documentation.

## 1. Tracking cadence
- Daily: update work journal + move issues on the board
- Per sprint: sprint review + retro notes stored under `evidence/meeting-notes/`

## 2. Soll/Ist tracking approach
- **Soll:** time plan Excel (1-hour blocks)
- **Ist:** filled daily in Excel
- **Exact minutes:** if work does not fit 1-hour blocks, the work journal contains the fine-grained breakdown (source of truth)

**Rule:**
- If multiple short tasks happen in one hour, log the hour to the dominant task and document the split in the journal.

---

## 3. Key alignment log (audit anchors)

| Date | Event | Outcome / decisions | Evidence |
|---|---|---|---|
| 2026-02-13 | Expert/supervisor kickoff (scope + plan validation) | Confirmed scope/goals, tooling readiness, Scrum method. Confirmed plan is 10 days total, organized into **2 sprints** with **2 separate timeplans**. | `evidence/meeting-notes/2026-02-13_expert-meeting.md` |
| 2026-02-19 | Sprint 1 review + retro | Sprint 1 baseline demonstrated (API + tests + perf + docs). Sprint 2 seeded with runtime PoC + real adapter integration. | `evidence/meeting-notes/2026-02-19_sprint-1-review-retro.md` |
| 2026-02-25 | Expert/supervisor check-in | Confirmed focus on documentation quality, regular commits, earlier transfer into A4 format, technical presentation readiness, and submission discipline. Frontend component-based UI expectation was discussed. | `evidence/meeting-notes/2026-02-25_expert-meeting.md` |
| 2026-02-26 | Runtime + UI validation checkpoint | Real runtime, backend endpoint, automated tests, and frontend demo UI were validated locally and stored as evidence. | runtime/API/UI screenshots under `evidence/screenshots/` |
| 2026-02-27 | Browser smoke test added | Added one automated browser test to formalize frontend smoke validation and reduce manual-only UI verification risk. | `frontend/e2e/ui-smoke.spec.ts` + Playwright run evidence |

---

## 4. Deviation log (Soll/Ist)

| Date | Task / Issue | Soll | Ist | Deviation | Reason | Action / decision | Evidence |
|---|---|---:|---:|---:|---|---|---|
| 2026-02-13 | Git setup + project bootstrap | 1h | 2h | +1h | git identity/auth issues | documented setup steps; updated setup notes | commit reference + setup notes |
| 2026-02-13 | pytest import path error | 1h | 1h | 0h | package/import structure | fixed imports + confirmed tests pass | commit reference |
| 2026-02-13 | perf run initially failed | 0.5h | 0.5h | 0h | backend not running | ran backend first; documented run order | `evidence/perf/2026-02-18_1332_results.json` |
| 2026-02-26 | initial runtime PoC failed | 0.5h | 0.5h | 0h | incorrect model file path | corrected command to use local file in `models/` | `evidence/runtime/2026-02-26_llamacpp_run.log` + `evidence/screenshots/2026-02-26_llamacpp_success.png` |
| 2026-02-26 | extra diagnostic/runtime text appeared in UI responses | 1h | 1h | 0h | llama.cpp CLI output contained extra diagnostic text / repeated content | tightened response extraction and fallback handling in `LlamaCppAdapter`; revalidated clean responses | `evidence/screenshots/2026-02-26_ui_fixed_extra_diagnostics_output.png` + clean UI screenshots |
| 2026-02-27 | Docker validation blocked on company machine | 0.5h | 0.5h | 0h | Docker Desktop unavailable / company restriction | kept Docker artifacts as optional deliverable only; did not treat container runtime as required for core acceptance | internal environment limitation note |

---

## 5. Risk register
Probability: L/M/H. Impact: L/M/H.

| ID | Risk | Probability | Impact | Mitigation (specific) | Trigger | Owner | Status |
|---|---|---|---|---|---|---|---|
| R1 | HF artifacts incompatible with llama.cpp | M | H | use GGUF repo OR timebox conversion; document steps | cannot load model/tokenizer mismatch | me | **mitigated** |
| R2 | 16GB RAM causes instability / OOM | M | H | use quantized GGUF (Q4 baseline); limit context; monitor memory | OOM / swap thrashing | me | open |
| R3 | Latency noticeable → demo feels laggy | M | H | optimize backend; add clear UX states; keep streaming out of scope | p95 high / visible lag | me | **partly mitigated** |
| R4 | Scope creep | M | M | freeze minimal API scope; backlog priorities; enforce DoD | milestones threatened | me | **controlled** |
| R5 | Timebox breach due to unknowns | M | H | strict sprint exit criteria; cut scope to protect demo | milestone slip | me | open |
| R6 | Licensing/IP concerns for dependencies | L | H | record sources/licenses; supervisor check if unclear | policy uncertainty | me + supervisor | open |
| R7 | HF model license/restrictions unsuitable | L/M | H | document license string + usage notes; supervisor confirmation | restrictive terms found | me + supervisor | open |
| R8 | UI validation relies only on manual checks | M | M | add one automated browser smoke test | UI regressions not caught quickly | me | **mitigated** |
| R9 | Docker cannot be fully validated on company device | M | M | treat Docker as optional/secondary packaging path; keep local run path as primary | no Docker runtime available | me | **accepted / documented** |

---

## 6. Problems encountered (evidence log)
This is the audit trail for issues and how they were solved.

| Date | Problem | Impact | Resolution | Evidence |
|---|---|---|---|---|
| 2026-02-13 | pytest import path error | blocked tests | fixed package layout/imports | commit reference |
| 2026-02-13 | perf script connection refused | blocked perf evidence | ran backend first; documented run order | `evidence/perf/2026-02-18_1332_results.json` + README note |
| 2026-02-26 | wrong GGUF path in initial `llama-cli` command | blocked first runtime PoC | corrected command to use the local model file in `models/` | `evidence/screenshots/2026-02-26_llamacpp_success.png` |
| 2026-02-26 | extra diagnostic/runtime text appeared in UI responses | reduced UI quality | tightened response extraction/cleanup in `LlamaCppAdapter` and revalidated clean output | `evidence/screenshots/2026-02-26_ui_fixed_extra_diagnostics_output.png` |
| 2026-02-26 | response repetition still appeared in some follow-up prompts | inconsistent UX quality | improved response cleanup + limited prompt history | clean UI validation screenshots |
| 2026-02-27 | Docker command unavailable on company machine | blocked full container verification | documented Docker as optional packaging path, not required for core demo acceptance | local environment evidence / internal note |

---

## 7. Current status summary
Current project status is **functionally complete for the defined demo scope**:

- real local inference works with `llama.cpp`
- backend endpoint works and preserves the intended OpenAI-style contract
- frontend demo UI is usable
- backend automated tests pass
- one automated browser smoke test passes
- performance baseline exists and is traceable
- remaining work is mainly:
  - documentation refinement / A4 transfer
  - optional packaging polish
  - final evidence selection and presentation preparation

This means the main risk is no longer technical feasibility, but **final documentation quality and handover quality**.