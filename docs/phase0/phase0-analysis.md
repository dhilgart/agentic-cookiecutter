# Phase 0 — Analysis: Taxonomy, Complement/Conflict Map, Reasoning Audit

**155+ practices across 34 categories → 7 themes, 11 complement clusters, 8 tensions, 3 reasoning tiers**
**80 decisions (D1-D80), 14 core principles**
**Last Updated:** 2026-03-27

---

## 1. Category Taxonomy

The 34 categories group into 7 themes. Each theme addresses a distinct architectural concern.

### Theme A: Workflow & Process ("How work flows from idea to shipped code")

| Category | Focus | Key Decisions |
|----------|-------|---------------|
| 1. Workflow Architecture | Pipeline: grill-me → PRD → issues → execute → QA | D47, D74, D75 |
| 8. Human-Agent Interaction | Grill-me, plan mode, concise context | D49, D70, D75 |
| 14. BMAD | Story files, right-sizing, adversarial review | D25 (adopt stories, discard personas) |
| 17. Obra/Superpowers | Mandatory workflows, two-stage review | D34 (two-stage review) |
| 28. Dan Shipper / Every | Compound engineering loop, 12-agent review | D47 (default workflow shorthand) |

**Theme summary:** The development process is **zoom-based progressive concretization** (D74). At every zoom level: identify 3-4 questions → self-check "can I answer from higher-level artifacts?" (D75) → resolve autonomously or escalate specific uncertainty → verify consistency → zoom in. Human involvement is pull-based, not push-based. D47 (Plan→Work→Assess→Compound) is the simplified shorthand: Plan = outer zoom levels, Work = implementation, Assess = verify + gates, Compound = zoom out + codify. Annotation cycles (D49) describe what naturally happens at outer zoom levels under D75 — the human is pulled in frequently because the agent can't derive purpose/structure answers autonomously. Story files (D25) with failing-to-passing checklists (D44) live locally in `stories/` (D79).

### Theme B: Context & Memory ("How agents remember and what they forget")

| Category | Focus | Key Decisions |
|----------|-------|---------------|
| 4. Context Management | Minimal CLAUDE.md, /clear, subagent isolation | D11, D20, D65 |
| 20. HumanLayer | CLAUDE.md as highest leverage point | D11, D20 |
| 22. ACE Paper | Structured bullets with usage metadata | D39, D68 |
| 29. Agent Memory Papers | Trajectory-informed memory, three types of learnings | D48 (learning entry taxonomy) |

**Theme summary:** CLAUDE.md must be minimal (D11) because context length alone degrades performance (D43). Dev agent alignment via conventions, not checklists (D65) — conventions serve double duty as coding guidance AND review-failure prevention without context bloat. Learnings live in a separate file with structured bullets, usage counters, and types (strategy/recovery/optimization) per D39/D48. Build full ACE-informed structure from day one (D68) but treat as hypothesis under active test (D69). Compaction prompts are optimizable targets (D42). State externalization is a discipline regardless of compaction vs rotation strategy (D80).

### Theme C: Quality & Anti-Slop ("How we ensure code quality at every level")

| Category | Focus | Key Decisions |
|----------|-------|---------------|
| 3. TDD & Testing | TDD as primary anti-slop, test behavior not implementation | D3, D77 |
| 5. Hooks & Automation | PostToolUse for ruff, git guardrails | D14, D19 |
| 9. Quality & Review | Writer/reviewer separation, verification loops | D34, D73 |
| 23. Anthropic Harness | GAN-inspired generator/evaluator, self-eval bias | D40 (named quality dimensions) |
| 25. Academic Papers (eval) | LLM-as-judge failures (52-78%), multi-dimensional review | D50 (two-tier rubric) |
| 30. Code Quality | Timeless principles, AI-specific smells | D50, D51, D52, D53 |
| 33. Cognitive Load Theory | Extraneous load checklist, hand-holding code | D58, D59, D60 |

