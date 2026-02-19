# Expert / Supervisor kickoff — 2026-02-13

## Participants
- Supervisor: Enrico Viola
- Apprentice: Tsering Lhamo Anodunkhartsang
- (Experts present / consulted): Yves Kaufmann, Mirio Joël Eggmann (as applicable)

## Purpose
Confirm project scope, goals, and that the 10-day IPA plan is understood and feasible.

## Topics discussed
1) **Scope + goals**
- Build an on-prem “sovereign AI” chatbot demo with Apertus LLM.
- Provide a web UI + OpenAI-style API minimum: `POST /v1/chat/completions`.

2) **Constraints**
- Target machine: Mac mini M4, 16 GB RAM.

3) **Project method**
- Scrum approach with 2 sprints (baseline first, integration second).

4) **Planning**
- Reviewed time plan.
- Decision: maintain **two separate timeplans** (Sprint 1 and Sprint 2).

5) **Tools readiness**
- Confirmed dev tools and workflow exist (repo, issue board, evidence discipline, testing/perf scripts approach).

## Decisions
- Project method: Scrum with Sprint 1 baseline + Sprint 2 integration/demo readiness.
- Two timeplans: one per sprint.

## Open questions / risks
- Confirm exact Apertus 8B model source + artifact format compatibility with chosen runtime.
- Validate local inference feasibility with quantized artifacts.

## Action items
- Finalize Sprint 1 baseline deliverables:
  - backend skeleton + `/health` + `/v1/chat/completions`
  - contract tests
  - perf baseline script + stored JSON
  - documentation set: A01/A02-A03/A04/A05/A12/H01/H08
- Prepare runtime compatibility evidence (PoC) to reduce Sprint 2 risk.

## Evidence references
- Timeplan: `docs/planning/` (Sprint 1 + Sprint 2)
- Board: GitHub Project (Kanban)
