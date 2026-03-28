---
name: compound
description: Extract and codify learnings at the end of a work session
---

# Skill: Compound (Learning Codification)

## Purpose

After completing a work session, extract learnings and codify them into the
project's learning store. Zoom out from the implementation to capture what
was non-obvious, surprising, or worth remembering.

## Trigger

Run at the end of a significant work session, or when a story is moved to `stories/done/`.

## Process

### Step 1 — Retrospective questions

Answer each question briefly:
1. What took longer than expected, and why?
2. What did I have to look up that I didn't already know?
3. What decision was made that a future agent wouldn't know from the code alone?
4. What went wrong and how was it recovered?
5. What pattern was reused from a prior learning? (Update its helpful counter.)
6. Is any entry in `docs/learnings/learnings.md` now wrong or outdated?

### Step 2 — Draft new entries

For each non-obvious insight, draft a learning entry:

```
- [LNNN] type:{strategy|recovery|optimization|pattern} | helpful:1 harmful:0 |
  {One sentence: what to do and why, specific enough to apply without context.} |
  source:{story-slug} | added:{date}
```

Types:
- **strategy** — a process or approach that kept options open or reduced risk
- **recovery** — how to get out of a specific failure mode
- **optimization** — a shortcut or routing decision that improves efficiency
- **pattern** — a code pattern that recurs in this project

### Step 3 — Promotion check

Scan entries with `helpful` counter ≥ 3. For each:
- Should it graduate to `CLAUDE.md` as a convention? → Propose the addition.
- Should it become a deterministic gate? → File a story to add it.

### Step 4 — Update learnings.md

Append new entries to `docs/learnings/learnings.md`. Never rewrite existing entries.
Update counters for referenced entries.

### Step 5 — Instrumentation check

Review `docs/instrumentation.md` for components touched this session.
For each:
- Are any "broken" criteria met? Flag them.
- Answer the relevant retrospective questions.
- If a fallback should be activated, draft an ADR in `docs/decisions/`.

## Output

Updated `docs/learnings/learnings.md` with new entries appended.
Optional: proposed additions to `CLAUDE.md` if promotion criteria met.
Optional: instrumentation flags if "broken" criteria are met.