**Theme summary:** Two-tier anti-slop rubric (D50). **Tier 1 (deterministic):** ruff, mypy --strict, cognitive complexity thresholds (15), dead code, test coverage — automated via PostToolUse hooks and CI. **Tier 2 (stochastic, LLM-judged):** 7 dimensions — naming quality, domain language preservation, function responsibility, architectural fit, unnecessary duplication, refactoring avoidance, cognitive load checklist — run by separate review agent(s). Self-evaluation bias (P26.1) means generator and reviewer MUST be separate agents. Review model strategy (D73): evaluate Opus single-reviewer vs Haiku swarm with narrow prompts. All quality guidance framed through cognitive load theory lens (D58). Testing stack: pytest + pytest-cov always; hypothesis and mutmut as cookiecutter opt-in (D77).

### Theme D: Architecture & Skills ("How the codebase and agent skills are structured")

| Category | Focus | Key Decisions |
|----------|-------|---------------|
| 2. Skills Design | Progressive disclosure, short but impactful | D36 (AutoResearch) |
| 6. Codebase Architecture | Deep modules, thin interfaces | D54 |
| 26. Anthropic Engineering Blog | Three-level skill architecture, sandboxing | D26 |
| 31. Architectural Principles | Pocock/Ousterhout deep modules, sinks not pipes | D54, D57 |
| 32. Python-Specific | Type hints, dataclasses, mypy, error handling | D55, D56 |

**Theme summary:** Skills use three-level progressive disclosure (P26.2). Codebase uses deep modules with clear interfaces (D54). Plan phase includes explicit interface design (D57). Python code uses typed structures (dataclass/TypedDict/Pydantic), never raw dicts for known shapes (D55). Quality stack: ruff + mypy --strict + pytest-cov + cognitive complexity (D56). Dependency management: uv (D76). Human-expert skills dramatically outperform LLM-generated ones (P25.7) — AutoResearch optimizes human-written skills, doesn't generate from scratch.

### Theme E: Autonomous Operation ("How agents work without human intervention")

| Category | Focus | Key Decisions |
|----------|-------|---------------|
| 7. Ralph Wiggum | Max iterations, stuck detection, independent context | D5, D78 |
| 10. Boris Cherny | 5 parallel sessions, /permissions, PostToolUse | D13, D14 |
| 21. YouTube Tactical | Context rot, git worktree, AutoResearch | D36, D37, D38 |

**Theme summary:** Autonomous loops use the official ralph-loop plugin (D78, D66: pre-built first). Context management: externalize state as discipline, default to compaction, test rotation as fallback (D80). Git worktrees for isolation (D38). Model routing via recursive decomposition (D72): cheapest model that's 99.9% reliable for the task, refined empirically via learning store (don't trust Opus to judge Haiku's capabilities). Sandboxing reduces permission prompts by 84% (P26.3). The "land the plane" pattern (D35) ensures clean state at session end.

### Theme F: Composition & Tooling ("What the cookiecutter actually produces")

| Category | Focus | Key Decisions |
|----------|-------|---------------|
| 11. Matt Pocock Skills | Direct installation candidates (grill-me, tdd, etc.) | D18 |
| 12/27. Plugin Ecosystem | 9K+ plugins, feature-dev 89K installs, composition | D45, D46, D66 |
| 24. GitHub Primitives | Three-layer framework | — |
| 34. Documentation Design | ARCHITECTURE.md, scaffolded README, dual coding, ADRs | D61, D62, D63, D64 |

**Theme summary:** The cookiecutter is a **composition and configuration layer** (D46), not a component builder. Pre-built first, custom only when existing fails criteria (D66). Custom components are agents/skills/hooks in .md files, NOT Python modules (D67). It produces: settings.json (plugin config), CLAUDE.md template, skill templates with eval files, hook configurations, learning store structure, story file templates, ARCHITECTURE.md (D61), scaffolded README with advance organizer (D62), Mermaid diagrams with rich visual encoding (D63, color + shape + line style + weight), ADR infrastructure (D64), and local story file backlog (D79).

