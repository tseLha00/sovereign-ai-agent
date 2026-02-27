# A04 — Time plan (v0.2)

## Version history
- **v0.1** — Initial two-sprint Scrum planning structure created, including 1-hour block Should/Is tracking.
- **v0.2** — Refined Sprint 2 milestones, clarified final documentation-transfer phase, and aligned references to the final timeplan files.

## 1. Planning approach
The time plan follows a **Scrum-based execution** with two sprints and explicit review points.
Time is planned and tracked in **1-hour blocks** to enable transparent **Should/Is** comparisons and deviations logging.

- Planning tool: Excel-based Gantt (Should/Is, 1h blocks)
- Backlog tool: GitHub Issues + GitHub Project (Kanban)
- Evidence: commits, issue history, meeting notes, perf results, test results

## 2. Calendar constraints

### IPA working days (execution)
**Sprint 1 (4 IPA days):**
- Day 1: Fri 13.02.2026
- Day 2: Tue 17.02.2026
- Day 3: Wed 18.02.2026
- Day 4: Thu 19.02.2026

**Sprint 2 (remaining IPA days):**
- Day 5: Fri 20.02.2026
- Day 6: Tue 24.02.2026
- Day 7: Wed 25.02.2026
- Day 8: Thu 26.02.2026
- Day 9: Fri 27.02.2026
- Day 10: Tue 03.03.2026

### Non-IPA days / constraints
- Mondays are school days (no IPA work recorded).
- Out-of-office/blocked days are represented as grey columns in the time plan.

## 3. Sprint structure and goals

### Sprint 1 (Days 1–4): Baseline + discipline
Goal: deliver a **working baseline** with measurable evidence:
- backend skeleton + adapter architecture
- OpenAI-style endpoint: `/v1/chat/completions` (non-streaming baseline)
- contract tests for API shape + health endpoint
- performance baseline script + stored results
- initial documentation and decision discipline (A01/A02/A03/A04/A05/A12/H01/H08)

Sprint 1 exit criteria:
- `make test` passes
- `make perf` produces JSON results saved under evidence
- API contract response shape is stable (tests)
- decision record H01 exists (**final runtime decision** + compatibility validation plan)

### Sprint 2 (Days 5–10): Apertus integration + demo readiness
Goal: integrate the real inference runtime and deliver a demo-quality UX:
- real Apertus inference behind adapter
- UI features expected for a chat experience (responsive, error handling, reset, etc.)
- latency/UX improvements (backend + UX mitigation)
- stability improvements + final evidence and documentation completion

Sprint 2 exit criteria:
- `/v1/chat/completions` uses real inference at least for a minimal path
- demo UI usable on common devices/resolutions
- perf results compared against baseline and documented
- final documentation and evidence complete

## 4. Milestones (shown as vertical lines in the Gantt)
Milestones mark **reviewable checkpoints**, not just tasks.

- **M1 (end of Sprint 1):** Baseline complete  
  (API + tests + perf baseline + documentation discipline)
- **M2 (Sprint 2 early):** Apertus 8B HF artifacts + license documented, and compatibility path confirmed  
  (GGUF direct load or conversion plan)
- **M3 (Sprint 2):** First successful Apertus inference through the API  
  (request → runtime → response)
- **M4 (Sprint 2):** UI usable on multiple devices  
  (responsive + common chat features)
- **M5 (final):** Final demo + evidence + documentation complete

## 5. Should/Is tracking rule (1-hour block approach)
- **Should** is planned in 1-hour increments in the time plan.
- **Is** is tracked in the same grid.

### Handling deviations and partial hours
Because the grid is 1-hour blocks:
- Combine short tasks into one hour block and document the breakdown in the work journal, or
- If your Excel supports it, represent half-hours using a second marking, and still document details in the work journal.

### Transparency rule
If totals look “messy” due to rounding:
- The **work journal is the source of truth** for exact breakdowns.
- Deviations are documented in A05 and linked to evidence (issues/commits).

## 6. References
- Time plan file: `planning/Timeplan.xlsx` (or your chosen path)
- Backlog board: GitHub Project (Kanban)
- Work journal: `docs/journal/day-XX.md`
