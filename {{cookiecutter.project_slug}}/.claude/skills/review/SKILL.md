---
name: review
description: Anti-slop code review with structured rubric and confidence threshold
---

# Skill: Review (Anti-Slop Rubric)

## Purpose

Review code changes against a structured rubric. Filter noise with a confidence
threshold — only findings above 80/100 confidence reach the human.

## Rubric

Score each dimension 0-100. Flag only findings with confidence ≥ 80.

| # | Dimension | Question |
|---|-----------|----------|
| 1 | **Naming quality** | Can I understand what each function does from its name and signature alone? |
| 2 | **Domain language** | Does the code use terms from `UBIQUITOUS_LANGUAGE.md`? |
| 3 | **Function responsibility** | Does each function do one thing? Any over 30 lines? |
| 4 | **Architectural fit** | Does this code belong where it's placed? Does it follow patterns in `ARCHITECTURE.md`? |
| 5 | **Unnecessary duplication** | Did this create something that already exists elsewhere? |
| 6 | **Refactoring avoidance** | Was new code bolted on where existing code should have been restructured? |
| 7 | **Cognitive load** | Could someone unfamiliar with this module understand the change without reading other files? |

## Process

1. Read `ARCHITECTURE.md` and `UBIQUITOUS_LANGUAGE.md` for context.
2. Read the diff.
3. Score each dimension. Write a one-sentence finding per dimension.
4. Filter: suppress any finding with confidence < 80.
5. Output findings with dimension, confidence score, file:line, and suggested fix.

## Output Format

```
## Review: {description of change}

### Findings (confidence ≥ 80)

**[Naming quality — 85]** `src/foo.py:42`
`process_data()` does not convey what it processes or produces. Rename to `normalize_transaction_amounts()`.

### Suppressed findings
{count} findings below confidence threshold.

### Learnings candidates
{Any pattern worth adding to docs/learnings/learnings.md}
```

## Reference

See `eval.md` for the AutoResearch evaluation methodology for this rubric.