### Theme G: Philosophical Foundations ("Why the system is designed this way")

| Category | Focus | Key Decisions |
|----------|-------|---------------|
| 13. Karpathy | Taste problem, vibe coding → agentic engineering | — |
| 16. Nate B. Jones | Specification bottleneck, harness > model, supervision | D31 |
| 18. Steve Yegge | 50 First Dates, design as bottleneck | D35 |
| 19. SDD Ecosystem | Spec quality = code quality | — |

**Theme summary:** 97.5% of agent failures are specification failures, not model failures (P16.1). The harness matters more than the model — 78% vs 42% on same benchmarks (D31). The cookiecutter IS the harness. Two additional philosophical principles emerged from ideation: **Build the theory, instrument for reality (D69)** — every research-backed component ships with full structure + retrospective questions + "broken" criteria + documented fallback. **Human mental energy is the scarce resource (D70)** — every human touchpoint minimizes extraneous cognitive load. Five SE principles flip (D71): docs worth it now, cognitive YAGNI, don't under-design, save brains, premature cognitive optimization is good.

---

## 2. Complement/Conflict Map

### Complement Clusters

11 clusters of practices that reinforce each other:

1. **Context minimalism chain:** D11 (minimal CLAUDE.md) + D43 (length hurts) + D65 (conventions not checklists) + P25.3 (context-length degrades)
2. **Anti-slop pipeline:** D50 (two-tier rubric) + D34 (separate reviewer) + D14 (PostToolUse hooks) + D52 (complexity threshold) + D60 (cognitive load checklist)
3. **Learning accumulation:** D39/D48 (structured entries) + D27 (3+ recurrences → gates) + D47 (compound step) + D68 (full structure day one) + D69 (instrument for reality)
4. **Specification precision:** P8.1 (grill-me) + D49 (annotation cycles) + D57 (interface design) + D44 (failing checklists) + D74/D75 (zoom process with self-check)
5. **Plugin composition:** D46 (composition layer) + D66 (pre-built first) + D67 (custom = .md files) + D45 (official code-review baseline) + D78 (official ralph-loop)
6. **Cognitive load reduction:** D58 (CLT lens) + D59 (top-to-bottom) + D55 (no bare dicts) + P33.3 (familiarity) + D70 (mental energy is scarce)
7. **Documentation as thinking tool:** D61 (ARCHITECTURE.md) + D62 (scaffolded README) + D63 (rich Mermaid) + D64 (ADRs) + D74 (artifacts at each zoom level) + D71 (docs worth it now)
8. **Model routing:** D72 (cheapest reliable model) + D73 (review model strategy) + D26 (right-size to task) + D74 (zoom level = routing signal)
9. **Process governance:** D74 (zoom process) + D75 (self-check gate) + D49 (annotation cycles at outer zoom) + D47 (shorthand) + D70 (pull-based involvement)
10. **Instrumentation:** D69 (instrument for reality) + D68 (learning store hypothesis) + D73 (review model evaluation) + D80 (compaction vs rotation testing)
11. **Token efficiency:** D65 (conventions not checklists) + D72 (cheapest model) + P28.1 (compound step saves future tokens) + D74 (better specs → cheaper inner zooms)

### Tensions

8 tensions identified, all resolved or managed:

