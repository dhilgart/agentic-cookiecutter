# Instrumentation — {{cookiecutter.project_name}}

Every research-backed component is a hypothesis under active test.
This file defines what "broken" looks like, the questions to ask, and what to
do if a component isn't earning its keep.

Referenced by the compound skill during retrospectives.

---

## Learning Store (`docs/learnings/learnings.md`)

**Broken looks like:**
- Entries accumulate but are never referenced in planning or review
- Helpful/harmful counters stuck at zero — no one is updating them
- Type tags (strategy, recovery, optimization, pattern) don't map to real patterns
- File grows without pruning or promotion to CLAUDE.md

**Retrospective questions:**
1. Were any learning entries referenced during this work session?
2. Are counters being updated when entries are relevant?
3. Are type tags useful for finding entries, or just noise?
4. Are entries retrieved at the right times (planning, review, compound)?
5. Has anyone pruned stale entries?

**Fallback:** If entries are never referenced, simplify to a flat list of
one-liners without metadata. Capture WHY the structured format failed.

---

## Anti-Slop Review Rubric (`.claude/skills/review/`)

**Broken looks like:**
- A dimension never flags anything (dead dimension)
- A dimension flags everything (false positive noise)
- Human routinely overrides a dimension's findings
- Confidence threshold filters out real issues (suppression errors)

**Retrospective questions:**
1. Are all 7 dimensions producing actionable findings?
2. Which dimensions are never triggered? Should they be removed or reworded?
3. Which dimensions are always overridden by the human?
4. Is the 80/100 confidence threshold filtering noise or hiding real issues?
5. Check `eval.md` — are TP/FP/suppression counters being updated?

**Fallback:** Drop to 3-4 high-signal dimensions. Remove any dimension with
>30% FP rate. Capture which dimensions were dropped and why.

---

## CLAUDE.md Conventions

**Broken looks like:**
- Conventions the agent follows anyway without CLAUDE.md (no value added)
- Conventions the agent ignores despite being listed
- File grows beyond 50 lines without pruning
- Conventions duplicate what the codebase already demonstrates

**Retrospective questions:**
1. Did any convention prevent a review failure this session?
2. Which conventions are redundant with the codebase's own patterns?
3. Which conventions are being ignored? Why?
4. Is the file still under 50 lines?

**Fallback:** Strip to only conventions that have prevented real failures
(evidence from review findings or learnings). Capture what was removed and why.

---

## Compound Step (`.claude/skills/compound/`)

**Broken looks like:**
- Codification happens but learnings are never referenced later
- Learnings are referenced but don't change agent behavior
- Step is routinely skipped under time pressure
- Retrospective questions feel like busywork, answers are copy-paste

**Retrospective questions:**
1. Were any new learnings captured this session?
2. Did any existing learning change how work was done?
3. Was the compound step skipped? Why?
4. Were retrospective answers thoughtful or formulaic?
5. Are any entries ready for promotion (helpful >= 3)?

**Fallback:** If consistently skipped, reduce to a single question:
"What was non-obvious?" Capture why the full process was abandoned.

---

## Zoom Process / Plan Skill (`.claude/skills/plan/`)

**Broken looks like:**
- Human prompted at inner zoom levels for things derivable from outer artifacts
  (spec quality problem — outer levels aren't doing their job)
- Agent proceeds confidently but fails review (D75 self-check too permissive)
- Zoom levels feel bureaucratic, not progressive
- Artifacts accumulate but go unread
- Loops back to higher levels don't happen when they should

**Retrospective questions:**
1. Did each zoom level's artifact help resolve questions at the next level?
2. Were there levels that felt like busywork?
3. Did D75 self-check escalate too often or too rarely?
4. Did the agent loop back to a higher level when needed?
5. Were story file artifacts read during implementation?

**Fallback:** If zoom levels feel bureaucratic, collapse to two levels:
plan (story file) and implement. Capture which intermediate levels were
dropped and why.

---

## Mermaid Style Guide (`docs/mermaid-style-guide.md`)

**Broken looks like:**
- Diagrams don't use the defined encoding channels
- Readers don't understand visual conventions without the legend
- Diagrams look good but don't convey more info than plain boxes-and-arrows

**Retrospective questions:**
1. Are the visual encoding channels being used in new diagrams?
2. Do readers understand diagrams without referencing the style guide?
3. Are diagrams more informative than plain monochrome alternatives?

**Fallback:** If encoding channels aren't used, simplify to "use Mermaid,
be consistent" with no encoding rules. Capture what was too prescriptive.

---

## Hook Configurations (`.claude/hooks.json`)

**Broken looks like:**
- PostToolUse hooks slow down editing to the point of frustration
- Hooks produce noisy output that gets ignored
- The git guardrail fires on legitimate operations (false positive)
- Stop hook message is never acted on

**Retrospective questions:**
1. Are PostToolUse hooks catching real issues on edit?
2. Is hook output noisy or actionable?
3. Has the git guardrail ever prevented a real mistake?
4. Does the Stop hook prompt useful reflection or get dismissed?

**Fallback:** Disable noisy hooks. Keep only hooks that have prevented a
real incident. Capture which hooks were disabled and why.

---

## Plugin / Skill Composition (`.claude/settings.json`)

**Broken looks like:**
- Listed plugins aren't installed or don't exist
- Skills are listed but never invoked
- Permission allowlist is too narrow (blocks legitimate work) or too broad
  (allows destructive actions without confirmation)

**Retrospective questions:**
1. Were all listed plugins actually available and functional?
2. Which skills were invoked this session? Which were never used?
3. Did permissions block any legitimate action?
4. Did permissions allow any action that should have required confirmation?

**Fallback:** Remove unused plugins/skills after 3 sessions of non-use.
Tighten or loosen permissions based on incidents. Capture changes and reasons.

---

## Story Files (`stories/`)

**Broken looks like:**
- Stories written but acceptance criteria not used during implementation
- Mental model diagrams skipped or perfunctory
- "Interfaces Changed" section always empty
- Completed stories never moved to `done/`

**Retrospective questions:**
1. Were acceptance criteria checked off during implementation?
2. Did the mental model diagram help with understanding?
3. Were interface changes documented before coding started?
4. Are completed stories being moved to `done/`?

**Fallback:** If the full template is too heavy, reduce to: title, why,
acceptance criteria. Capture which sections were dropped and why.

---

## How to Use This File

1. During the **compound step**, review the sections relevant to work done.
2. Answer the retrospective questions honestly.
3. If "broken" criteria are met, consider the fallback.
4. Log any changes to `docs/learnings/learnings.md`.
5. If a fallback is activated, record an ADR in `docs/decisions/`.
