# Agentic Coding Workflow — Project Tracker

**Project:** Python Cookiecutter for Agentic Coding Workflow (Claude Code Native)
**Status:** 🟡 Planning
**Last Updated:** 2026-03-25
**Human Time Target:** 90% ideation / 10% review
**Runtime:** Claude Code (confirmed)
**Python:** 3.12+ (confirmed)
**Layout:** src layout, single package (confirmed)

---

## Table of Contents

1. [Project Vision & Principles](#1-project-vision--principles)
2. [Ubiquitous Language](#2-ubiquitous-language)
3. [Open Questions for Human](#3-open-questions-for-human)
4. [Phase 0 — Research & Best Practices Synthesis](#4-phase-0--research--best-practices-synthesis)
5. [Phase 1 — Architecture & Design](#5-phase-1--architecture--design)
6. [Phase 2 — Cookiecutter Scaffold](#6-phase-2--cookiecutter-scaffold)
7. [Phase 3 — Core Agent System](#7-phase-3--core-agent-system)
8. [Phase 4 — Anti-Slop Pipeline](#8-phase-4--anti-slop-pipeline)
9. [Phase 5 — Human Interaction Layer](#9-phase-5--human-interaction-layer)
10. [Phase 6 — Autonomous Loop Engine (Ralph Wiggum)](#10-phase-6--autonomous-loop-engine-ralph-wiggum)
11. [Phase 7 — Learning & Adaptation System](#11-phase-7--learning--adaptation-system)
12. [Phase 8 — Dev Tooling & CI/CD](#12-phase-8--dev-tooling--cicd)
13. [Phase 9 — Integration Testing & Validation](#13-phase-9--integration-testing--validation)
14. [Phase 10 — Documentation & Polish](#14-phase-10--documentation--polish)
15. [Pain Points Remediation Map](#15-pain-points-remediation-map)
16. [NCAA Eval Learnings — Adoption Analysis](#16-ncaa-eval-learnings--adoption-analysis)
17. [Arxiv Paper Findings — Context File Effectiveness](#17-arxiv-paper-findings--context-file-effectiveness)
18. [Insights Report Findings — Real Usage Patterns](#18-insights-report-findings--real-usage-patterns)
19. [Decision Log](#19-decision-log)
20. [Learnings Captured](#20-learnings-captured)

---

## 1. Project Vision & Principles

### Vision

Build a production-grade Python cookiecutter repository that scaffolds a Claude Code-native agentic coding workflow capable of autonomous operation (overnight Ralph Wiggum loops), smart human interaction (knowing when to ask vs. proceed), rigorous anti-slop enforcement, and continuous self-improvement — all while being cruft-compatible for future template updates.

### Core Principles

- **Trust through verification, not hope.** Every output passes deterministic and stochastic quality gates before it reaches the human.
- **Human time is precious.** The system optimizes for high-leverage human interaction (ideation, judgment calls) and minimizes low-leverage review.
- **Fail gracefully, not silently.** When the agent can't proceed, it logs why, queues the blocker, and moves to the next viable task.
- **Learn explicitly.** Learnings are captured, debated with the human, and codified — not just pattern-matched implicitly.
- **Slop is the enemy.** Multiple independent checks (deterministic + stochastic) catch different failure modes. No single gate is trusted alone.
- **Minimal, surgical context files.** Per the ETH Zurich research (arxiv 2602.11988), CLAUDE.md and similar files should contain only non-obvious tooling and project-specific conventions — not comprehensive documentation. Linters/formatters enforce style deterministically; context files handle what tools can't.
- **Solve the specification bottleneck.** (Nate B. Jones) 97.5% of agent failures are specification failures, not model failures. The system exists to make specifications precise enough that autonomous execution is reliable.
- **Externalize tacit knowledge.** (Nate B. Jones) AI slop is what happens when unspoken expectations stay in humans' heads. Ubiquitous language, design requirements, and the learning store transform implicit knowledge into structures AI can work with.
- **Supervise, don't just prompt.** (Nate B. Jones) Agents introduce a supervision problem, not a prompting problem. The system provides version control, scoped tasks, persistent rules, and verification loops — not just better prompts.
- **The harness matters more than the model.** (Nate B. Jones) The same model scored 78% vs. 42% on identical benchmarks depending on the harness. This cookiecutter IS the harness — skills, hooks, permissions, memory, backlog, anti-slop gates. That's what determines output quality, not which model you run.
- **Solve the cognitive architecture problem.** (Nate B. Jones) The bottleneck moved from capability to how much you can concurrently think sensibly about. The system makes the human a better fleet commander by handling supervision infrastructure so they can focus on specification and taste.
- **Build the theory, instrument for reality.** Every design choice based on research ships with its full recommended structure from day one — don't plan to "add later" because later never comes. BUT treat every research-backed design as a hypothesis under active test. Each component ships with: (1) the structure the research recommends, (2) a retrospective prompt with pointed questions to detect failure, (3) clear criteria for what "broken" looks like, (4) a documented fallback if it doesn't work, capturing WHY so the next attempt is better-informed. This applies everywhere: the learning store, anti-slop rubric dimensions, process ordering, CLAUDE.md conventions, Mermaid style guide.
- **Human mental energy is the scarce resource, not time.** AI is cheap; human cognitive capacity is finite and non-renewable within a session. Every interaction with the human — prompts, documentation, architecture decisions, code review, UI — must minimize extraneous cognitive load. The cost of human input is not measured in minutes but in mental energy depleted. This flips several established SE principles: (1) "Working software over comprehensive documentation" flips to "Good documentation saves more mental energy than it costs to write — because AI writes it cheaply now." (2) "YAGNI" partially flips — upfront structure that reduces future cognitive load IS needed, even if not functionally required yet. (3) "Don't over-engineer" flips to "Don't under-design" — a refactor that dramatically reduces cognitive load should almost always be done, even if the current code works. (4) "Move fast and break things" flips to "Move thoughtfully and save brains." (5) "Premature optimization is the root of all evil" gets a sibling: "Premature COGNITIVE optimization is the root of all good." The system should actively surface epiphanies that reveal lower-extraneous-load approaches — through broader brainstorming in the plan phase, retrospective review, and learning store patterns.

---

## 2. Ubiquitous Language

> **Design philosophy:** Every repo generated from this cookiecutter ships with its own `UBIQUITOUS_LANGUAGE.md` and Matt Pocock's `ubiquitous-language` skill (installed via `npx skills@latest add mattpocock/skills/ubiquitous-language`). The skill extracts and formalizes domain terms from conversations — the glossary is the single source of truth for terminology in that project. The agent references it, uses it consistently, and flags when terms drift.
>
> Below is the Ubiquitous Language for *this project itself* (the cookiecutter system). Each derived repo will have its own, covering its own domain.

### Quality lifecycle

| Term | Definition | Aliases to avoid |
|------|-----------|-----------------|
| **Slop** | AI-generated output that is misaligned with the human's intent or is low-quality. | Hallucination (too narrow), bad code (too vague) |
| **Anti-Slop Gate** | A quality checkpoint that code must pass before reaching the human. | Filter, validator, check (too generic) |
| **Trust Tier** | A classification of an agent output that determines how much human review it requires. | Risk score (too narrow — it's about review routing, not just risk) |

### Agent execution

| Term | Definition | Aliases to avoid |
|------|-----------|-----------------|
| **Skill** | A self-contained capability the agent can invoke, defined as a structured prompt with validation criteria. | Tool (conflicts with Claude Code tool-use concept), command, script |
| **Ralph Wiggum Loop** | An autonomous execution loop where the agent iterates on a task until a completion promise is met or max iterations are reached. | Autonomous loop (too generic), retry loop (misses the convergence philosophy) |
| **Completion Promise** | The exact string the agent outputs to signal task completion in a Ralph Wiggum loop. | Done signal, exit code, success marker |
| **Agent Hook** | A lifecycle callback that fires at specific points in the agent's workflow. | Plugin (too broad), middleware |
| **Permission Boundary** | The set of tools and actions the agent is authorized to perform. | Allowlist (implementation detail, not the concept), permissions |

### Human-agent interaction

| Term | Definition | Aliases to avoid |
|------|-----------|-----------------|
| **Confidence Score** | The agent's self-assessed certainty that it understands what the human wants. | Certainty, probability, readiness |
| **Blocker** | A condition that prevents a task from proceeding, requiring human input or external resolution. | Issue (too vague), question (too narrow — could also be missing permission) |
| **Divergent Ideation** | A phase where agent and human explore possibilities broadly, expanding the solution space. | Brainstorming (implies unstructured; this is facilitated) |
| **Convergent Ideation** | A phase where agent and human narrow from options to decisions. | Decision-making (too generic — this is a specific phase transition) |
| **Grill-Me** | A skill where the agent aggressively interrogates the human's design decisions before writing code. | Code review (happens after code), Q&A (too passive) |

### Work management

| Term | Definition | Aliases to avoid |
|------|-----------|-----------------|
| **Backlog** | The prioritized queue of work items the agent draws from, with dependency and blocker tracking. | Todo list (no prioritization/dependency semantics), task list |
| **Design Requirement** | A human-specified behavior or constraint that must trace to at least one test. | Spec (too informal), AC (too BMAD-specific for general use) |
| **Learning** | A documented insight from agent operation, debated with the human and codified for future reference. | Note (too informal), memory (implies implicit rather than explicit) |

### Relationships

- A **Backlog** contains zero or more **Design Requirements**, each of which may have a **Blocker**.
- An **Anti-Slop Gate** evaluates the output of a **Skill** and assigns a **Trust Tier**.
- A **Ralph Wiggum Loop** executes one **Skill** at a time, checking **Confidence Score** before starting and running **Anti-Slop Gates** after completion.
- A **Learning** may modify how a **Skill** behaves or add a new **Anti-Slop Gate**.
- A **Grill-Me** session during **Divergent Ideation** produces **Design Requirements** during **Convergent Ideation**.

### Example dialogue

> **Human:** "I pushed a change but it broke something downstream."
> **Agent:** "I'll check the **Backlog** for related **Design Requirements**. It looks like this change touches a requirement with no test coverage — that's a gap in our **Anti-Slop Gates**. I have moderate **Confidence** I understand the fix, but I want to **grill you** on one thing first: was the downstream behavior an intentional **Design Requirement**, or just emergent behavior we never specified?"
> **Human:** "It was emergent — I never explicitly required it."
> **Agent:** "Then let's capture a new **Learning**: emergent behaviors that users depend on should be promoted to explicit **Design Requirements** with test coverage. I'll add it to the glossary and write the test. This is low-risk, so I'll classify it as a low **Trust Tier** — auto-merge OK?"

### Flagged ambiguities

- **"Task" vs "Skill" vs "Work item"**: A "task" is a unit of work in the **Backlog**. A "skill" is an agent capability. Don't use "task" to mean a skill invocation or vice versa. Claude Code's `Task` tool (for subagent spawning) adds a third meaning — always qualify: "backlog task," "agent skill," or "Task tool."
- **"Review"**: Could mean code review (anti-slop gate), human review (trust tier gate), or adversarial review (LLM-as-judge). Always specify which: "LLM code review," "human review gate," or "adversarial review."
- **"Test"**: Could mean unit test, integration test, or the act of testing an agent's output. When referring to test suites, use the 4-dimensional taxonomy (scope/approach/purpose/execution). When referring to agent output evaluation, say "anti-slop gate" or "LLM-as-judge."

---

## 3. Open Questions for Human

> Items the agent needs human input on before proceeding with affected work. When a question is answered, move it to the Decision Log.

| # | Question | Context | Blocking | Status |
|---|----------|---------|----------|--------|
| Q4 | **What's your confidence threshold intuition?** | At what confidence level should the agent stop and ask? Initial thought: 0.7 = proceed with caveats noted, below 0.7 = ask. Does that feel right? | Phase 5 design | 🔴 Open |
| Q5 | **What does the trust tier / review gating model need to look like?** | You said the simple risk-classification threshold "might not be ultimately where I want to end up" and it needs more fleshing out. What's your instinct on what's missing? Is it that some dimensions of risk matter more than others? Or that the model should be more nuanced than a single score? | Phase 5 design | 🔴 Open |
| Q9 | **Dependency management: Poetry, uv, or pip-tools?** | **RESOLVED → D76.** uv selected. | Phase 2 scaffold | ✅ Resolved |
| Q11 | **What's your preferred testing framework setup?** | **RESOLVED → D77.** pytest + pytest-cov always. hypothesis and mutmut as cookiecutter opt-in variables. nox excluded. | Phase 2 scaffold | ✅ Resolved |
| Q12 | **What is the optimal cognitive sequence from idea to working code?** | **RESOLVED — see below.** Unified process: Zoom-based progressive concretization. At each zoom level: identify questions → self-check ("can I answer from higher-level artifacts?") → resolve what you can → escalate ONLY genuine uncertainties as focused questions → verify consistency → zoom in. Human involvement is pull-based, not push-based: the agent works autonomously and pulls the human in only when it hits ambiguity the higher-level artifacts don't resolve. The quality of outer zoom levels determines how autonomous inner levels can be (P16.1 made operational). Documentation artifacts (advance organizer, ARCHITECTURE.md, ADRs) are produced as the TOOL for thinking at each level, not as afterthoughts. Same process for new repos and new features — just start at whatever zoom level has unresolved questions. | RESOLVED | ✅ Resolved |
| Q13 | **Visual information design science for Mermaid style guide** | Before writing the Mermaid style guide, research: (1) Pre-attentive visual attributes (what the brain processes before conscious attention — position, color hue, color intensity, size, orientation, shape, motion, enclosure). (2) Gestalt principles applied to diagrams (proximity, similarity, continuity, closure, figure-ground). (3) Colorblind-safe palette design (8% of men are red-green colorblind — avoid red/green as sole distinguisher). (4) Edward Tufte's principles (data-ink ratio, chartjunk minimization, small multiples). (5) Whether Mermaid supports additional sub-channels beyond what we've identified (icon embedding, subgraph grouping as enclosure, node size variation, text positioning). (6) Cognitive science on diagram comprehension — how many visual dimensions can be processed simultaneously before interference? Goal: produce a Mermaid style guide grounded in visual perception science, not just aesthetic preference. | Phase 2 (when writing style guide) | 🟡 Future Research |
| Q14 | **Validate model routing strategy (D72/D73) against real cost and quality data** | Current model routing is based on reasoning from principles. Need to validate with actual token costs and quality measurements once we're running real tasks. Key unknowns: (1) Where is the crossover point where Sonnet's lower cost outweighs its slightly lower plan quality? (2) Is Haiku actually reliable enough for narrow-scope review tasks? (3) How much does the confidence threshold filter matter for noise reduction? (4) Do model capabilities shift fast enough that this routing needs to be re-evaluated quarterly? | Phase 2+ (once running real tasks) | 🟡 Future Validation |

### Resolved Questions (moved to Decision Log)

| # | Original Question | Resolution | Decision # |
|---|-------------------|------------|------------|
| Q1 | Is "Ralph Wiggum Loop" the correct term/definition? | Yes — official Claude Code plugin. Stop hook intercepts exit, re-injects prompt. | D5 |
| Q2 | Is Claude Code the target agent runtime? | Yes, Claude Code specific. | D6 |
| Q3 | Where is the NCAA Eval repo learnings file? | Parsed. 4,450 lines, 288KB. See Section 16. | D7 |
| Q6 | Do you have specific sources you've found valuable? | Extensive list provided. See Phase 0 source list. | D8 |
| Q7 | What's your preferred project structure convention? | src layout, single package. | D9 |
| Q8 | Python version target? | 3.12+ | D10 |
| Q10 | BMAD: which aspects to keep? | Adopt story files, right-sizing, adversarial review. Discard heavy persona system. | D25 |

---

## 4. Phase 0 — Research & Best Practices Synthesis

**Goal:** Conduct extensive research across the agentic coding ecosystem, catalogue practices, evaluate reasoning quality, and produce a ranked synthesis document.

**Status:** 🟢 Complete

### Sources Researched

**Tier 1 (Deep Dive — 6 sources, 62+ practices):**
Matt Pocock, Boris Cherny (53 tips across 5 threads), Anthropic docs/blog (6 engineering posts), Andrej Karpathy, Nate B. Jones (27 podcast episodes), BMAD framework

**Tier 2 (Survey — 8+ sources, 26+ practices):**
Obra/Superpowers, Steve Yegge/Gas Town, SDD ecosystem (OpenSpec, Spec Kit), HumanLayer, YouTube tactical playlist (12 videos), Dan Shipper/Every (compound engineering), Boris Tane (annotation cycles), AGENTS.md, Geoffrey Huntley

**Academic Papers (10 papers):**
ACE (ICLR 2026), ACON, context-length-hurts, coding-agents-long-context, LLM-as-judge failures, LLM-as-judge survey, IoT-SkillsBench, OpenDev, trajectory-informed memory, self-improving coding agent

**Plugin Ecosystem:** 9K+ plugins, 101 official, feature-dev (89K installs), code-review (4 parallel agents)

**Code Quality & Cognitive Science:** SOLID/DRY/KISS, AI-specific code smells, Python typing/dataclasses/mypy, cognitive load theory (Miller, Sweller, Cowan), documentation/learning science (Ausubel, Bruner, Paivio), architectural principles (Pocock, Ousterhout)

**Skipped (sufficient coverage from other paths):**
Simon Willison, paddo.dev, Latent Space podcast, Practical AI podcast, Discord/Reddit communities, conference talks, newsletters, specific case studies

### Research Deliverables

| Deliverable | Description | Status |
|------------|-------------|--------|
| **Raw Catalogue** | 155+ practices across 34 categories. See `phase0-research-catalogue.md`. | ✅ Complete |
| **Category Taxonomy** | 34 categories → 7 themes. See `phase0-analysis.md`. | ✅ Complete |
| **Complement/Conflict Map** | 11 complement clusters + 8 tensions. See `phase0-analysis.md`. | ✅ Complete |
| **Reasoning Audit** | 3 tiers, zero unsound. See `phase0-analysis.md`. | ✅ Complete |
| **NCAA Eval Learnings** | Parsed. Adoption decisions integrated into decision log. | ✅ Complete |
| **Arxiv Analysis** | Key implications for CLAUDE.md strategy integrated. | ✅ Complete |
| **Insights Report Analysis** | Real friction data, hooks config, usage patterns integrated. | ✅ Complete |
| **Ideation Session** | Review findings with Dan, resolve open questions | 🟢 Complete — F1/F3 resolved, Q12 resolved (D74/D75) |
| **Phase 1 Design Inputs** | Synthesize decisions + open questions into actionable architecture inputs | ✅ Complete — see `phase1-design-inputs.md` |

### Research Process

1. ☑ Web research pass 1: Deep dives on all Tier 1 sources
2. ☑ Web research pass 2: Tier 2 sources survey
3. ☑ Web research pass 3: Academic papers, Anthropic blog, plugin ecosystem, new practitioners
4. ☑ Code quality + Python-specific + cognitive load + documentation/learning science research
5. ☑ Build raw catalogue (155+ practices, 34 categories)
6. ☑ Build category taxonomy (7 themes)
7. ☑ Identify complements and conflicts (11 clusters, 8 tensions)
8. ☑ Audit reasoning (3 tiers, 0 unsound)
9. ☑ Parse NCAA Eval learnings
10. ☑ Analyze arxiv papers and Anthropic engineering blog
11. ☑ Analyze Claude Code /insights report
12. ✅ Review synthesis with Dan — ideation session (F1/F3 resolved, Q12 resolved via D74/D75)
13. ✅ Synthesize into actionable design inputs for Phase 1 — see `phase1-design-inputs.md`

---

## 5. Phase 1 — Architecture & Design → Implementation

**Goal:** Build the cookiecutter template that generates a configured workspace per the Phase 0 research synthesis. See `phase1-design-inputs.md` for complete specifications.

**Status:** 🟡 Ready to Start — Phase 0 complete, design inputs synthesized

**Key reframing:** Phase 1 is NOT traditional architecture design. The architecture was decided in Phase 0 (75 decisions). Phase 1 is BUILDING the workspace template: writing markdown skill files, hook configs, TOML/JSON configuration, and documentation templates.

### Deliverables

| # | Deliverable | Description | Inputs |
|---|------------|-------------|--------|
| 1 | Cookiecutter template structure | File tree per design inputs Section 3 | D46, D67 |
| 2 | CLAUDE.md template | Minimal, surgical, ~50 lines per Section 4 | D11, D20, D51, D54, D55, D59, D65 |
| 3 | Hook configurations | PostToolUse (ruff+mypy), Stop, git guardrails per Section 5 | D14, D19, D23 |
| 4 | Planning skill | Zoom process with D75 self-check gate encoded as skill prompt | D74, D75, D49 |
| 5 | Review skill | Anti-slop rubric with 7 named dimensions per Section 6 | D50, D40, D45, D53, D60 |
| 6 | Compound skill | Learning codification with structured entry format per Section 7 | D47, D48, D68 |
| 7 | Plugin settings.json | Compose official plugins per Section 8 | D66, D45, D18 |
| 8 | Documentation templates | README, ARCHITECTURE.md, ADR, story file per Section 9-10 | D61, D62, D63, D64, D25, D44 |
| 9 | Learning store structure | docs/learnings/ with ACE-informed format per Section 7 | D21, D39, D68 |
| 10 | pyproject.toml | Full quality stack config per Section 12 | D56, D10 |
| 11 | CI workflow | GitHub Actions with deterministic gates | D50, D52, D56 |
| 12 | Retrospective prompts | D69 instrumentation for each component | D69 |
| 13 | Mermaid style guide | Visual encoding conventions (pending Q13 research) | D63, Q13 |

### Open Decisions to Resolve in Phase 1

All previously open items have been resolved:

| Decision | Resolution |
|----------|-----------|
| Q9: Dependency management | ✅ uv (D76) |
| Q11: Testing stack | ✅ pytest+cov always; hypothesis, mutmut opt-in (D77) |
| D24a: Ralph plugin vs bash | ✅ Official plugin first (D78) |
| D24b: Task backlog format | ✅ Local story files (D79) |
| D37/D41: Context rotation | ✅ Externalize state, default to compaction, test rotation as fallback (D80) |

---

## 6. Phase 2 — Cookiecutter Scaffold

**Goal:** Build the cookiecutter template structure with cruft compatibility, dev tooling, and project conventions.

**Status:** 🔴 Not Started — Blocked on Phase 1

### Scaffold Components

| Component | Description | Status |
|-----------|-------------|--------|
| cookiecutter.json | Template variables (project name, Python version, etc.) | Not Started |
| Cruft compatibility | .cruft.json, template update workflow | Not Started |
| pyproject.toml | Project metadata, dependencies, tool configs (Python 3.12+) | Not Started |
| src layout | `src/{{cookiecutter.package_name}}/` single-package structure | Not Started |
| .claude/ directory | `settings.json` (permissions + hooks), `CLAUDE.md` (minimal per arxiv findings) | Not Started |
| .claude/ hooks | PostToolUse: auto-run ruff after Edit/Write (per insights — eliminates #1 friction) | Not Started |
| .claudeignore | Exclude irrelevant files from Claude's context | Not Started |
| Dev tooling: mypy | Strict type checking config (per NCAA eval learnings) | Not Started |
| Dev tooling: pytest | Test framework with fixtures, markers, coverage config | Not Started |
| Dev tooling: ruff | Linting and formatting (explicit rule codes, not prefixes) | Not Started |
| Dev tooling: pre-commit | Local mypy hook pattern (not mirrors-mypy — per NCAA eval) | Not Started |
| Dev tooling: nox | Session management with `python=False` for Poetry/conda compat | Not Started |
| CI/CD: GitHub Actions | Workflows for testing, linting, type checking | Not Started |
| PR template | Enforced checklist that agent cannot skip | Not Started |
| Issue templates | Structured task definitions | Not Started |
| UBIQUITOUS_LANGUAGE.md | Empty DDD-style glossary template (Matt Pocock format: grouped terms, aliases to avoid, relationships, example dialogue, flagged ambiguities) | Not Started |
| .claude/skills/ubiquitous-language/ | Matt Pocock's skill — installed via `npx skills@latest add mattpocock/skills/ubiquitous-language` | Not Started |
| cookie-cutter-improvements.md | Empty file for learnings from derived projects (per NCAA eval) | Not Started |
| TESTING_STRATEGY.md | Hub-and-spoke testing documentation (per NCAA eval) | Not Started |

### Key NCAA Eval Patterns to Adopt in Scaffold

- Local mypy hook (NOT mirrors-mypy) for src-layout projects
- Both `[tool.coverage.run]` AND `[tool.coverage.report]` in pyproject.toml from day one
- Explicit Ruff rule codes (not PLR09 prefix wildcards)
- Marker-based test exclusion (not `-k` name matching)
- `pre-commit install` documented as required post-clone step
- Pin GitHub Actions to specific version tags, never `@master`
- Nox sessions with `python=False` when using Poetry/conda
- Google-style docstrings enforced via ruff pydocstyle convention
- 4-dimensional testing model: Scope × Approach × Purpose × Execution
- Test marker taxonomy with strict discipline (every test gets a marker)

---

## 7. Phase 3 — Core Agent System

**Goal:** Implement the core agent loop, skill registry, and permission boundary system.

**Status:** 🔴 Not Started — Blocked on Phase 1, Phase 2

### Sub-Components

#### 3A. Agent Core Loop

| Step | Description | Status |
|------|-------------|--------|
| State machine definition | Define agent states: idle, planning, executing, evaluating, blocked, waiting-for-human | Not Started |
| Task intake | How the agent picks up work from the backlog | Not Started |
| Execution cycle | Single iteration of plan→execute→evaluate | Not Started |
| Transition logic | Rules for moving between states | Not Started |
| Error handling | Graceful failure, logging, blocker creation | Not Started |

#### 3B. Skill Registry

| Step | Description | Status |
|------|-------------|--------|
| Skill definition format | Claude Code slash commands / agent files / YAML definitions | Not Started |
| Skill discovery | Auto-discovery from skills/ directory | Not Started |
| Skill versioning | Track skill versions, allow rollback | Not Started |
| Skill invocation | Standard interface for calling skills | Not Started |

#### 3C. Permission Boundary Checker

| Step | Description | Status |
|------|-------------|--------|
| Permission config | Parse `.claude/settings.json` allowlists | Not Started |
| Pre-flight check | Before every tool call, verify permission exists | Not Started |
| Alternative tool finder | When denied, search for permitted alternatives that accomplish the same thing | Not Started |
| Exhaustion handling | When no permitted alternative exists, create blocker and move on | Not Started |
| Logging | All permission checks logged for audit | Not Started |

### Skill Inventory (Initial)

| Skill | Description | Priority | Status |
|-------|-------------|----------|--------|
| **grill-me** | Interrogate human's design decisions before coding (Matt Pocock) | 🔴 Critical | Not Started |
| **write-code** | Generate code following project conventions and design requirements | 🔴 Critical | Not Started |
| **write-tests** | Generate tests aligned with design requirements (bidirectional traceability) | 🔴 Critical | Not Started |
| **write-pr** | Generate PR following template, with checklist enforcement | 🔴 Critical | Not Started |
| **review-code** | LLM-as-judge code review against quality criteria | 🔴 Critical | Not Started |
| **document-learning** | Capture, debate, and codify learnings | 🔴 Critical | Not Started |
| **assess-confidence** | Evaluate agent's understanding of human intent | 🔴 Critical | Not Started |
| **classify-trust-tier** | Score a PR/output for review requirements | 🔴 Critical | Not Started |
| **check-permissions** | Pre-flight permission check before tool calls | 🔴 Critical | Not Started |
| **manage-backlog** | Prioritize, re-sequence, identify unblocked work | 🟡 High | Not Started |
| **research** | Search and synthesize information from external sources | 🟡 High | Not Started |
| **refactor** | Improve existing code while preserving behavior | 🟡 High | Not Started |
| **ubiquitous-language** | Matt Pocock's skill (use directly, don't fork). Extracts DDD-style glossary from conversation, flags ambiguities, writes UBIQUITOUS_LANGUAGE.md. Install: `npx skills@latest add mattpocock/skills/ubiquitous-language` | 🟡 High | Not Started |
| **diagnose-failure** | Analyze test failures, runtime errors, CI failures | 🟡 High | Not Started |
| **ideation-facilitate** | Guide divergent/convergent ideation sessions with human | 🟡 High | Not Started |

---

## 8. Phase 4 — Anti-Slop Pipeline

**Goal:** Implement multi-layer quality gates that catch slop before it reaches the human.

**Status:** 🔴 Not Started — Blocked on Phase 3

### Deterministic Gates

| Gate | What It Catches | Implementation | Status |
|------|----------------|----------------|--------|
| **Type checking (mypy)** | Type errors, missing annotations, unsafe casts | mypy --strict | Not Started |
| **Linting (ruff)** | Style violations, unused imports, code smells | ruff check + ruff format | Not Started |
| **Test suite (pytest)** | Functional regressions, logic errors | Full test suite with coverage | Not Started |
| **PR template compliance** | Skipped checklist items, missing sections | Deterministic parse of PR body | Not Started |
| **Design req traceability** | Tests ↔ requirements gaps | Cross-reference markers | Not Started |
| **Permission boundary** | Tool calls outside allowed set | Pre-flight check | Not Started |
| **Import/dependency check** | Undeclared imports | AST scan vs. pyproject.toml | Not Started |
| **Diff size check** | Overly large PRs | Line count thresholds | Not Started |
| **Marker discipline** | Unmarked tests | Scan for missing markers | Not Started |

### Stochastic Gates (LLM-as-Judge)

| Gate | What It Catches | Evaluation Criteria | Status |
|------|----------------|---------------------|--------|
| **Code quality review** | Slop patterns: unnecessary abstractions, boilerplate | Rubric scoring against conventions | Not Started |
| **Requirement alignment** | Code that works but misses intent | Compare behavior vs. stated requirements | Not Started |
| **Test quality review** | Over-constraining, testing implementation not behavior | Check against design requirements | Not Started |
| **PR narrative review** | PR description doesn't match changes | Compare diff vs. PR description | Not Started |
| **Future flexibility** | Unnecessarily restrictive code | Evaluate against known upcoming reqs | Not Started |

### Pipeline Flow

```
Code Generated → Lint → Type Check → Tests → Traceability → PR Template
    → LLM Code Review → LLM Requirement Alignment
    → Trust Tier Classification → [Auto-merge | Review Queue | Human Required]
```

---

## 9. Phase 5 — Human Interaction Layer

**Goal:** Build the system for smart human interaction — knowing when to ask, facilitating ideation, and managing the human's attention budget.

**Status:** 🔴 Not Started — Blocked on Phase 3

### Sub-Components

#### 5A. Confidence-Based Gating (Blocked on Q4)

#### 5B. Ideation Facilitation

| Step | Description | Status |
|------|-------------|--------|
| Divergent mode | Generate options, ask "what if," expand space | Not Started |
| Convergent mode | Evaluate tradeoffs, drive toward decisions | Not Started |
| Mode detection | Recognize which mode is appropriate | Not Started |
| Half-baked input handling | Work with incomplete thoughts, ask targeted questions | Not Started |
| Grill-me integration | Aggressive design interrogation before coding | Not Started |

#### 5C. Trust Tier System (Blocked on Q5)

#### 5D. Blocker Management & Async Communication

| Step | Description | Status |
|------|-------------|--------|
| Blocker creation | Structured: what's blocked and why | Not Started |
| Question batching | Group related questions for human | Not Started |
| Smart pivot | When blocked, find next unblocked task | Not Started |
| Completion reporting | Overnight run summary | Not Started |

---

## 10. Phase 6 — Autonomous Loop Engine (Ralph Wiggum)

**Goal:** Implement Ralph Wiggum-based autonomous loops for overnight backlog processing.

**Status:** 🔴 Not Started — Blocked on Phases 3, 4, 5

### Ralph Wiggum Integration Notes

- Install: `/plugin marketplace add anthropics/claude-code` then `/plugin install ralph-wiggum@claude-plugins-official`
- Run: `/ralph-loop "prompt" --max-iterations N --completion-promise "TOKEN"`
- Stop hook intercepts exit, re-injects prompt
- `--max-iterations` = PRIMARY safety mechanism
- `--completion-promise` = exact string matching only (fragile — not a safety mechanism)
- Known issues: session bleed across terminals, Docker compat, jq dependency on Windows
- Cost: 50 iterations on medium codebase ≈ $50-100+ API credits

### Good For vs. Not Good For

**Good:** Well-defined tasks with objective success criteria, iterative refinement, batch mechanical work, multi-phase overnight chains.

**Not good:** Ambiguous requirements, architectural decisions, security-critical code, exploratory work.

### Our Wrapping Architecture

```
Human: "goodnight, work on these"
  → Backlog Manager: select highest-priority unblocked task
  → Confidence Scorer: can we proceed without human?
    → Below threshold: create blocker, pivot to next task
    → Above threshold: construct Ralph Wiggum prompt
  → /ralph-loop with constructed prompt
    → DONE: run anti-slop pipeline → trust tier → merge/queue
    → BLOCKED: parse blocker, add to human queue, pivot
    → Max iterations: document attempts, create blocker
  → More unblocked tasks + budget remaining? Loop back.
  → Done: generate completion report for human
```

### Safety Rails

| Rail | Purpose | Default |
|------|---------|---------|
| Max iterations per task | Prevent infinite single-task loops | 20-30 |
| Max tasks per night | Overall cost/risk cap | Configurable |
| Error rate circuit breaker | Stop on consecutive failures | 3 consecutive |
| Cost monitoring | Track API spend | Configurable alerts |
| No `--dangerously-skip-permissions` | Always respect permission boundaries | Hard rule |

---

## 11. Phase 7 — Learning & Adaptation System

**Goal:** Capture, debate, codify, and apply learnings over time.

**Status:** 🔴 Not Started — Blocked on Phase 3

### Learning Storage Format (Draft)

```yaml
learning_id: L001
date_captured: 2026-03-25
category: testing
title: "Tests should verify behavior, not implementation"
observation: |
  Agent wrote tests asserting internal method calls that broke on refactor.
root_cause: |
  Test generation optimized for coverage % rather than behavioral verification.
behavior_change: |
  Frame assertions in terms of observable outputs/side effects, never internals.
confidence: 0.9
validated_by: human
related_learnings: []
```

### Key Features

- Learning detection (agent recognizes potential learnings)
- Human debate protocol (back-and-forth to refine)
- Codification into structured store
- Application in future decisions
- `cookie-cutter-improvements.md` for upstream feedback (per NCAA eval)
- Conflict resolution when new learnings contradict existing ones

---

## 12. Phase 8 — Dev Tooling & CI/CD

**Goal:** Configure all dev tooling and CI/CD in the cookiecutter template.

**Status:** 🔴 Not Started — Blocked on Phase 2

### Tooling (see Phase 2 for full list)

Key NCAA eval-informed configurations: mypy strict + local hook, both coverage sections, explicit ruff codes, nox with `python=False`, pre-commit with current stage names, pinned GitHub Actions versions, CI Python matching pyproject.toml.

---

## 13. Phase 9 — Integration Testing & Validation

**Goal:** Verify end-to-end. Address "passes tests but fails in practice" pain point.

**Status:** 🔴 Not Started — Blocked on Phases 3–8

### Test Levels

Unit → Integration → End-to-end → Scenario (pain points) → E2E documented commands (NCAA eval pattern) → User acceptance (Dan runs it)

---

## 14. Phase 10 — Documentation & Polish

**Goal:** Complete docs following minimal/surgical CLAUDE.md strategy + hub-and-spoke documentation.

**Status:** 🔴 Not Started

### Deliverables

README.md, ARCHITECTURE.md, SKILLS.md, LEARNINGS.md, CONTRIBUTING.md, WORKFLOW.md, CLAUDE.md (minimal), UBIQUITOUS_LANGUAGE.md (Matt Pocock DDD-style template)

---

## 15. Pain Points Remediation Map

| Pain Point | Remediation | Phase |
|-----------|-------------|-------|
| **Agent uses unpermitted tools** | Permission Boundary Checker: pre-flight → alternative finder → blocker | 3C |
| **Agent skips PR checklist** | Deterministic PR template compliance gate; write-pr skill | 4 |
| **Code passes tests but fails in practice** | E2E documented command tests; requirement traceability; scenario tests | 4, 9 |
| **Hard to decide when to review** | Trust Tier Classifier (model TBD — Q5). Insights data suggests friction is in tooling, not logic — may justify higher auto-merge threshold. | 5C |
| **Trust fatigue → over-trusting** | Trust tiers + auto-merge for low-risk | 5C |
| **Small PRs block overnight progress** | Ralph Wiggum loop + trust tiers: auto-merge trivial PRs, chain multiple | 5C, 6 |
| **Test coverage ↔ requirements misaligned** | Bidirectional traceability; marker discipline; LLM test quality review | 4 |
| **Tests over-constrain future code** | "Test behavior not implementation" learning; test quality gate | 4, 7 |
| **Requirements lack test coverage** | Traceability: every requirement → test; every public method → test ID at planning | 4 |
| **Ruff formatting breaks commits** *(from insights)* | PostToolUse hook auto-runs ruff after Edit/Write; pre-commit gate | 2, 8 |
| **Invalid commitizen commit types** *(from insights)* | CLAUDE.md explicit allowlist; pre-commit hook validates message format | 2, 8 |
| **Test fixtures drift from code changes** *(from insights)* | Anti-slop gate checks fixture/constant sync; skill directive for atomic updates | 4 |
| **Agent breaks persona boundaries** *(from insights)* | Skill definitions include explicit persona constraints and "do NOT" rules | 3B |
| **Wrong first approach / misdiagnosis** *(from insights)* | Confidence scoring before acting; structured diagnosis protocol in skills | 5A |

---

## 16. NCAA Eval Learnings — Adoption Analysis

> Parsed from: `template-requirements.md` — 4,450 lines, 288KB

### High-Confidence Adoptions

| Learning | Category | Why Adopt |
|----------|----------|-----------|
| Local mypy hook (not mirrors-mypy) for src-layout | Dev Tooling | mirrors-mypy can't type-check local package imports |
| Both `coverage.run` + `coverage.report` in pyproject.toml | Testing | Omitting `coverage.run` silently disables branch coverage |
| Explicit Ruff rule codes (not prefix wildcards) | Dev Tooling | PLR09 prefix over-selects rules with undocumented defaults |
| Marker-based test exclusion (not `-k`) | Testing | Name-based exclusion breaks silently on rename |
| Nox `python=False` for Poetry/conda | Dev Tooling | Avoids duplicating dependency tree per session |
| Pin GitHub Actions to version tags | CI/CD | Supply chain security |
| CI Python must match pyproject.toml | CI/CD | Mismatched versions cause subtle breakage |
| 4-dimensional testing model | Testing | Orthogonal dimensions improve test selection clarity |
| Hub-and-spoke documentation | Docs | 1 main + focused guides > monolithic doc |
| Visual-first docs (Mermaid) | Docs | Pictures > Words |
| Every test gets a marker | Testing | Unmarked tests silently excluded from targeted runs |
| Test behavior, not implementation | Testing | Core anti-slop principle; addresses Dan's pain point |
| `cookie-cutter-improvements.md` feedback loop | Process | Enables derived projects to contribute upstream |
| No codespell, no blacken-docs | Dev Tooling | Both cause more damage than they prevent |
| `pre-commit install` required post-clone | Dev Tooling | Without it, hooks silently inactive |
| Session-scoped fixtures for expensive ops | Testing | Better than globals with `noqa: PLW0603` |
| Library-first before reimplementing | Process | Check for existing packages before writing custom code |
| Every public method → at least one test | Testing | Bugs concentrate in untested methods |
| Spike stories need human decision gate | Process | Prevents agent from committing scope decisions unilaterally |
| Pre-commit current stage names | Dev Tooling | `pre-commit` not `commit`, `pre-push` not `push` |

### Conditional Adoptions

| Learning | Condition |
|----------|-----------|
| Poetry-specific patterns | Only if Poetry chosen (Q9) |
| Commitizen + branch protection | If using commitizen |
| Sphinx + Furo + myst-parser | Depends on docs tooling choice |
| Mutmut patterns | If mutation testing included (requires WSL) |

---

## 17. Arxiv Paper Findings — Context File Effectiveness

> Source: arxiv 2602.11988 (Feb 2026, ETH Zurich)
> "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"

### Key Findings

1. **LLM-generated context files REDUCE task success** by ~3%
2. **Human-written files only marginally help** (+4%)
3. **Both types increase inference cost 20%+**
4. **Stronger models don't generate better context files**
5. **Tool instructions have massive multiplier** (uv mentioned → used 160x more)
6. **Comprehensive documentation = noise** that makes tasks harder

### Our CLAUDE.md Strategy (Based on Findings)

**INCLUDE:** Non-obvious tooling ("use `nox`", "use `ruff`"), project conventions tools can't enforce, ubiquitous language reference, permission boundaries, known footguns, valid commitizen commit types (per insights: feat, fix, docs, style, refactor, perf, test, build, ci, chore — never 'review'), atomic test fixture update rule, "Be extremely concise. Sacrifice grammar for the sake of concision." (Matt Pocock), reference to learnings file

**EXCLUDE:** Project overview (agent reads README), directory structure (agent can `ls`), style guide (ruff/mypy enforce), dependency list (pyproject.toml), general best practices (agent knows)

**Glossary approach:** Separate `UBIQUITOUS_LANGUAGE.md` file maintained via Matt Pocock's `ubiquitous-language` skill, referenced by one line in CLAUDE.md — keeps CLAUDE.md minimal while making terminology available.

---

## 18. Insights Report Findings — Real Usage Patterns

> Source: Claude Code `/insights` report — 448 messages across 189 sessions, Feb 22 – Mar 14, 2026
> 251 commits, 41 hours, +48,776/-5,007 lines across 990 files

### Dan's Observed Usage Pattern

The insights report reveals Dan as a **"workflow architect"** — he triggers structured automated pipelines and lets Claude execute entire development cycles autonomously with minimal mid-session guidance. Key stats:

- **2.4 messages per session** — Dan fires a workflow, Claude executes, done
- **86% fully achieved** rate (43/50 analyzed sessions)
- **711 TodoWrite invocations** — heavy use of structured task tracking
- **Multi-file changes** succeeded in 41/50 sessions
- **Nearly zero multi-clauding** (1 overlap event) — sequential, not parallel yet
- **Evening-heavy usage** (183 evening messages vs. 130 morning) — aligns with "work overnight" goal

### What's Already Working (Preserve These Patterns)

| Pattern | Evidence | Implication for New System |
|---------|----------|---------------------------|
| End-to-end automated SDLC pipeline | create-story → implement (TDD) → adversarial code review → PR, all in YOLO mode | Our skill-based architecture should replicate this pipeline but with anti-slop gates between stages |
| TodoWrite-driven task execution | 711 calls — Claude stays on rails during complex multi-file workflows | Backlog manager should leverage similar structured task tracking |
| Autonomous code review with auto-fix | Sessions find 5-10 issues, auto-fix, run tests, open PRs | review-code skill should preserve this pattern; add test-generation for review findings |
| Single-task session dominance | 46 single-task vs. 3 multi-task sessions | Confirms the "one task per Ralph Wiggum loop iteration" architecture |

### Friction Points (These MUST Be Solved by the New System)

| Friction | Frequency | Root Cause | Remediation in Our System |
|----------|-----------|-----------|---------------------------|
| **Ruff formatting/linting breaks commits** | 4+ sessions | Claude edits code then commits without running linters | **PostToolUse hook**: auto-run `ruff check --fix && ruff format` after every Edit/Write tool call. Also: deterministic pre-commit gate in anti-slop pipeline. |
| **Invalid commitizen commit types** | 2+ sessions (used 'review' which doesn't exist) | Claude doesn't know allowed commit types | **CLAUDE.md directive**: explicit allowlist of valid types (feat, fix, docs, style, refactor, perf, test, build, ci, chore). Also: pre-commit hook validates commit message format. |
| **Test fixtures drift from code changes** | 2+ sessions | Test helpers generate data for 2025 but constant updated to 2026 | **Anti-slop gate**: test quality review specifically checks for fixture/constant synchronization. **Skill directive**: "update test fixtures atomically with code changes." |
| **Initial misdiagnosis / wrong first approach** | 4 sessions | Claude assumes wrong root cause or breaks persona | **Confidence scoring**: before acting, assess confidence that the diagnosis is correct. **Persona enforcement**: skill definitions include persona boundaries with explicit "do NOT" rules. |
| **Agent breaks persona** (SM writes code) | 1 notable session | No guardrail preventing role drift | **Skill-level persona enforcement**: each skill defines what it IS and IS NOT allowed to do. Stop hook could check for role boundary violations. |

### Hooks Configuration (From Insights Recommendations)

The insights report specifically recommended this PostToolUse hook configuration — directly applicable to our cookiecutter:

```json
// .claude/settings.json
{
  "hooks": {
    "post_tool_use": [
      {
        "matcher": "Edit|Write",
        "command": "ruff check --fix $CLAUDE_FILE_PATH && ruff format $CLAUDE_FILE_PATH"
      }
    ]
  }
}
```

This alone would eliminate the #1 friction source (4+ sessions of wasted retries).

### Horizon Items (Align with Our Architecture)

The insights report identified three "on the horizon" capabilities that map directly to our system:

| Horizon Item | Insights Framing | Our System's Answer |
|-------------|-----------------|---------------------|
| **Parallel agent story execution** | Spawn parallel Claude Code agents for independent stories | Backlog manager identifies non-conflicting tasks; Ralph Wiggum loop executes them sequentially (parallel is future enhancement) |
| **Self-healing CI with fix loops** | Watch CI output, diagnose failures, auto-fix, re-commit | Anti-slop pipeline + Ralph Wiggum iteration = this is our core architecture |
| **Adversarial review with test generation** | Write failing tests for review findings BEFORE fixing | Directly maps to our write-tests + review-code skill interaction pattern |

### Key Insight for Trust Tier Design (Q5)

The insights data suggests a trust tier model should consider **session outcome history**. With 86% fully achieved and the friction concentrated in tooling issues (not logic errors), Dan's system may actually justify a higher auto-merge threshold than expected — the problems aren't in the code logic, they're in the commit/lint hygiene that our hooks and gates will fix. This is relevant to the Q5 discussion about what the trust tier model should look like.

---

## 19. Decision Log

| # | Decision | Rationale | Date |
|---|----------|-----------|------|
| D1 | Rubric-based quality scoring for LLM-as-judge | Binary loses nuance; rubrics allow tuning | 2026-03-25 |
| D2 | Learnings debated with human before codification | Prevents learning wrong lesson | 2026-03-25 |
| D3 | Research ranked by reasoning soundness, not frequency | Popular ≠ correct | 2026-03-25 |
| D4 | Cruft-compatible cookiecutter | Enables pulling future template improvements | 2026-03-25 |
| D5 | Ralph Wiggum = official Claude Code plugin (Stop hook) | Confirmed via link to official plugin | 2026-03-25 |
| D6 | Claude Code is the target runtime | Confirmed by Dan | 2026-03-25 |
| D7 | NCAA Eval learnings parsed | 4,450 lines, 288KB. See Section 16. | 2026-03-25 |
| D8 | Priority source list seeded | 22+ named sources. See Phase 0. | 2026-03-25 |
| D9 | src layout, single package | Confirmed by Dan | 2026-03-25 |
| D10 | Python 3.12+ | Confirmed by Dan | 2026-03-25 |
| D11 | CLAUDE.md: minimal and surgical | Per arxiv 2602.11988. Non-obvious tooling only. | 2026-03-25 |
| D12 | Use .claudeignore | Manage context window, prevent pollution | 2026-03-25 |
| D13 | No `--dangerously-skip-permissions` | Hard rule. Permission checker handles gracefully. | 2026-03-25 |
| D14 | PostToolUse hook for ruff after Edit/Write | Per insights report — eliminates #1 friction source | 2026-03-25 |
| D15 | Valid commitizen types in CLAUDE.md | Per insights report — prevents invalid commit type retries | 2026-03-25 |
| D16 | Test fixtures updated atomically with code changes | Per insights report — prevents fixture drift | 2026-03-25 |
| D17 | Use Matt Pocock's `ubiquitous-language` skill directly | Don't fork or rename — use upstream, get updates. Each derived repo gets UBIQUITOUS_LANGUAGE.md + the skill installed. | 2026-03-25 |
| D18 | Install Matt Pocock's `grill-me`, `git-guardrails-claude-code`, `tdd`, `write-a-prd`, `write-a-skill` directly | Core skills for ideation, safety, testing, planning, meta-skill creation. Evaluate `prd-to-plan`, `prd-to-issues`, `triage-issue`, `improve-codebase-architecture` for fit. | 2026-03-25 |
| D19 | Never commit directly to main | Hard rule. Agent always works on feature branches. PRs are the integration mechanism. Enforced by git guardrails hook. Matt Pocock's Ralph-to-main approach explicitly rejected. | 2026-03-25 |
| D20 | "Be extremely concise. Sacrifice grammar for concision." in CLAUDE.md | Matt Pocock's viral directive. Makes plans scannable, reduces cost, paradoxically increases information density. | 2026-03-25 |
| D21 | Store learnings in a separate file, not CLAUDE.md | Boris Cherny advocates updating CLAUDE.md on errors, but arxiv says keep CLAUDE.md minimal. Resolution: learnings in separate file, CLAUDE.md references it with one line. | 2026-03-25 |
| D22 | Use /permissions + .claude/settings.json for permission management (Boris Cherny pattern) | Pre-allow safe commands, share via settings.json with team. Don't use --dangerously-skip-permissions. This is the implementation of D13. | 2026-03-25 |
| D23 | Stop hook for end-of-turn verification | Boris Cherny: use Stop hook to verify work before allowing exit. "Give Claude a way to verify = 2-3x quality." | 2026-03-25 |
| D24 | Ralph vs bash loop and GitHub Issues vs local backlog deferred to Phase 1 | Not enough info to decide now. Both are architecture decisions that depend on choices we haven't made yet. | 2026-03-25 |
| D25 | Adopt BMAD story files as handoff mechanism; discard heavy persona system | Story files work (proven in NCAA eval). Personas add token overhead and break (insights report). Use skills with clear instructions instead. | 2026-03-25 |
| D26 | Right-size execution to task complexity | Not every task needs a full Ralph loop. Karpathy's multi-layer approach: simple fix → single `claude -p`, medium task → plan+execute, complex feature → full grill-me → PRD → loop pipeline. | 2026-03-25 |
| D27 | Learnings that recur 3+ times should become deterministic gates | Boris Cherny's Meta practice: recurring review comments → lint rules. Our learning system should feed back into the anti-slop pipeline as new automated checks. | 2026-03-25 |
| D28 | Anti-slop rubrics must include failure examples, not just success criteria | Nate B. Jones: "Teach AI with examples of failure, not just success." Rubrics need anti-patterns alongside patterns. | 2026-03-25 |
| D29 | Core principle: "The system exists to make specifications precise enough that autonomous execution is reliable" | Nate B. Jones: 97.5% of agent failures are specification failures, not model failures. The specification bottleneck is the real constraint. | 2026-03-25 |
| D30 | Core principle: "Externalize tacit knowledge into structures AI can work with" | Nate B. Jones: AI slop is what happens when tacit expectations stay in humans' heads. UBIQUITOUS_LANGUAGE.md, design requirements, learning store = externalized tacit knowledge. | 2026-03-25 |
| D31 | Core principle: "The harness matters more than the model" | Nate B. Jones: Same model, 78% vs 42%. The cookiecutter IS the harness. Skills, hooks, permissions, memory, backlog, anti-slop gates determine quality, not the model. | 2026-03-25 |
| D32 | Trust tiers route human attention to high-value review, not eliminate review | Nate B. Jones: 10x productivity means expanding ambition, not cutting headcount. Auto-merge trivial PRs so human time goes to architecture decisions. | 2026-03-25 |
| D33 | Learning store must be a shared surface readable by both human and agent | Nate B. Jones (Open Brain): Memory as shared surface, not hidden database. Markdown files satisfy this — both Dan and the agent can read/write them. | 2026-03-25 |
| D34 | Implement two-stage review in anti-slop pipeline (spec compliance, then code quality) | Obra/Superpowers: Single-pass review conflates two failure modes. Code can match spec but be poorly written, or be well-written but not match spec. Separate checks improve catch rate. | 2026-03-26 |
| D35 | Adopt "land the plane" pattern — end-of-session state cleanup and handoff | Steve Yegge/Gas Town: At the end of each session/iteration, agent summarizes what it did, what's left, and generates a ready-to-resume prompt. Prevents the "50 First Dates" problem. | 2026-03-26 |
| D36 | Build AutoResearch capability into the cookiecutter — skills should have eval files | Karpathy AutoResearch: Skills fail ~30% of the time silently. Binary eval criteria + overnight optimization loops took skills from 41% → 92%. Every skill should ship with an eval file. This is the compounding mechanism. | 2026-03-26 |
| D37 | Build context rotation into Ralph loop design | Context rot accelerates after ~65% fill. Ralph loops must either auto-rotate context at a threshold or /clear between iterations with structured handoff. A clean 160K budget beats a polluted 80K budget. | 2026-03-26 |
| D38 | Include git worktree setup in cookiecutter | Claude Code's --worktree flag enables true parallel development. Standard practice for Agent Teams and parallel execution. | 2026-03-26 |
| D39 | Learning store entries must be structured bullets with usage metadata (ID, helpful/harmful counters) | ACE paper (arxiv 2510.04618, ICLR 2026): Itemized bullets with metadata prevent context collapse and brevity bias. +10.6% on agent benchmarks. Append-only deltas, never monolithic rewrites. | 2026-03-26 |
| D40 | Anti-slop rubrics decompose quality into named dimensions with specific criteria per dimension | Anthropic March 2026 harness blog: GAN-inspired generator/evaluator. "Is this good?" doesn't work — decompose into design quality, originality, craft, fidelity (or equivalent dimensions for code). | 2026-03-26 |
| D41 | Evaluate whether Opus 4.6 + SDK compaction eliminates need for manual context rotation (D37) | Anthropic March 2026: Context resets no longer needed with Opus 4.6. May modify D37. Test before committing to manual rotation. | 2026-03-26 |
| D42 | Treat compaction prompts as optimizable targets (like skills via AutoResearch) | ACON paper (arxiv 2510.00615): Failure-driven compression optimization. When compaction causes issues, update the compaction prompt to preserve that class of information. 26-54% token reduction while preserving accuracy. | 2026-03-26 |
| D43 | Academic validation: context length alone hurts performance even with perfect retrieval | arxiv 2510.05381: Even 100% exact-match retrieval degrades as length increases. Strongest justification for minimal CLAUDE.md (D11). Every unnecessary token actively degrades output quality. | 2026-03-26 |
| D44 | Story files must include failing-to-passing feature checklists | Anthropic harness blog: Initializer writes 200+ features marked "failing." Agent turns them "passing." Prevents premature completion. | 2026-03-26 |
| D45 | Use Anthropic's official code-review plugin as baseline, customize with our anti-slop rubric | Don't reinvent: 4 parallel agents with confidence scoring already built. Customize the review prompt with our quality dimensions. | 2026-03-26 |
| D46 | Cookiecutter = composition + configuration + learning system, NOT component builder | Plugin ecosystem (9K+ plugins, 101 official) is mature. Cookiecutter's value is the workflow, settings.json, CLAUDE.md template, skill templates with eval files, and hook configs — not rebuilding plugin functionality. | 2026-03-26 |
| D47 | Default workflow is Plan → Work → Assess → Compound (simplified mental model of D74) | Every.to: "80% of compound engineering is plan and review, 20% is work." This is the SIMPLIFIED SHORTHAND for D74's zoom-based process: "Plan" = outer zoom levels (purpose, structure, contracts). "Work" = implementation zoom. "Assess" = verify consistency + quality gates. "Compound" = zoom all the way out, verify docs, codify learnings. D47 is how you explain the workflow in one sentence. D74 is how it actually operates. | 2026-03-26 |
| D48 | Learning entries include type (strategy/recovery/optimization) and provenance | Trajectory-Informed Memory paper (arxiv 2603.10600): Three types of learnings from agent traces. Generic advice is worthless — learnings must be specific, contextual, and traceable to the task that generated them. | 2026-03-26 |
| D49 | Plan annotation cycles until implementation is boring (describes natural behavior at outer zoom levels) | Boris Tane: Three rounds of human annotation on Claude's plan. By the time implementation starts, every decision has been made. This is what NATURALLY HAPPENS at outer zoom levels under D74/D75: at purpose and structure levels, there's almost nothing above to derive answers from, so the D75 self-check gate escalates most questions to the human. The annotation cycle IS frequent human involvement at outer zooms. At inner zooms, the higher-level artifacts resolve most questions, so the human is rarely pulled in. D49 and D75 are compatible: D49 describes the outer-zoom experience, D75 is the general mechanism that produces it. | 2026-03-26 |
| D50 | Two-tier anti-slop rubric: deterministic (automated) + stochastic (LLM-judged) | Code quality research: Tier 1 = formatting, type checking, cognitive complexity, dead code, test coverage (automated in CI). Tier 2 = naming quality, domain language, function responsibility, architectural fit, duplication, refactoring avoidance (LLM reviewer). | 2026-03-26 |
| D51 | "Search before creating" instruction in CLAUDE.md | AI-specific context blindness: agents reimplement existing logic because they generate more readily than they search. CLAUDE.md must instruct: "Before implementing any utility or helper, search the codebase for existing implementations." | 2026-03-26 |
| D52 | Cognitive complexity threshold as deterministic quality gate | SonarSource metric validated by University of Stuttgart study (24K evaluations). Functions > 15 cognitive complexity should be refactored. Add to CI alongside ruff/mypy/tests. | 2026-03-26 |
| D53 | "Domain language preservation" as anti-slop rubric dimension | AI-specific "model collapse" smell: repeated AI edits erode domain terms → generic language. Ubiquitous language file gives reviewer the reference to check against. | 2026-03-26 |
| D54 | Deep modules with clear interfaces — CLAUDE.md architectural guidance | Matt Pocock / Ousterhout: AI can't compensate for bad architecture. Modules must expose clear public APIs. AI should understand a module by reading its interface, not its implementation. | 2026-03-26 |
| D55 | Never pass dicts as args when shape is known | Project owner rule. Use dataclass, TypedDict, NamedTuple, or Pydantic model. CLAUDE.md rule + anti-slop review check. Dict → TypedDict → dataclass migration path. | 2026-03-26 |
| D56 | Python quality stack: ruff + mypy --strict + pytest-cov + cognitive complexity | All pre-configured in pyproject.toml. PostToolUse hook runs ruff + mypy after every edit. Deterministic gates catch Level 1-2 quality. LLM gates catch Level 3-5. | 2026-03-26 |
| D57 | Plan phase includes interface design as explicit step before implementation | Matt Pocock: "Design becomes bottleneck when execution is cheap." Human applies taste at module boundaries. AI implements against those interfaces. | 2026-03-26 |
| D58 | All code quality guidance framed through cognitive load theory lens | Sweller (1988): Three types of load — intrinsic (problem complexity), extraneous (accidental complexity from bad code), germane (learning). Minimize extraneous. Every quality practice justified by its cognitive load impact. | 2026-03-26 |
| D59 | Code must be readable top-to-bottom without jumping between files | Guard clauses for edge cases, one abstraction level per function, named intermediates, colocated helpers. CLAUDE.md conventions for "hand-holding" code. | 2026-03-26 |
| D60 | Extraneous cognitive load checklist as anti-slop review dimension | Seven concrete questions the LLM reviewer asks on every PR: Can I understand this from name+signature? Can I read top-to-bottom? Nesting > 3? Multiple responsibilities? Any "wait what?" moments? Consistent patterns? Standalone comprehensibility? | 2026-03-26 |
| D61 | Generate ARCHITECTURE.md alongside README | matklad: "10x more time to figure out WHERE to change than HOW." High-level mental map of module hierarchy, data flow, conventions. Under 200 lines. Updated rarely. Advance organizer for the codebase. | 2026-03-26 |
| D62 | README uses scaffolded structure: Advance Organizer → Quickstart → Tutorial → Reference | Learning science (Ausubel, Bruner, Paivio): advance organizer creates mental hooks, quickstart proves setup, tutorial guides first task, reference supports independent work. Each section serves a different reader at a different stage. | 2026-03-26 |
| D63 | Mermaid diagrams with rich visual encoding: color + shape + line style + weight | Dual coding theory: each visual sub-channel (color, shape, size, line style) is processed in parallel. 4 dimensions = 4x information density at same cognitive load. Use classDef/linkStyle (GitHub-compatible). Cookiecutter includes Mermaid style guide with colorblind-safe palette, shape conventions, line meanings, and reusable classDef block. | 2026-03-26 |
| D64 | ADR (Architectural Decision Record) infrastructure in docs/decisions/ | Code shows WHAT, comments show HOW, ADRs show WHY. Numbered, immutable, git-tracked. AI agents read ADRs to understand constraints when modifying architecture. | 2026-03-26 |
| D65 | Dev agent alignment via conventions, not checklists (token efficiency + context minimalism) | Tension: encoding quality expectations in dev prompt saves review-fix cycles BUT adds context to every invocation (conflicts with D11/P25.3). Resolution: don't add a "quality gates checklist." Instead, write CLAUDE.md conventions that naturally produce code passing review. "Use dataclasses not dicts" is one line of convention AND a review-failure prevention. Deterministic gates (ruff, mypy) give feedback via PostToolUse hooks — free, no context cost. Only add targeted lines for persistent, specific failure patterns (D27 graduation). The compound step keeps conventions short and high-signal. | 2026-03-26 |
| D66 | Pre-built first, custom only when existing fails criteria | Use official plugins (feature-dev, code-review, ralph-loop, etc.) as the default. Switch to custom ONLY when a specific plugin demonstrably fails our quality or workflow criteria. Evaluate before building. | 2026-03-26 |
| D67 | Custom components are agents/skills/hooks (md files), NOT Python modules | When we do build custom, the artifacts are .md skill files, agent prompts, hook configurations, and slash commands — NOT Python code in the src/ package. The cookiecutter generates a configured workspace of markdown-based agent instructions, not a Python library. | 2026-03-26 |
| D68 | Learning system: build full ACE-informed structure from day one, but treat as hypothesis under active test | Ship with structured entries (unique ID, type tag, helpful/harmful counters, provenance, append-only updates) from the start — don't plan to "add later" because later never comes. BUT treat the structure as a hypothesis, not proven. Include: (1) Retrospective prompt that runs every N cycles asking pointed questions ("Are counters being updated? Are type tags useful? Are entries being retrieved at the right times?"). (2) Clear criteria for "broken" (entries accumulating but never referenced, counters stuck at zero, type tags that don't map to real patterns, file growing without pruning). (3) Documented fallback — if structure creates more friction than value, simplify to plain bullets and capture WHY so next attempt is better-informed. Structure from day one + active failure detection + planned course correction. | 2026-03-26 |
| D69 | "Build the theory, instrument for reality" applies to ALL research-backed components | Generalized from D68: every component backed by research ships with full recommended structure + retrospective questions + "broken" criteria + documented fallback. Applies to: anti-slop rubric dimensions, process ordering/cognitive scaffolding, CLAUDE.md conventions, Mermaid style guide, compound step, AND the zoom process itself (D74). The system is a set of hypotheses we believe in strongly enough to build, but honestly enough to test. **D74 instrumentation:** Retrospective questions: "Does each zoom level's artifact actually help resolve questions at the next level? Are there levels that feel like busywork? Does the D75 self-check gate escalate too often (vague specs) or too rarely (overconfident agent)? Are loops back to higher levels happening when they should? Are artifacts accumulating but not being read?" Broken looks like: human gets prompted at inner levels for things derivable from outer artifacts (spec quality problem); agent proceeds confidently but fails review (self-check too permissive); zoom levels feel bureaucratic rather than genuinely progressive; documentation artifacts go unread. | 2026-03-26 |
| D70 | Human mental energy (not time) is the scarce resource — optimize all human touchpoints for cognitive load | Every prompt, doc, architecture decision, code review, and UI the human encounters must minimize extraneous cognitive load. AI tokens are cheap; human cognitive capacity is finite and non-renewable within a session. Validate every human-facing artifact against: does this require the minimum possible mental energy to process? | 2026-03-27 |
| D71 | Five SE principle flips when optimizing for mental energy | (1) "Working software > comprehensive docs" → good docs save more mental energy than they cost, because AI writes them cheaply. (2) YAGNI partially flips → upfront structure that reduces future cognitive load IS needed. (3) "Don't over-engineer" → "Don't under-design" — cognitive load reducing refactors are almost always worth it. (4) "Move fast break things" → "Move thoughtfully save brains." (5) "Premature optimization is evil" gains a sibling → "Premature COGNITIVE optimization is good." | 2026-03-27 |
| D72 | Model routing via recursive decomposition: cheapest model that's 99.9% reliable for the task | For any complex task, ask: "Can this be broken into subtasks I'm 99.9% confident Haiku could do well without mistakes?" If yes → Haiku. If no → ask the same question with Sonnet. If no → Opus. This makes planning do double duty: decomposing for human comprehension AND for model routing simultaneously. A well-decomposed plan naturally routes to cheaper models because each piece is small and well-specified enough for a less capable model. Connects to D49 (implementation should be boring): boring = specified precisely enough that Haiku can execute it. **Critical caveat:** Don't rely on Opus's judgment to assess whether Haiku can handle a task — LLMs lack accurate models of other models' capabilities (P25.5 applied to meta-judgment). Instead, build an empirical map: start with a reasonable guess for task-type-to-model routing, track success/fail per model tier in the learning store, and let actual outcomes correct the routing over time. The learning store naturally accumulates "Haiku failed on cross-file reasoning tasks" and "Haiku succeeded on single-function implementations" as strategy entries. | 2026-03-27 |
| D73 | Review model strategy: evaluate Opus single-reviewer vs. Haiku swarm with narrow prompts | Haiku swarm has appealing property: each agent gets a tiny focused prompt ("check ONLY domain language") where Haiku can be reliable. But noisy false positives cost human mental energy (D70). Evaluate both approaches per D69 (instrument for reality). "Broken" criteria for Haiku swarm: false positive rate > 20%, human routinely dismisses findings. "Broken" criteria for Opus single: misses issues that narrow-focus agents would catch. The confidence scoring from Anthropic's code-review plugin (threshold 80/100) is the noise filter mechanism regardless of model choice. | 2026-03-27 |
| D74 | Development process: zoom-based progressive concretization with self-check loop | Unified process combining 5 hypotheses: (1) Work at zoom levels from outer (purpose) to inner (implementation). (2) At each level: identify 3-4 open questions, self-check "can I answer from higher-level artifacts?", resolve what you can autonomously, escalate ONLY genuine uncertainties to human as focused questions, verify consistency with levels above, zoom in. (3) Human involvement is pull-based not push-based — agent works autonomously, pulls human in only for genuine ambiguity. (4) Documentation (advance organizer, ARCHITECTURE.md, ADRs, interfaces) is produced as the TOOL for thinking at each level, not as afterthought. (5) Same process for new repos and new features — start at whatever zoom level has unresolved questions. Resolves Q12. | 2026-03-27 |
| D75 | Agent self-check gate: "Do I have enough information to proceed without prompting the human?" | Before escalating to human, agent must verify the question can't be answered from higher-level artifacts. If it can → proceed autonomously. If it genuinely can't → formulate the SPECIFIC uncertainty as one focused question, not "please review this." Quality of outer zoom levels directly determines how autonomous inner levels can be. Vague purpose = constant interruptions. Precise purpose = agent resolves most questions itself. This is P16.1 (specification bottleneck) made operational. | 2026-03-27 |
| D76 | uv for dependency management | Fast, standard pyproject.toml, same team as ruff, ecosystem momentum. CLAUDE.md setup section uses `uv sync`. Quickstart uses `uv run`. Lockfile is `uv.lock`. Per D69: if uv causes friction, document why and evaluate alternatives. | 2026-03-27 |
| D77 | Testing stack: pytest + pytest-cov always; hypothesis and mutmut as cookiecutter opt-in | pytest + pytest-cov = non-negotiable baseline, always included. hypothesis = opt-in cookiecutter variable (pairs well with typed interfaces — auto-generates test inputs from dataclass definitions). mutmut = opt-in cookiecutter variable (powerful quality validation but slow, noisy on large codebases). nox excluded from default (overkill for single-user applications). | 2026-03-27 |
| D78 | Use official ralph-loop plugin for autonomous operation (D66: pre-built first) | Start with the official plugin. If Opus 4.6 compaction handles context growth (D41), session persistence is an advantage. If context growth causes issues, switch to custom bash loop with fresh context per iteration. Test before building custom. Per D69: "broken" = context quality degrades across iterations, agent repeats mistakes from earlier iterations, or loop doesn't terminate cleanly. | 2026-03-27 |
| D79 | Local story files for task backlog (simplest, agent-optimal) | Stories live in `stories/` directory as markdown files. Agent reads directly from filesystem — fast, no API, works identically in local and remote Claude Code. No GitHub Issues dependency. Story file IS the spec and tracking artifact (failing-to-passing checklist, D44). Completed stories move to `stories/done/`. Add GitHub Issues integration later if collaborator visibility or PR linkage becomes needed. | 2026-03-27 |
| D80 | Context management: externalize state as discipline, rely on compaction, test rotation as fallback | Can't decide context rotation vs compaction theoretically — needs empirical testing. Strategy: enforce good state externalization regardless (story files, learning store, ARCHITECTURE.md all current). This makes BOTH approaches viable. Default to Opus 4.6 compaction. If compaction degrades quality during Ralph loops (agent repeats mistakes, loses track of progress, contradicts earlier decisions), activate manual context rotation. Per D42: treat compaction prompts as optimizable targets. Resolves D37/D41. | 2026-03-27 |

---

## 20. Learnings Captured

*No learnings captured yet — system is in planning phase.*

---

## Phase Dependencies

```
Phase 0 (Research) ← In Progress
    │
    ▼
Phase 1 (Architecture) ← Q5, Q9, Q10
    │
    ▼
Phase 2 (Scaffold) ← Q9
    │
    ├──────────────────────────┐
    ▼                          ▼
Phase 3 (Core Agent)    Phase 8 (Dev Tooling)
    │
    ├──────────┬───────────────┐
    ▼          ▼               ▼
Phase 4    Phase 5         Phase 7
(Anti-Slop) (Human IX)    (Learning)
    │          │
    ▼          ▼
Phase 6 (Ralph Wiggum Loop)
    │
    ▼
Phase 9 (Integration Testing)
    │
    ▼
Phase 10 (Documentation)
```

## Estimated Timeline

| Phase | Duration | Blockers |
|-------|----------|----------|
| Phase 0: Research | 1–2 weeks | None — can proceed |
| Phase 1: Architecture | 1 week | Phase 0, Q5, Q9, Q10 |
| Phase 2: Scaffold | 2–3 days | Phase 1 |
| Phase 3: Core Agent | 1–2 weeks | Phase 2 |
| Phase 4: Anti-Slop | 1 week | Phase 3 |
| Phase 5: Human Interaction | 1 week | Phase 3, Q5 |
| Phase 6: Ralph Wiggum | 1 week | Phases 3, 4, 5 |
| Phase 7: Learning | 3–5 days | Phase 3 |
| Phase 8: Dev Tooling | 2–3 days (∥ Phase 3) | Phase 2, Q9 |
| Phase 9: Integration Test | 1 week | Phases 3–8 |
| Phase 10: Docs | 3–5 days | Phases 1–9 |
| **Total** | **~7–10 weeks** | |

---

*Living document. Updated as decisions are made and work progresses.*
