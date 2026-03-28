# Skill: Plan (Zoom-Based Progressive Concretization)

## Purpose

Translate a human request into a concrete implementation plan using zoom-based
progressive concretization. Resolve ambiguity autonomously when possible; pull
in the human only for genuine uncertainty.

## Process

### Step 1 — Identify questions (zoom out)

List 3-4 questions this task raises:
- What problem does this solve? For whom?
- What interfaces or modules does it touch?
- What constraints apply (performance, backwards-compat, style)?
- What could go wrong?

### Step 2 — Self-check gate (D75)

For each question, ask: **"Can I answer this from existing artifacts?"**

Artifacts to check, in order:
1. `ARCHITECTURE.md` — module boundaries, conventions
2. `UBIQUITOUS_LANGUAGE.md` — correct terminology
3. `docs/learnings/learnings.md` — past patterns and recoveries
4. `stories/` — related story files
5. Code itself — existing patterns to follow

If YES → resolve autonomously and proceed.
If NO → surface the specific uncertainty to the human as a concrete question.

### Step 3 — Produce the plan artifact

Write a story file in `stories/` using the story template. Include:
- **Why:** Problem and user
- **Mental Model:** Mermaid diagram showing fit in existing system
- **Acceptance Criteria:** Failing-to-passing checklist (each item verifiable)
- **Interfaces Changed:** New or modified types/signatures
- **Notes:** Resolved questions and edge cases

### Step 4 — Verify consistency

Before declaring the plan ready:
- [ ] Acceptance criteria are independently verifiable
- [ ] No term is used that isn't in UBIQUITOUS_LANGUAGE.md (or add it)
- [ ] Plan respects module boundaries in ARCHITECTURE.md
- [ ] No open questions remain (or they are explicitly flagged for human)

## Output

A completed story file at `stories/{slug}.md`, ready for implementation.

## When to escalate

Escalate to the human when:
- The decision has architectural implications not covered by ARCHITECTURE.md
- Two valid approaches exist and the choice depends on unstated priorities
- The feature scope is larger than one work session
