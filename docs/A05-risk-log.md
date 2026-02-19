# A05 — Progress and risk tracking (v0.2)

## 1. Tracking cadence
- Daily: update work journal + move GitHub issues on the board
- Per sprint: sprint review + retro notes stored under `evidence/meeting-notes/`

## 2. Soll/Ist tracking approach
- **Soll:** time plan Excel (1-hour blocks)
- **Ist:** filled daily in Excel
- **Exact minutes:** if work does not fit 1-hour blocks, the work journal contains the fine-grained breakdown (source of truth).

Rule:
- If multiple short tasks happen in one hour, log the hour to the dominant task and document the split in the journal.

---

## 3. Key alignment / kickoff log (audit anchors)

| Date | Event | Outcome / decisions | Evidence |
|---|---|---|---|
| 2026-02-13 | Expert/supervisor kickoff (scope + plan validation) | Confirmed scope/goals, tooling readiness, Scrum method. Confirmed plan is 10 days total, organized into **2 sprints** with **2 separate timeplans**. | `evidence/meeting-notes/2026-02-13_expert-kickoff.md` |

---

## 4. Deviation log (Soll/Ist)
Use this when a deviation affects time plan, scope, or approach.

| Date | Task / Issue | Soll | Ist | Deviation | Reason | Action / decision | Evidence |
|---|---|---:|---:|---:|---|---|---|
| 2026-02-13 | Git setup + project bootstrap | 1h | 2h | +1h | git identity/auth issues | documented setup steps; updated README checklist | commit link + README section |
| 2026-02-13 | pytest import path error | 1h | 1h | 0h | package/import structure | fixed imports + confirmed tests pass | commit link |
| 2026-02-13 | perf run initially failed | 0.5h | 0.5h | 0h | backend not running | documented “run app then perf” | `evidence/perf/..._results.json` |

---

## 5. Risk register
Probability: L/M/H. Impact: L/M/H.

| ID | Risk | Probability | Impact | Mitigation (specific) | Trigger | Owner | Status |
|---|---|---|---|---|---|---|---|
| R1 | HF artifacts incompatible with llama.cpp | M | H | use GGUF repo OR timebox conversion; document steps | cannot load model/tokenizer mismatch | me | open |
| R2 | 16GB RAM causes instability / OOM | M | H | use quantized GGUF (Q4 baseline); limit context; monitor memory | OOM / swap thrashing | me | open |
| R3 | Latency noticeable → demo feels laggy | M | H | optimize backend; add “thinking…” UX; keep streaming as nice-to-have | p95 high / visible lag | me | open |
| R4 | Scope creep | M | M | freeze minimal API scope; backlog priorities; enforce DoD | milestones threatened | me | open |
| R5 | Timebox breach due to unknowns | M | H | strict sprint exit criteria; cut scope to protect demo | milestone slip | me | open |
| R6 | Licensing/IP concerns for dependencies | L | H | record sources/licenses; supervisor check if unclear | policy uncertainty | me + supervisor | open |
| R7 | HF model license/restrictions unsuitable | L/M | H | document license string + usage notes; supervisor confirmation | restrictive terms found | me + supervisor | open |

---

## 6. Problems encountered (evidence log)
This is the audit trail for issues and how they were solved.

| Date | Problem | Impact | Resolution | Evidence |
|---|---|---|---|---|
| 2026-02-13 | pytest import path error | blocked tests | fixed package layout/imports | commit link |
| 2026-02-13 | perf script connection refused | blocked perf evidence | run backend first; documented steps | `evidence/perf/..._results.json` + README note |
