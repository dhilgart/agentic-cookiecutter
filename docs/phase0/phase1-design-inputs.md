# Phase 1 Design Inputs — Synthesized from Phase 0 Research

**75 decisions, 14 core principles, 155+ practices → organized into what Phase 1 needs to build.**
**Date:** 2026-03-27

---

## 1. What the Cookiecutter IS (and isn't)

The cookiecutter generates a **configured workspace**, not a Python library (D46, D66, D67).

**It produces:**
- Configuration files (settings.json, pyproject.toml, .claude/)
- Markdown-based agent instructions (CLAUDE.md, skills, story templates)
- Hook configurations (PostToolUse, Stop, git guardrails)
- Documentation templates (README, ARCHITECTURE.md, ADR directory)
- Learning store structure
- A minimal Python src/ scaffold with typed stubs

**It does NOT produce:**
- Python modules that implement workflow orchestration
- Custom review agents in Python
- A task queue system in code
- Any component that exists as an official Claude Code plugin

**Build-vs-compose rule (D66):** Use pre-built plugins first. Switch to custom ONLY when a plugin demonstrably fails our criteria. Custom components are .md skill files and hook configs, not Python (D67).

---

## 2. The Development Process (D74, D75)

**Zoom-based progressive concretization.** One loop at every level:

```
Identify 3-4 questions → Self-check (D75): "Can I answer from higher-level artifacts?"
  → YES: resolve autonomously, produce artifact
  → NO: escalate SPECIFIC uncertainty to human
→ Verify consistency with levels above → Zoom in (or loop back up)
```

**Human involvement is pull-based (D75).** Agent works autonomously, pulls human in only for genuine ambiguity. Quality of outer zoom levels determines autonomy of inner levels.

**D47 (Plan→Work→Assess→Compound) is the simplified shorthand:** Plan = outer zooms. Work = implementation. Assess = verify + gates. Compound = zoom out + codify.

**Phase 1 must define:** How the zoom process is encoded in skills/prompts. What artifact is produced at each zoom level. How the self-check gate (D75) is implemented in a skill prompt.

---

## 3. What the Cookiecutter Generates — Complete File Tree

Based on all decisions, the cookiecutter should produce:

```
{{cookiecutter.project_slug}}/
├── .claude/
│   ├── settings.json              # Plugin configs, permissions (D22, D66)
│   ├── hooks.json                 # PostToolUse, Stop hooks (D14, D23)
│   ├── commands/                  # Slash commands
│   │   ├── commit-push-pr.md      # Inner loop workflow
│   │   └── ...
│   └── skills/                    # Project-specific skills
│       ├── plan/                  # Outer zoom planning skill
│       │   └── SKILL.md
│       ├── review/                # Anti-slop review rubric
│       │   ├── SKILL.md
│       │   └── eval.md            # AutoResearch eval (D36)
│       ├── compound/              # Learning codification skill
│       │   └── SKILL.md
│       └── ...
├── CLAUDE.md                      # Minimal, surgical (D11)
├── ARCHITECTURE.md                # High-level mental map (D61)
├── README.md                      # Scaffolded: organizer→quickstart→tutorial→ref (D62)
├── UBIQUITOUS_LANGUAGE.md         # Domain terms (D17)
├── pyproject.toml                 # All tooling config (D56)
├── src/
│   └── {{cookiecutter.package_name}}/
│       ├── __init__.py            # __all__ exports (D54)
│       └── ...                    # Typed stubs
├── tests/
│   ├── conftest.py
│   └── ...
├── docs/
│   ├── decisions/                 # ADR infrastructure (D64)
│   │   └── 0000-template.md
│   ├── learnings/                 # Learning store (D21, D39, D68)
│   │   └── learnings.md           # Structured bullets with metadata
│   └── mermaid-style-guide.md     # Visual encoding conventions (D63)
├── stories/                       # Story file templates (D25, D44, D79)
│   ├── template.md                # Includes failing-to-passing checklist
│   └── done/                      # Completed stories
└── .github/
    └── workflows/                 # CI with quality gates
        └── ci.yml                 # ruff + mypy + tests + complexity (D56)
```

---

## 4. CLAUDE.md Contents (D11, D20, D51, D54, D55, D59, D65)

Must be minimal. Every line must earn its place. Conventions, not checklists.

```markdown
# CLAUDE.md

## Project
{one-sentence description}

## Setup
{activate venv command}
{install command}
{test command}

## Conventions
- Use dataclasses for internal types, TypedDict for external dict-shaped data,
  Pydantic for validated input. Never pass dict when shape is known.
- Type hints on all functions. mypy --strict enforced.
- Search the codebase before creating new utilities.
- Write code readable top-to-bottom: guard clauses, named intermediates,
  one abstraction level per function.
- Use domain language from UBIQUITOUS_LANGUAGE.md.
- See ARCHITECTURE.md for module structure and boundaries.

## Quality Gates (automated)
- PostToolUse: ruff format + mypy check after every edit
- Pre-commit: ruff + mypy + pytest + cognitive complexity < 15
- Review: /code-review runs before PR

## Learnings
- See docs/learnings/learnings.md for project-specific patterns.
```

