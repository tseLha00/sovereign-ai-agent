# A05 — Progress and risk tracking (v0.1)

## 1. Tracking cadence
- Daily: update work journal + move GitHub issues on the board
- Per sprint: review + retro notes saved under `evidence/meeting-notes/`

## 2. Soll/Ist tracking approach
- **Soll:** time plan Excel (1-hour blocks)
- **Ist:** filled daily in Excel
- **Exact minutes:** if work does not fit 1-hour blocks, the work journal contains the fine-grained breakdown (source of truth).

Rule:
- If multiple short tasks happen in one hour, log the hour to the dominant task and document the split in the journal.

## 3. Deviation log (Should/Is)
Use this only when there is a meaningful deviation that affects plan, scope, or approach.

| Date | Task / Issue | Soll | Ist | Deviation | Reason | Action / decision | Evidence link |
|---|---|---:|---:|---:|---|---|---|
| 2026-02-13 | Git setup + project bootstrap | 1h | 2h | +1h | git identity/auth issues | document setup; update checklist | link to commit / screenshot |
|  |  |  |  |  |  |  |  |

## 4. Risk register
Probability: L/M/H. Impact: L/M/H. Keep mitigations specific and testable.

| ID | Risk | Probability | Impact | Mitigation (specific) | Trigger | Owner | Status |
|---|---|---|---|---|---|---|---|
| R1 | Apertus artifacts incompatible with chosen runtime | M | H | validate model loading early (Sprint 2 Day 5/6); define fallback runtime | cannot load model / tokenizer mismatch | me | open |
| R2 | Memory constraints (16GB) cause instability or OOM | M | H | use quantized artifacts; limit context length; monitor memory during PoC | OOM, swap thrashing | me | open |
| R3 | Latency noticeable → demo UX feels “laggy” | M | H | optimize backend; add frontend thinking state; consider streaming later | p95 high or user-visible lag | me | open |
| R4 | Scope creep (too many endpoints/features) | M | M | freeze minimal API scope early; backlog with priorities; enforce DoD | backlog growth threatens milestones | me | open |
| R5 | Timebox breach (miss milestones due to unknowns) | M | H | strict sprint exit criteria; cut scope to protect demo | milestone slip | me | open |
| R6 | Licensing/IP concerns for dependencies | L | H | record sources and licenses; supervisor check for sensitive deps | uncertainty about use | supervisor/me | open |

## 5. Problems encountered (evidence log)
This is the “audit trail” for issues and how you solved them.

| Date | Problem | Impact | Resolution | Evidence link |
|---|---|---|---|---|
| 2026-02-13 | pytest import path error (module not found) | blocked tests | fixed package layout + import path | link to commit / screenshot |
| 2026-02-13 | perf script failed (connection refused) | perf evidence blocked | run app before `make perf`; add README note | link to perf output + note |
|  |  |  |  |  |