| # | Tension | Resolution |
|---|---------|------------|
| T1 | Minimal context (D11) vs. encoding quality expectations (D65 early version) | D65 updated: conventions not checklists. CLAUDE.md stays minimal; conventions serve double duty. |
| T2 | Pre-built plugins (D66) vs. custom quality requirements | D66 says pre-built FIRST, switch to custom when existing demonstrably fails. Not dogmatic. |
| T3 | Full ACE structure (D68) vs. YAGNI | D68 resolved: build structure from day one because "add later" = "never add." But instrument for reality (D69). |
| T4 | Deterministic gates (reliable) vs. stochastic gates (powerful) | D50: two tiers. Stochastic supplements, never replaces deterministic. Confidence threshold filters noise. |
| T5 | Context rotation (proven) vs. compaction (convenient) | D80: externalize state regardless (makes both work). Default to compaction, test rotation as fallback. |
| T6 | D49 (frequent human annotation) vs. D75 (minimize human prompts) | Resolved: D49 describes what naturally happens at OUTER zoom levels under D75. Inner levels are autonomous. Same mechanism, different zoom level. |
| T7 | SOLID/DRY abstraction vs. cognitive load from indirection | D58/D71: frame through cognitive load. Abstraction that reduces load = good. Abstraction that adds indirection without reducing load = bad. |
| T8 | Opus quality vs. token cost | D72: cheapest model that's 99.9% reliable. Better specs → more work routes to cheaper models. Planning ROI includes token savings. |

---

## 3. Reasoning Audit

### Tier 1 — Strongest Evidence (empirical measurement or convergent practitioner evidence)