**Target: under 50 lines. Under 2K tokens.** (Boris Cherny's team: 2.5K tokens.)

---

## 5. Hook Configurations (D14, D23, D19)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "ruff format --quiet $FILE && ruff check --fix --quiet $FILE && mypy --no-error-summary $FILE || true"
      }
    ],
    "Stop": [
      {
        "command": "echo 'Verify: Do all tests pass? Is the change consistent with ARCHITECTURE.md?'"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "git commit|git push",
        "command": "python -c \"import sys; assert 'main' not in sys.argv, 'Never commit to main'\""
      }
    ]
  }
}
```

---

## 6. Anti-Slop Pipeline (D50, D34, D40, D45, D52, D53, D60)

### Tier 1: Deterministic (automated, every file edit)
| Gate | Tool | Trigger |
|------|------|---------|
| Formatting | ruff format | PostToolUse |
| Linting | ruff check | PostToolUse |
| Type checking | mypy --strict | PostToolUse |
| Cognitive complexity | ruff/flake8 cognitive-complexity plugin, threshold 15 | CI |
| Dead code | ruff (F841, etc.) | CI |
| Test coverage | pytest-cov, minimum TBD | CI |

### Tier 2: Stochastic (LLM-judged, separate review agent, per D26.1)
Use Anthropic's official code-review plugin as baseline (D45). Customize review prompt with these dimensions (D40, D60):

| Dimension | Question |
|-----------|----------|
| Naming quality | Can I understand what each function does from its name and signature alone? |
| Domain language | Does the code use terms from UBIQUITOUS_LANGUAGE.md? |
| Function responsibility | Does each function do one thing? Any over 30 lines? |
| Architectural fit | Does this code belong where it's placed? Does it follow patterns in ARCHITECTURE.md? |
| Unnecessary duplication | Did this create something that already exists elsewhere? (D51) |
| Refactoring avoidance | Was new code bolted on where existing code should have been restructured? |
| Cognitive load | Could someone unfamiliar with this module understand the change without reading other files? |

Confidence scoring (threshold 80/100) filters noise. Only findings above threshold reach the human.

---

## 7. Learning Store (D21, D39, D48, D68, D27)

**File:** `docs/learnings/learnings.md`

**Format (ACE-informed, D39):**

```markdown
# Project Learnings

## Active Entries

- [L001] type:strategy | helpful:3 harmful:0 | Protocol for Store before
  choosing implementation kept options open without blocking. |
  source:initial-build | added:2026-03-27

- [L002] type:recovery | helpful:1 harmful:0 | When mypy reports
  incompatible types on dict access, likely need TypedDict or dataclass. |
  source:auth-module | added:2026-03-28

- [L003] type:optimization | helpful:2 harmful:1 | Haiku handles
  pure-dataclass tasks reliably. Route by default. |
  source:model-routing-eval | added:2026-03-29
```

**Rules:**
- Append-only updates. Never rewrite the file (D39, P22.2).
- Counters updated by review agents when entries are referenced.
- Entries recurring 3+ times as review findings graduate to CLAUDE.md conventions (D27) or deterministic gates.
- Human reviews during compound step — validates, prunes, promotes.
- Ship with full structure from day one (D68). Instrument with retrospective questions (D69).

---

## 8. Settings.json — Plugin Composition (D66, D45, D18)

```json
{
  "plugins": {
    "official": [
      "code-review",
      "feature-dev",
      "ralph-loop",
      "commit-commands",
      "security-guidance"
    ],
    "skills": [
      "mattpocock/skills/grill-me",
      "mattpocock/skills/tdd",
      "mattpocock/skills/write-a-prd",
      "mattpocock/skills/ubiquitous-language",
      "mattpocock/skills/write-a-skill",
      "mattpocock/skills/git-guardrails"
    ]
  },
  "permissions": {
    "allow": [
      "ruff *",
      "mypy *",
      "pytest *",
      "git status",
      "git diff *",
      "git add *",
      "git commit *",
      "git checkout -b *",
      "git push *"
    ]
  }
}
```

---

## 9. Documentation Templates

### README.md structure (D62, P34.7):
1. **Advance Organizer** — one sentence, Core Concepts box (3-5 terms), Mermaid relationship diagram
2. **Quickstart** — prerequisites, one copy-paste block, expected output, < 5 min
3. **Tutorial** — guided first task with WHY explanations
4. **Architecture** — link to ARCHITECTURE.md, C4 L1-2 diagrams
5. **Reference** — config, CLI, file structure, troubleshooting
6. **Contributing** — link to ADRs, code quality standards

### ARCHITECTURE.md (D61, P34.1):
- Under 200 lines. Updated rarely.
- Module hierarchy with one paragraph per module.
- Mermaid diagram at C4 Level 1-2 with rich encoding (D63).
- Data flow narrative.
- Conventions section (what patterns are used and why).

### ADR template (D64):
```markdown
# ADR-NNNN: {Title}

## Status
{Proposed | Accepted | Superseded by ADR-NNNN}

## Context
{What problem or question triggered this decision?}

## Decision
{What was decided?}

## Alternatives Considered
{What else was considered and why was it rejected?}

## Consequences
{What are the implications? What becomes easier? Harder?}
```

---

## 10. Story File Template (D25, D44)

```markdown
# Story: {Title}

## Why
{What problem does this solve? For whom?}

## Mental Model
{How does this fit into the existing system? Mermaid diagram.}

## Acceptance Criteria (failing-to-passing checklist)
- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Interfaces Changed
{Which module interfaces are affected? New types?}

## Notes
{Constraints, edge cases, open questions resolved during planning.}
```

---

## 11. Model Routing Defaults (D72, D73)

| Activity | Default Model | Rationale |
|----------|--------------|-----------|
| Grill-me / spec / interface design | Opus | Judgment, taste, ambiguity |
| Plan annotation cycles | Opus | Nuance of human corrections |
| Implementation against clear spec | Sonnet | Mechanical; spec did the hard work |
| Simple fixes (typo, config) | Haiku | Trivially specified |
| Deterministic gates | No LLM | Tools |
| Stochastic review | Evaluate (D73) | Opus single vs Haiku swarm — test both |
| Compound / learning extraction | Sonnet | Structured extraction |

Routing refined empirically via learning store (D72 caveat). Don't trust Opus to judge what Haiku can handle — track outcomes and build a lookup.

---

## 12. pyproject.toml Quality Configuration (D56)

```toml
[tool.ruff]
target-version = "py312"
line-length = 88
src = ["src"]

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "S", "B", "A", "C4", "DTZ", "T20", "ICN", "PIE", "PT", "RSE", "RET", "SLF", "SIM", "TCH", "ARG", "PTH", "ERA"]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing"

[tool.coverage.run]
source = ["src"]
branch = true
```

---

## 13. Resolved Items (formerly open)

All Phase 1 blocking items resolved:

| Item | Resolution | Decision |
|------|-----------|----------|
| Q9: Dependency management | uv | D76 |
| Q11: Testing stack | pytest + pytest-cov always; hypothesis and mutmut as cookiecutter opt-in | D77 |
| D24a: Ralph loop | Official ralph-loop plugin first | D78 |
| D24b: Task backlog | Local story files in `stories/` directory | D79 |
| D37/D41: Context rotation | Externalize state as discipline, default to compaction, test rotation as fallback | D80 |

### Remaining open items (NOT blocking Phase 1)

| Item | Status | When |
|------|--------|------|
| Q4: Confidence threshold | 🔴 Open | Phase 5 (trust tiers) |
| Q5: Trust tier model | 🔴 Open | Phase 5 |
| Q13: Visual design science for Mermaid | 🟡 Future | When writing style guide |
| Q14: Model routing validation | 🟡 Future | Post-launch |

---

## 14. Core Principles (the "why" behind all decisions)

1. Trust through verification, not hope
2. Human time is precious
3. Fail gracefully, not silently
4. Learn explicitly
5. Slop is the enemy
6. Minimal, surgical context files
7. Solve the specification bottleneck
8. Externalize tacit knowledge
9. Supervise, don't just prompt
10. The harness matters more than the model
11. Solve the cognitive architecture problem
12. Build the theory, instrument for reality
13. Human mental energy is the scarce resource, not time
14. Five SE principle flips (docs worth it, cognitive YAGNI, don't under-design, save brains, premature cognitive optimization is good)

---

## 15. What Phase 1 Actually Needs to Do

Phase 1 is no longer "design the architecture" in the traditional sense. It's:

1. **Build the cookiecutter template** producing the file tree in Section 3
2. **Write the skill files** for: planning (zoom process + D75 self-check), review (anti-slop rubric), compound (learning codification)
3. **Configure the plugins** specified in Section 8
4. **Write the CLAUDE.md template** per Section 4
5. **Write the hook configurations** per Section 5
6. **Write the documentation templates** per Section 9 (README, ARCHITECTURE.md, ADR, story file)
7. **Set up the learning store structure** per Section 7
8. **Configure pyproject.toml** per Section 12
9. **Resolve remaining open items** per Section 13
10. **Instrument everything** per D69 (retrospective questions, "broken" criteria for each component)

Most of these are writing markdown files and TOML/JSON configuration. The "architecture" was decided in Phase 0 — Phase 1 is implementation of the workspace.