| Practice | Evidence Type | Why It's Top Tier |
|----------|-------------|-------------------|
| P25.3 (context length hurts) | Empirical — multi-model, calibrated study | Directly measured: performance degrades with context length even with perfect retrieval. |
| P25.5 (LLM judge 52-78%) | Empirical — RCRR metric across models | Quantifies the limit of LLM judgment. |
| P25.7 (human skills >> LLM skills) | Empirical — IoT-SkillsBench, 42 tasks, 3 platforms | LLM-generated skills sometimes worse than no skills. |
| P22.1-3 (ACE framework) | Empirical — +10.6% on agent benchmarks (ICLR 2026) | Structured bullets + counters > monolithic prompts. Peer-reviewed. |
| P25.2 (ACON compression) | Empirical — 26-54% token reduction preserving accuracy | Failure-driven optimization works. |
| P29.2 (self-improving agent) | Empirical — 17-53% gains on SWE-bench Verified | Agent self-editing its harness. Directly measured. |
| P26.1 (self-eval bias) | Practitioner — Anthropic internal, reproducible | Agents rubber-stamp own work. |
| P26.3 (sandboxing 84%) | Practitioner — Anthropic internal measurement | 84% fewer permission prompts. |
| P10.1-7 (Boris Cherny) | Practitioner — creator of Claude Code, daily use | 53 tips from the person who built the tool. |
| P30.3 (cognitive complexity) | Empirical — Stuttgart study (24K evaluations) | Higher complexity → longer comprehension time. |
| P30.2 (naming = #1 readability) | Empirical — study of 25 code features | Naming consistency most influential factor. |
| P28.1 (compound engineering) | Practitioner — Every.to, 2 engineers → output of 15 | Named methodology, production results. |
| P27.1-2 (plugin ecosystem) | Market data — 89K installs, 9K+ plugins | Community validated via installations. |
| P5.2 (PostToolUse hooks) | Practitioner — Boris Cherny + Every + Anthropic | Multiple independent teams converged. |
| P4.1 (minimal CLAUDE.md) | Practitioner + empirical (P25.3 validates) | Multiple practitioners + academic confirmation. |

### Tier 2 — Strong Reasoning (practitioner-tested or well-reasoned theory)

| Practice | Evidence | Assessment |
|----------|----------|------------|
| P1.1 (pipeline) | Practitioner — Pocock, widely adopted | Subsumed by D74 zoom process. |
| P3.1 (TDD as anti-slop) | Practitioner + theory | Sound within scope (functional, not taste). |
| P8.1 (grill-me) | Practitioner — Pocock skill, 1000s of installs | Surfaces hidden assumptions. |
| P9.1 (writer/reviewer) | Practitioner + P26.1 validates | Separate contexts prevent self-eval bias. |
| P16.1-15 (Nate B. Jones) | Practitioner + podcast (27 episodes) | Philosophical frameworks from production. |
| P30.1 (SOLID/DRY/KISS) | Theory + decades of practice | Risk: over-application (T7). |
| P30.6-9 (AI-specific smells) | Practitioner + academic | Observed and confirmed. |
| P31.1-4 (architecture) | Theory + practitioner (Pocock, Ousterhout) | Deep modules, progressive disclosure. |
| P32.1-7 (Python practices) | Community consensus + tooling | PEP 8, mypy, dataclasses. Sound for 3.12+. |
| P33.1-6 (cognitive load theory) | Theory (Sweller, Cowan) + application | Well-established cognitive science. |
| P17.2 (two-stage review) | Practitioner — Obra/Superpowers | Spec + code quality as separate passes. |
| P21.4 (AutoResearch) | Practitioner — single report, 41%→92% | Sound approach. |
| P23.1 (three-agent system) | Practitioner — Anthropic Labs | Latest harness design. |
| D46 (composition layer) | Market analysis + practitioner | Plugin ecosystem validates. |
| D49 (annotation cycles) | Practitioner — Boris Tane | Outer-zoom behavior under D75. |
| D74 (zoom process) | Synthesized from CLT, Ausubel, C4, Bruner, Sweller | Novel. Internally consistent. Needs production validation (D69). |
| D70/D71 (mental energy + SE flips) | Theory (NASA-TLX, CLT) + reasoning | Well-grounded. Needs production validation. |

### Tier 3 — Reasonable But Unvalidated

| Practice | Evidence | Risk |
|----------|----------|------|
| P7.1 (max iterations) | Heuristic | Right number needs tuning per task. |
| P8.3 (sacrifice grammar) | Single source (Boris Cherny) | Context-dependent. |
| P14.2 (BMAD lifecycle) | Single framework | Subsumed by D74. |
| P16.10 (simulation) | Single source, limited | Not universal. |
| P19.2 (constitution) | Single framework (SDD) | May add extraneous load. |
| P19.3 (50KB limit) | Single source, dated | Threshold wrong; principle sound. |
| P28.2 (12-subagent review) | Single team (Every.to) | D73 captures evaluate-both. |
| P33.4 (40-min confusion) | Single source (zakirullin) | Design philosophy only. |
| P23.2 (GAN evaluator) | Single implementation | Dimensions adapted in D50. |

### Zero Practices Flagged as Unsound

No practice has fundamentally flawed reasoning. Weakest entries are reasonable but unvalidated.

---

## 4. Key Findings

### Finding 1: The strongest evidence cluster is context engineering
Five of the top 15 Tier 1 practices relate to context management. Less context = better performance, structured > unstructured, incremental > rewrites.

### Finding 2: The anti-slop pipeline has the deepest research support
D50 is validated by LLM-as-judge failure rates, self-eval bias, cognitive complexity studies, naming studies, and Anthropic's GAN evaluator.

### Finding 3: The learning system has the best theory and least production validation
Resolution: build full structure day one, instrument for reality (D68, D69).

### Finding 4: Cognitive load theory is the unifying framework
Every quality practice reduces extraneous load through the same mechanism. Extended in D70/D71: human mental energy is the scarce resource, which flips five SE principles.

### Finding 5: The composition architecture is validated by market data
89K installs, 9K+ plugins. Pre-built first (D66), custom = .md files (D67).

### Finding 6: The zoom process (D74) is a novel synthesis
Emerged from combining 5 hypotheses grounded in different research. Internally consistent but unvalidated. Per D69: instrument and watch.

### Finding 7: The system is a set of testable hypotheses
Per D69, every component ships with retrospective questions and "broken" criteria. The system is hypotheses we believe in strongly enough to build, but honestly enough to test.

---

*This analysis accompanies the raw catalogue (`phase0-research-catalogue.md`), project tracker (`agentic-workflow-tracker.md`), and Phase 1 design inputs (`phase1-design-inputs.md`). Together they represent the complete Phase 0 research output.*
