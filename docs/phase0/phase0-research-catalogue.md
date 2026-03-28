# Phase 0 — Research Catalogue: Agentic Coding Best Practices

**Status:** Complete — 155+ practices across 34 categories. Full research, analysis, and audit complete.
**Last Updated:** 2026-03-26
**Ranking Criterion:** Soundness of reasoning (not frequency of repetition)

---

## Research Methodology

Each practice is catalogued with:
- **Source**: Who recommends this
- **Practice**: What they recommend
- **Reasoning**: Why they say it works
- **Assessment**: Is the reasoning sound given current AI state (March 2026)?
- **Relevance**: How directly applicable to our cookiecutter project
- **Adopt?**: Preliminary recommendation

---

## Category 1: Workflow Architecture (Idea → Shipping Code)

### P1.1 — Pipeline: Grill-Me → PRD → Issues → Execute → QA

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (daily workflow, AI Hero) |
| **Practice** | Chain skills in a linear pipeline: `/grill-me` (reach shared understanding) → `/write-a-prd` (formalize requirements) → `/prd-to-issues` (break into independently grabbable vertical slices) → execute via Ralph Wiggum loop → manual QA |
| **Reasoning** | Each skill forces a specific quality checkpoint. Grill-me prevents misunderstanding. PRD prevents scope creep. Prd-to-issues prevents horizontal slicing. TDD during execution prevents slop. Manual QA catches what automation misses. |
| **Assessment** | ✅ Sound. The pipeline enforces discipline at each stage. The reasoning addresses the exact failure mode each step prevents. The "3 sentences" grill-me skill generating 16-50 questions proves that constraint breeds thoroughness. |
| **Relevance** | 🔴 Direct — this is our core workflow architecture. |
| **Adopt?** | ✅ Yes — adapt for Python/Claude Code context. Consider which Matt Pocock skills to install directly vs. fork. |

### P1.2 — Vertical Slices, Not Horizontal

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (prd-to-issues skill), Rich Tabor (ralph implementation) |
| **Practice** | Break work into thin vertical slices through all integration layers, not horizontal slices of one layer. Each issue should be independently grabbable. |
| **Reasoning** | Horizontal slices (write all tests, then write all code) produce tests that validate imagined implementation, not actual behavior. Vertical slices produce working features that can be verified independently. Also enables parallelism — independent slices can be worked by parallel agents. |
| **Assessment** | ✅ Sound. This directly addresses the "tests pass but code fails in practice" pain point. Vertical slices are inherently more testable and verifiable. |
| **Relevance** | 🔴 Direct — addresses Dan's pain point. |
| **Adopt?** | ✅ Yes |

### P1.3 — Size Work to One Context Window

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (Claude Code for Real Engineers), Rich Tabor, Anthropic best practices |
| **Practice** | Each task/issue should be sized to fit within one context window. Features that span more than one context window need PRDs to provide framing across sessions. |
| **Reasoning** | Claude's performance degrades as context fills. Fresh context = better reasoning. PRDs bridge context boundaries by providing shared understanding that can be re-loaded. |
| **Assessment** | ✅ Sound. Confirmed by Anthropic's own docs: "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills." |
| **Relevance** | 🔴 Direct — affects how we size backlog items and Ralph Wiggum loop iterations. |
| **Adopt?** | ✅ Yes |

### P1.4 — PRD Dependency Graphs for Overnight Execution

| Field | Value |
|-------|-------|
| **Source** | Rich Tabor (ralph blog post) |
| **Practice** | Structure PRDs as JSON with `dependsOn` fields. Ralph won't start a feature until its dependencies are complete. When all stories in a PRD have `passes: true`, Ralph pushes the branch, creates a PR, and moves to the next PRD in the graph. |
| **Reasoning** | Dependency ordering prevents Ralph from starting work that requires incomplete prerequisites. Structured JSON allows deterministic checking of completion state. |
| **Assessment** | ✅ Sound. This is effectively our backlog manager with dependency tracking — proven in production by Rich Tabor. The JSON structure provides the deterministic completion checking our system needs. |
| **Relevance** | 🔴 Direct — maps to our backlog manager + Ralph Wiggum loop controller. |
| **Adopt?** | ✅ Yes — evaluate Rich Tabor's skill implementations alongside our design. |

---

## Category 2: Skills Design

### P2.1 — Skills Don't Have to Be Long to Be Impactful

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (grill-me is 3 sentences; generates 16-50 questions per session) |
| **Practice** | Choose the right words at the right time. A well-crafted 3-sentence skill can be more impactful than a 200-line spec. |
| **Reasoning** | LLMs are good at expanding terse, well-chosen instructions into thorough behavior. Over-specifying constrains the model and wastes context. The skill just needs to set the right *intent* and *mode*. |
| **Assessment** | ✅ Sound. Aligns with the arxiv 2602.11988 finding that comprehensive context files hurt performance. Minimal, surgical instructions > exhaustive documentation. |
| **Relevance** | 🔴 Direct — our skill design philosophy. |
| **Adopt?** | ✅ Yes |

### P2.2 — Skill Description Is the Only Thing the Agent Sees for Selection

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (write-a-skill), Anthropic (skills docs) |
| **Practice** | The `description` field in SKILL.md frontmatter is surfaced in the system prompt alongside all other installed skills. The agent reads descriptions and picks the relevant skill. Make descriptions specific enough to trigger correctly. |
| **Reasoning** | Good trigger language prevents skills from being invoked at the wrong time or not invoked when needed. Bad descriptions ("helps with documents") give the agent no way to distinguish from other similar skills. |
| **Assessment** | ✅ Sound. Confirmed by Anthropic docs: "Skill descriptions are loaded into context so Claude knows what's available. The budget scales dynamically at 2% of the context window." |
| **Relevance** | 🔴 Direct — affects how we write all our skill descriptions. |
| **Adopt?** | ✅ Yes |

### P2.3 — Progressive Disclosure in Skills (Reference Files)

| Field | Value |
|-------|-------|
| **Source** | Anthropic (skills docs), Matt Pocock (write-a-skill) |
| **Practice** | Keep the main SKILL.md focused. Put detailed reference content in separate files (e.g., `REFERENCE.md`, `EXAMPLES.md`) that the skill can reference. This controls context cost — the agent only loads the detail when it needs it. |
| **Reasoning** | Reduces context window consumption. The description + SKILL.md summary is always loaded; supporting files are loaded on demand. |
| **Assessment** | ✅ Sound. Directly supported by Anthropic's context management architecture. |
| **Relevance** | 🟡 Medium — relevant for complex skills like TDD that need substantial philosophy/rules. |
| **Adopt?** | ✅ Yes |

### P2.4 — disable-model-invocation for Side-Effect Skills

| Field | Value |
|-------|-------|
| **Source** | Anthropic (skills docs) |
| **Practice** | Set `disable-model-invocation: true` in frontmatter for skills with side effects you want to trigger manually (e.g., deploy, release). This hides the skill from Claude's auto-selection, reducing context cost to zero until manually invoked. |
| **Reasoning** | Not every skill should be auto-triggered. Deploy, release, and destructive operations should only run when the human explicitly invokes them. Also saves context budget. |
| **Assessment** | ✅ Sound. Clear separation between reference skills (auto-invoked) and action skills (manually invoked). |
| **Relevance** | 🟡 Medium — relevant for our deploy-like skills. |
| **Adopt?** | ✅ Yes |

---

## Category 3: TDD & Testing

### P3.1 — TDD as the Primary Anti-Slop Mechanism

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (TDD skill), NCAA eval learnings |
| **Practice** | Use strict red-green-refactor loops: write exactly one failing test → write minimal code to pass → refactor. Build features one vertical slice at a time, not all tests first then all implementation. |
| **Reasoning** | "Horizontal slicing" (write all tests, then implementation) produces tests that validate the imagined implementation, not actual behavior. Vertical TDD creates a feedback loop where each test verifies one observable behavior. Tests survive refactors because they test behavior, not implementation details. |
| **Assessment** | ✅ Sound. This is the most consistent way to improve agent outputs according to Matt Pocock's experience. Directly addresses Dan's pain point of tests that over-constrain future code. |
| **Relevance** | 🔴 Direct — core testing philosophy. |
| **Adopt?** | ✅ Yes — install Matt Pocock's TDD skill directly or adapt for Python. |

### P3.2 — Test Behavior, Not Implementation

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (TDD skill), NCAA eval (multiple learnings), Dan's pain points |
| **Practice** | Frame assertions in terms of observable outputs and side effects. Never assert internal method calls, private attribute values, or implementation structure. Tests should survive refactors. |
| **Reasoning** | Tests that assert implementation details break when code is refactored even though behavior is preserved. This creates false negatives that waste time and erode trust in the test suite. |
| **Assessment** | ✅ Sound. NCAA eval documented this failing repeatedly across multiple stories. This is the single most important testing principle. |
| **Relevance** | 🔴 Direct — Dan's explicit pain point. |
| **Adopt?** | ✅ Yes — bake into TDD skill, anti-slop test quality gate, and learning store. |

### P3.3 — Objective Completion Criteria for Every Story

| Field | Value |
|-------|-------|
| **Source** | Rich Tabor, Matt Pocock (PRD skill) |
| **Practice** | Every story/issue needs deterministic success criteria: "Typecheck passes," "Lint passes," "Tests pass." UI stories need "Verify at localhost:3000/path." Don't accept vague criteria like "works correctly." |
| **Reasoning** | Ralph Wiggum loops converge when success criteria are objective and testable. Vague criteria cause the loop to run endlessly or stop prematurely. The agent needs to be able to deterministically verify completion. |
| **Assessment** | ✅ Sound. This is the foundation of reliable autonomous execution. Without objective criteria, the completion promise is meaningless. |
| **Relevance** | 🔴 Direct — affects PRD skill, backlog items, and Ralph Wiggum loop prompts. |
| **Adopt?** | ✅ Yes |

---

## Category 4: Context Management

### P4.1 — CLAUDE.md Should Be Minimal and Surgical

| Field | Value |
|-------|-------|
| **Source** | Arxiv 2602.11988 (ETH Zurich), Anthropic best practices |
| **Practice** | Include only: non-obvious tooling, project-specific conventions tools can't enforce, known footguns. Exclude: directory trees, style guides (use linters), comprehensive overviews (agent reads README), general best practices (agent already knows). |
| **Reasoning** | ETH Zurich found LLM-generated context files reduce task success by ~3% and increase cost 20%+. Even human-written files only marginally help (+4%). The problem is unnecessary requirements making tasks harder. But tool-specific instructions have a massive multiplier effect. |
| **Assessment** | ✅ Sound. Backed by rigorous academic research across multiple agents and models. Consistent with Anthropic's own advice: "If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise." |
| **Relevance** | 🔴 Direct — already adopted as D11. |
| **Adopt?** | ✅ Already adopted |

### P4.2 — Use /clear After Two Failed Corrections

| Field | Value |
|-------|-------|
| **Source** | Anthropic best practices |
| **Practice** | When correcting Claude repeatedly and it's still wrong, `/clear` and write a better initial prompt incorporating what you learned. Don't keep polluting context with failed approaches. |
| **Reasoning** | Context pollution from failed attempts degrades Claude's ability to reason about the correct approach. Fresh context + better prompt > accumulated failure history. |
| **Assessment** | ✅ Sound. Maps to the Ralph Wiggum philosophy — each loop iteration starts fresh (in the bash approach) or at least with cleaner context. |
| **Relevance** | 🟡 Medium — affects how our skills handle retries within a single session. |
| **Adopt?** | ✅ Yes — build into retry logic within skills. |

### P4.3 — Subagents for Context Isolation

| Field | Value |
|-------|-------|
| **Source** | Anthropic (subagents docs) |
| **Practice** | Use subagents when: the task produces verbose output you don't need, you want specific tool restrictions, or the work is self-contained. Subagents run in their own context, returning only summaries to the main conversation. |
| **Reasoning** | Subagents prevent context pollution. A code review that reads 50 files shouldn't fill your main context window. Also enables the Writer/Reviewer pattern — fresh context improves review quality since Claude won't be biased toward code it just wrote. |
| **Assessment** | ✅ Sound. The Writer/Reviewer pattern directly addresses the "agent reviews its own code" anti-pattern. Critical for our anti-slop pipeline. |
| **Relevance** | 🔴 Direct — our LLM-as-judge review gates should use subagents for unbiased review. |
| **Adopt?** | ✅ Yes |

### P4.4 — Subagent Memory for Persistent Learning

| Field | Value |
|-------|-------|
| **Source** | Anthropic (subagents docs) |
| **Practice** | Use the `memory: user` field in subagent definitions. The subagent gets a persistent directory that survives across conversations, building knowledge like codebase patterns, debugging insights, and architectural decisions. First 200 lines of MEMORY.md are loaded at session start. |
| **Reasoning** | Subagents with memory can learn over time — a code reviewer that remembers patterns from previous reviews gets better. This is a lightweight form of the learning system we need. |
| **Assessment** | ✅ Sound. This is a built-in mechanism for exactly the kind of learning we want. |
| **Relevance** | 🔴 Direct — maps to our Learning & Adaptation System (Phase 7). |
| **Adopt?** | ✅ Yes — evaluate whether subagent memory can serve as the primary learning mechanism. |

---

## Category 5: Hooks & Automation

### P5.1 — Hooks for Deterministic Rules, CLAUDE.md for Advisory

| Field | Value |
|-------|-------|
| **Source** | Anthropic best practices |
| **Practice** | "Use hooks for actions that must happen every time with zero exceptions. Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." |
| **Reasoning** | CLAUDE.md is probabilistic — Claude might ignore a rule. Hooks are deterministic — they execute regardless. For must-always-happen behavior (lint after edit, validate commit message), hooks are the right tool. |
| **Assessment** | ✅ Sound. This is the key distinction. Our insights report showed that CLAUDE.md instructions about ruff weren't consistently followed, but a PostToolUse hook would eliminate the problem entirely. |
| **Relevance** | 🔴 Direct — already adopted as D14 (PostToolUse ruff hook). Extends to other deterministic behaviors. |
| **Adopt?** | ✅ Already adopted; extend to more behaviors. |

### P5.2 — PostToolUse Hook for Auto-Linting After Edits

| Field | Value |
|-------|-------|
| **Source** | Dan's insights report, Anthropic hooks docs |
| **Practice** | PostToolUse hook matching `Edit|Write` that runs `ruff check --fix && ruff format` on the affected file after every code edit. |
| **Reasoning** | #1 friction source in Dan's workflow (4+ sessions of wasted retries). Deterministic enforcement eliminates the problem entirely. |
| **Assessment** | ✅ Sound. Proven by data from Dan's actual usage. |
| **Relevance** | 🔴 Direct — already adopted as D14. |
| **Adopt?** | ✅ Already adopted |

### P5.3 — Git Guardrails Hook

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (git-guardrails-claude-code skill) |
| **Practice** | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, force push) before they execute. |
| **Reasoning** | Autonomous agents should not be able to force-push, hard-reset, or clean without human approval. These are destructive operations that can't be undone. |
| **Assessment** | ✅ Sound. Essential safety rail for autonomous operation, especially overnight Ralph Wiggum loops. |
| **Relevance** | 🔴 Direct — critical for overnight autonomous operation. |
| **Adopt?** | ✅ Yes — install Matt Pocock's skill or create equivalent. |

---

## Category 6: Codebase Architecture for Agent Effectiveness

### P6.1 — Deep Modules with Thin Interfaces

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (improve-codebase-architecture skill, TDD philosophy) |
| **Practice** | Restructure code into larger modules with thin interfaces rather than many tiny undifferentiated modules. AI navigates deep modules more easily because understanding requires reading fewer files. |
| **Reasoning** | "When an AI looks at a bad codebase, it sees many tiny, undifferentiated modules. But if you restructure it into larger modules with thin interfaces on top, the AI can navigate it much more easily." Deep modules also make test boundaries clearer. |
| **Assessment** | ✅ Sound. This is a well-established software design principle (John Ousterhout's "A Philosophy of Software Design") applied specifically to agent-navigable codebases. Good architecture helps both humans and agents. |
| **Relevance** | 🟡 Medium — applies to the structure of the cookiecutter output and any derived project. |
| **Adopt?** | ✅ Yes — include improve-codebase-architecture as an installable skill. |

---

## Category 7: Autonomous Operation (Ralph Wiggum)

### P7.1 — Max Iterations as Primary Safety, Not Completion Promise

| Field | Value |
|-------|-------|
| **Source** | Ralph Wiggum official docs, community consensus |
| **Practice** | `--max-iterations` is the primary safety mechanism. `--completion-promise` uses fragile exact string matching and cannot be changed during runtime. |
| **Reasoning** | Completion promises can be missed (wrong string, partial output, model refuses). Max iterations guarantees the loop stops. |
| **Assessment** | ✅ Sound. Deterministic safety > probabilistic signaling. |
| **Relevance** | 🔴 Direct — our Ralph Wiggum loop controller must use max-iterations as the hard stop. |
| **Adopt?** | ✅ Already adopted |

### P7.2 — Bash-Based Independent Context Per Iteration (vs. Plugin Session Persistence)

| Field | Value |
|-------|-------|
| **Source** | Community consensus (paddo.dev analysis), frankbria/ralph-claude-code |
| **Practice** | The bash-based approach (loop `claude -p` in a shell script) gives each iteration an independent context window, which may be more robust than the plugin's "run forever in one session" model for complex multi-task workflows. |
| **Reasoning** | Independent context per iteration prevents context pollution from earlier failures. The plugin's single-session model means errors accumulate in context. However, the plugin preserves session state which helps for iterative refinement. |
| **Assessment** | 🟡 Nuanced. Both approaches have tradeoffs. For single-task iteration (fix until tests pass), the plugin works well. For multi-task overnight runs (our use case), bash-based may be more robust because each task starts fresh. |
| **Relevance** | 🔴 Direct — affects whether we use the plugin directly or wrap Ralph in bash scripts. |
| **Adopt?** | 🔶 Needs testing — evaluate both approaches for our specific multi-task overnight use case. |

### P7.3 — Include "What to Do if Stuck" in Loop Prompts

| Field | Value |
|-------|-------|
| **Source** | Ralph Wiggum official docs |
| **Practice** | Include fallback instructions in the loop prompt: "After 15 iterations, if not complete: Document what's blocking progress, list what was attempted, suggest alternative approaches." |
| **Reasoning** | Without stuck-detection, the agent burns iterations on an impossible path. Explicit fallback instructions create a structured exit ramp. |
| **Assessment** | ✅ Sound. This is our "blocker creation" pattern — when stuck, document and pivot. |
| **Relevance** | 🔴 Direct |
| **Adopt?** | ✅ Yes — bake into our Ralph Wiggum prompt construction. |

---

## Category 8: Human-Agent Interaction

### P8.1 — Grill-Me Before Writing Code

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock |
| **Practice** | Before writing any code, have the agent relentlessly interview you about every aspect of the plan. Walk down each branch of the design tree, resolving dependencies between decisions one by one. For each question, the agent should provide its recommended answer. If a question can be answered by exploring the codebase, explore the codebase instead. |
| **Reasoning** | Forces the human to articulate what they actually want. Prevents misunderstanding before it becomes misimplementation. 16-50 questions per session = comprehensive coverage of edge cases and assumptions. |
| **Assessment** | ✅ Sound. Directly addresses Dan's goal of spending 90% of time in ideation. This IS the ideation mechanism. |
| **Relevance** | 🔴 Direct — core skill. Install Matt Pocock's grill-me directly. |
| **Adopt?** | ✅ Yes — install directly via `npx skills@latest add mattpocock/skills/grill-me` |

### P8.2 — Agent Should Provide Recommended Answers

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (grill-me skill: "For each question, provide your recommended answer") |
| **Practice** | When asking questions, the agent doesn't just ask — it provides its best guess at the answer. The human can accept, modify, or reject the recommendation. |
| **Reasoning** | This is more efficient than open-ended questions. The human can react to a concrete proposal faster than formulating an answer from scratch. It also reveals the agent's assumptions, which the human can correct. |
| **Assessment** | ✅ Sound. This is how experienced consultants work — they don't just ask questions, they propose answers for validation. Reduces human cognitive load. |
| **Relevance** | 🔴 Direct — applies to our confidence scoring and ideation facilitation. |
| **Adopt?** | ✅ Yes |

### P8.3 — "Be Extremely Concise. Sacrifice Grammar for Concision."

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (global CLAUDE.md directive, went viral) |
| **Practice** | Add to CLAUDE.md: "Be extremely concise. Sacrifice grammar for the sake of concision." Makes plans scannable, cheaper to output, and easier to read in a terminal. |
| **Reasoning** | Plans and explanations are often over-written. In a terminal, you read the end of the output first. Concise output means you actually read it instead of blindly accepting it. Also reduces token cost. Multiple independent analyses confirm it creates a "forcing mechanism" that paradoxically produces more informative output by eliminating filler. |
| **Assessment** | ✅ Sound. Aligns with the arxiv finding that comprehensive docs = noise. Terminal UX demands conciseness. The counter-intuitive finding (grammar sacrifice → more substance) is confirmed by independent testing. |
| **Relevance** | 🔴 Direct — add to our CLAUDE.md template. |
| **Adopt?** | ✅ Yes |

### P8.4 — Plan Mode for Everything, Then Auto-Accept Edits

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (plan mode article), Boris Cherny (tip #1) |
| **Practice** | Start with `--permission-mode plan` or `/plan`. Iterate until the plan is solid. Then switch to auto-accept edits mode. Claude executes the entire implementation in one go without back-and-forth. Also: end every plan with a numbered list of concrete steps (last thing visible in terminal). |
| **Reasoning** | Plan mode prevents the classic failure: agent makes 40 changes you didn't want. Planning forces explicitness before execution. "Most people using Claude Code are not using plan mode. They're jumping straight into execution." This is the #1 difference between effective and ineffective users. |
| **Assessment** | ✅ Sound. Separating planning from execution is a fundamental engineering principle. Boris and Matt both use this as their primary workflow. |
| **Relevance** | 🔴 Direct — our pipeline already separates planning (grill-me + PRD) from execution (Ralph loop). This confirms the architecture. |
| **Adopt?** | ✅ Yes |

---

## Category 9: Quality & Review

### P9.1 — Writer/Reviewer Pattern (Separate Contexts)

| Field | Value |
|-------|-------|
| **Source** | Anthropic best practices |
| **Practice** | Use a fresh context for code review — Claude won't be biased toward code it just wrote. Have one session write code, then a subagent (fresh context) review it. Can also apply to tests: one writes tests, another writes code to pass them. |
| **Reasoning** | Self-review is inherently biased. The same cognitive process that produced the code will overlook its own flaws. Fresh context = fresh perspective. |
| **Assessment** | ✅ Sound. This is a well-established principle in software engineering (no one reviews their own code). Subagents provide the mechanism. |
| **Relevance** | 🔴 Direct — our anti-slop LLM-as-judge gates should use subagents for unbiased review. |
| **Adopt?** | ✅ Yes |

### P9.2 — Adversarial Review with Test Generation BEFORE Fixing

| Field | Value |
|-------|-------|
| **Source** | Dan's insights report (horizon item) |
| **Practice** | During code review: (1) identify issues, (2) write failing tests for each issue BEFORE fixing anything, (3) confirm tests fail as expected, (4) fix issues one by one, running tests after each fix. |
| **Reasoning** | Writing tests for issues before fixing them creates a verification loop. If the test doesn't fail, the issue description was wrong. If the fix doesn't make the test pass, the fix is incomplete. |
| **Assessment** | ✅ Sound. This is TDD applied to code review — red-green for bug fixes. Creates verifiable evidence that the issue existed and was fixed. |
| **Relevance** | 🔴 Direct — enhances our review-code + write-tests skill interaction. |
| **Adopt?** | ✅ Yes |

### P9.3 — Give Claude a Way to Verify Its Work (2-3x Quality)

| Field | Value |
|-------|-------|
| **Source** | Boris Cherny (tip #13 — "probably the most important thing") |
| **Practice** | Always provide a verification method: tests, scripts, UI screenshots, build commands. If Claude has a feedback loop, it will 2-3x the quality of the final result. Boris uses the Chrome extension so Claude can open a browser, test UI, and iterate. |
| **Reasoning** | Without verification, Claude's output is "fire and forget." With verification, Claude can self-correct. The difference is massive — 2-3x quality improvement by Boris's measurement. |
| **Assessment** | ✅ Sound. This is the core Ralph Wiggum philosophy: let it iterate toward verified success. The 2-3x claim is from the creator of Claude Code running it daily. |
| **Relevance** | 🔴 Direct — every skill should include a verification step. Our anti-slop pipeline IS the verification loop. |
| **Adopt?** | ✅ Yes |

---

## Category 10: Boris Cherny Workflow Practices

### P10.1 — 5 Parallel Sessions in Separate Git Checkouts

| Field | Value |
|-------|-------|
| **Source** | Boris Cherny (tip #1) |
| **Practice** | Run 5+ Claude Code instances in parallel, each in a separate git checkout of the same repo. Use OS notifications to know when any Claude needs input. |
| **Reasoning** | Parallel execution multiplies throughput. Separate checkouts prevent conflicts. Notifications prevent blocking. This is essentially the "workflow architect" pattern Dan already uses. |
| **Assessment** | ✅ Sound for power users. Dan's insights report shows only 1 parallel event — this is an area for growth. |
| **Relevance** | 🟡 Medium — aspirational for our system. Our current focus is sequential overnight execution, but parallel is a future enhancement. |
| **Adopt?** | 🔶 Defer — note as Phase 2 enhancement after core system works. |

### P10.2 — PostToolUse Hook for Formatting (The Last 10%)

| Field | Value |
|-------|-------|
| **Source** | Boris Cherny (tip #9) |
| **Practice** | "Claude usually generates well-formatted code out of the box, and the hook handles the last 10% to avoid formatting errors in CI later." |
| **Reasoning** | Don't try to teach Claude to format perfectly. Let it focus on logic; let a deterministic hook handle formatting. This is the hooks-for-determinism principle applied. |
| **Assessment** | ✅ Sound. Already adopted as D14. Boris's framing ("the last 10%") is important — the hook isn't replacing Claude's formatting, it's polishing the edge cases. |
| **Relevance** | 🔴 Direct — already adopted. |
| **Adopt?** | ✅ Already adopted |

### P10.3 — Don't Use --dangerously-skip-permissions; Use /permissions Instead

| Field | Value |
|-------|-------|
| **Source** | Boris Cherny (tip #10) |
| **Practice** | Pre-allow common safe commands via `/permissions` and check them into `.claude/settings.json` shared with the team. Don't use `--dangerously-skip-permissions`. |
| **Reasoning** | Fine-grained allowlists give autonomy for safe operations while maintaining guardrails for dangerous ones. Shared via settings.json = team-wide consistency. |
| **Assessment** | ✅ Sound. Directly addresses Dan's permission pain point AND his requirement not to use --dangerously-skip-permissions. This is the solution. |
| **Relevance** | 🔴 Direct — already adopted as D13. Boris's approach (pre-allow via `/permissions`, share via settings.json) is the implementation pattern. |
| **Adopt?** | ✅ Already adopted; Boris's pattern is the implementation. |

### P10.4 — Route Permission Requests to Opus via Hook

| Field | Value |
|-------|-------|
| **Source** | Boris Cherny (team tip) |
| **Practice** | Route permission approval requests to Opus via a hook — let it scan for attacks and auto-approve safe ones. |
| **Reasoning** | Instead of blanket-allowing or blanket-blocking, use an LLM to evaluate each permission request intelligently. More sophisticated than simple allowlists. |
| **Assessment** | 🟡 Interesting but risky. Using an LLM to auto-approve permissions adds a stochastic element to a security-critical decision. For overnight autonomous runs, the risk profile matters. Consider as an enhancement after the basic allowlist approach is solid. |
| **Relevance** | 🟡 Medium — enhancement to our permission boundary checker. |
| **Adopt?** | 🔶 Evaluate — potential Phase 2 enhancement, not day-one. |

### P10.5 — Stop Hook to Verify Work at End of Turn

| Field | Value |
|-------|-------|
| **Source** | Boris Cherny (tip #12) |
| **Practice** | Use a Stop hook to nudge Claude to verify its work or continue at the end of a turn. Can prompt Claude to run verification, or use deterministically. |
| **Reasoning** | Ensures every turn ends with verification, not just a "done" claim. This is more reliable than hoping Claude remembers to verify. |
| **Assessment** | ✅ Sound. This is how Ralph Wiggum works — the Stop hook is the mechanism. But using it for verification (not just loop continuation) is a distinct application. |
| **Relevance** | 🔴 Direct — our anti-slop pipeline should include a Stop hook that triggers verification before allowing exit. |
| **Adopt?** | ✅ Yes |

### P10.6 — Update CLAUDE.md on Errors (Living Documentation)

| Field | Value |
|-------|-------|
| **Source** | Boris Cherny workflow, LobeHub boris-workflow skill |
| **Practice** | When Claude makes an error that a human corrects, update CLAUDE.md with the correction so future sessions don't repeat it. This is "living documentation" — the project learns from its mistakes. |
| **Reasoning** | Without this, every new session starts naive. With it, accumulated corrections prevent recurring errors. This is a lightweight learning system. |
| **Assessment** | ✅ Sound. This is a simpler version of our Learning System (Phase 7). The question is whether CLAUDE.md is the right place (it gets too long) vs. a separate learning store. Per the arxiv paper, CLAUDE.md should stay minimal — so learnings might belong in a separate file referenced by CLAUDE.md. |
| **Relevance** | 🔴 Direct — informs our learning system design. Store learnings in a separate file, not CLAUDE.md itself. |
| **Adopt?** | ✅ Yes — but put learnings in a separate file, not CLAUDE.md (to keep it minimal per arxiv findings). |

### P10.7 — Never Commit Directly to Main

| Field | Value |
|-------|-------|
| **Source** | Dan (explicit requirement), standard engineering practice |
| **Practice** | Agent always works on feature branches, never commits to main. PRs are the integration mechanism, gated by review (human or automated based on trust tier). |
| **Reasoning** | Main branch must always be in a deployable state. Direct commits bypass all review gates. Matt Pocock's Ralph approach of committing to main is explicitly rejected for our system. |
| **Assessment** | ✅ Sound. Standard engineering practice. No agent should have write access to main. |
| **Relevance** | 🔴 Direct — hard rule. |
| **Adopt?** | ✅ Yes — hard rule, enforced by git guardrails hook. |

---

## Category 11: Matt Pocock Skills — Direct Installation Candidates

These are Matt Pocock skills that can potentially be installed directly via `npx skills@latest add`:

| Skill | Direct Install? | Notes |
|-------|----------------|-------|
| **grill-me** | ✅ Yes | Core ideation skill. 3 sentences, incredibly impactful. |
| **write-a-prd** | ✅ Yes | PRD generation. Skips steps if grill-me already done. |
| **prd-to-plan** | 🟡 Evaluate | Turns PRD into multi-phase implementation plan using tracer-bullet vertical slices. |
| **prd-to-issues** | 🟡 Evaluate | Issues as GitHub Issues with blocking relationships — need to evaluate for our backlog format. |
| **tdd** | ✅ Likely Yes | Methodology-focused, not TypeScript-specific. Core philosophy: vertical slices, behavior not implementation, never write all tests first. Includes bundled `tests.md` and `mocking.md` reference files. |
| **ubiquitous-language** | ✅ Yes | Already adopted (D17). |
| **git-guardrails-claude-code** | ✅ Yes | Essential safety for autonomous operation. Blocks push, reset --hard, clean, force push. |
| **write-a-skill** | ✅ Yes | Meta-skill for creating new skills with proper structure + progressive disclosure. |
| **improve-codebase-architecture** | 🟡 Evaluate | Explores codebase for deep modules, testability, architectural improvements. |
| **triage-issue** | 🟡 Evaluate | Bug investigation + TDD fix plan → GitHub issue. Maps to our diagnose-failure skill. |
| **request-refactor-plan** | 🟡 Evaluate | Refactor plans with tiny commits via user interview → GitHub issue. |
| **design-an-interface** | 🟢 Lower priority | Parallel sub-agents for interface design — interesting but not core. |
| **setup-pre-commit** | ❌ Skip | TypeScript-specific (Husky + Prettier). We have our own Python pre-commit config from NCAA eval. |
| **migrate-to-shoehorn** | ❌ Skip | TypeScript-specific migration tool. |
| **scaffold-exercises** | ❌ Skip | Course-content-specific. |

## Category 12: Related Frameworks — obra/superpowers

**Discovery:** obra/superpowers is a comprehensive agentic skills framework that auto-triggers skills across the entire development lifecycle: brainstorming → git worktrees → writing plans → TDD → code review → branch finishing. It includes systematic debugging, verification-before-completion, and subagent-driven-development patterns.

| Aspect | Assessment |
|--------|-----------|
| **Philosophy** | "Mandatory workflows, not suggestions" — skills trigger automatically based on task type. |
| **Key innovation** | Writing-skills skill that applies TDD methodology to creating skills themselves (RED-GREEN-REFACTOR for process documentation). |
| **Subagent-driven development** | Tasks dispatched to subagents with two-stage review (spec compliance, then code quality). |
| **Adopt?** | 🟡 Evaluate — the framework is opinionated and comprehensive. Some patterns (auto-triggering, subagent dispatch) are exactly what we want. Others might conflict with our architecture. Worth a deep evaluation during Phase 1. |

---

## Conflict/Complement Map (Preliminary)

> **Full analysis** with category taxonomy (7 themes), 10 complement clusters, 8 tensions, and 3-tier reasoning audit available in `phase0-analysis.md`.

### Complements (practices that reinforce each other)

- P1.1 (pipeline) + P3.1 (TDD) + P7.3 (stuck detection) = complete autonomous execution architecture
- P4.1 (minimal CLAUDE.md) + P2.1 (short skills) + P5.1 (hooks for determinism) + P8.3 (sacrifice grammar) = lean, effective context management
- P8.1 (grill-me) + P8.4 (plan mode) + P1.2 (vertical slices) + P3.3 (objective criteria) = well-specified work that agents can execute reliably
- P4.3 (subagents) + P9.1 (writer/reviewer) = unbiased quality gates
- P4.4 (subagent memory) + P10.6 (update docs on errors) + our learning system = continuous improvement
- P9.3 (verify work = 2-3x quality) + P10.5 (Stop hook for verification) + P3.1 (TDD) = verification at every level
- P10.3 (permissions not --dangerously-skip) + P5.3 (git guardrails) + P10.7 (never commit to main) = safe autonomous operation
- **P16.1 (specification bottleneck) + P8.1 (grill-me) + P16.9 (clear ≠ complete) + P16.5 (externalize tacit knowledge)** = the entire ideation/specification pipeline justified from first principles
- **P16.4 (the 17% that looks right) + P9.3 (verification = 2-3x) + P16.6 (AI for evaluation not just generation)** = anti-slop pipeline justified from first principles
- **P16.3 (domain memory transforms behavior) + P4.4 (subagent memory) + P10.6 (living docs)** = learning system justified as a structural necessity, not a nice-to-have
- **P16.2 (supervision not prompting) + P16.8 (task queues replace chat)** = our entire architecture (backlog + overnight loops + trust tiers) as a supervision system
- **P16.11 (harness > model, 78% vs 42%) + P16.12 (bottleneck = cognitive architecture) + P16.13 (skills externalize expertise)** = the cookiecutter's fundamental value proposition: we're building the harness that makes the human a better fleet commander
- **P16.14 (memory as shared surface) + P4.4 (subagent memory) + P10.6 (living docs) + D33 (markdown learning store)** = learning system as human-readable shared surface, not hidden database
- **P16.15 (expand ambition not cut headcount) + D32 (trust tiers route attention)** = trust tiers free human time for high-leverage work, not eliminate human involvement
- **P21.4 (AutoResearch self-improving skills) + D27 (recurring learnings → deterministic gates) + P16.7 (compounding gap)** = the complete compounding loop: skills auto-improve via evals, learnings graduate to gates, the system gets better every day without manual intervention
- **P21.1 (context rot) + D35 (land the plane) + D37 (context rotation in Ralph loops)** = context management as a first-class engineering concern in autonomous loops, not an afterthought
- **P17.2 (two-stage review) + P9.1 (writer/reviewer) + P16.4 (the 17% that looks right)** = multi-layer anti-slop: deterministic gates catch obvious issues, spec compliance review catches requirement drift, code quality review catches taste issues

### Tensions (practices that need reconciliation)

- **Ralph Wiggum plugin vs. bash loop** (P7.2): Deferred to Phase 1 architecture decision. Need to evaluate both for our multi-task overnight use case.
- **GitHub Issues vs. local file-based backlog**: Deferred to Phase 1 architecture decision. Matt uses GitHub Issues, Rich uses local JSON. Both have merits.
- **CLAUDE.md learning updates (P10.6) vs. minimal CLAUDE.md (P4.1)**: Resolution: store learnings in a separate file referenced by CLAUDE.md with one line, not in CLAUDE.md itself. CLAUDE.md stays minimal; learnings file can grow.
- **Matt Pocock's Ralph commits to main vs. our branch-based workflow (P10.7)**: Resolved — our system always works on branches. This is a hard rule. Git guardrails hook enforces it.

---

## Category 13: Karpathy — Agentic Engineering Philosophy

### P13.1 — Vibe Coding → Agentic Engineering (Role Shift)

| Field | Value |
|-------|-------|
| **Source** | Andrej Karpathy (Feb 2026 retrospective) |
| **Practice** | "You are not writing the code directly 99% of the time… you are orchestrating agents who do and acting as oversight." The shift is from writing code to orchestrating, testing, and maintaining oversight. |
| **Reasoning** | LLMs are now capable enough for professional use, but only with "more oversight and scrutiny." The leverage comes from agents doing the mechanical work while humans provide taste, judgment, and architectural thinking. |
| **Assessment** | ✅ Sound. This is exactly our architecture — Dan as workflow architect, agents as executors, anti-slop pipeline as the oversight layer. |
| **Relevance** | 🔴 Direct — philosophical validation of the entire project. |
| **Adopt?** | ✅ Already the premise of the project. |

### P13.2 — The "Taste Problem" (Where AI Falls Short)

| Field | Value |
|-------|-------|
| **Source** | Karpathy |
| **Practice** | AI writes functional code but makes bad aesthetic/architectural choices. Code quality = functional correctness + "taste" (abstractions, naming, structure, when to split/merge). Humans must supply taste. |
| **Reasoning** | LLMs optimize for "works" not "elegant." They don't inherently value simplicity, consistency, or maintainability unless specifically instructed. |
| **Assessment** | ✅ Sound. This is exactly what our stochastic (LLM-as-judge) anti-slop gates are for — catching functional-but-tasteless code that deterministic gates (lint, type check, tests) can't catch. |
| **Relevance** | 🔴 Direct — justifies the stochastic anti-slop gate layer. |
| **Adopt?** | ✅ Already incorporated into anti-slop pipeline design. |

### P13.3 — Multi-Layer Tool Specialization

| Field | Value |
|-------|-------|
| **Source** | Karpathy |
| **Practice** | Don't force one tool to do everything. Tab completion (75% of work) → targeted code mods → Claude Code for substantial features → strongest model for hardest problems. Different tools for different task sizes. |
| **Reasoning** | Each layer of tooling has a sweet spot. Using a heavy agent for a one-line change wastes context and time. Using tab completion for a multi-file refactor misses critical context. |
| **Assessment** | ✅ Sound. For our system: not every backlog item needs a full Ralph Wiggum loop. Small fixes might just need a single `claude -p` command. |
| **Relevance** | 🟡 Medium — our system should right-size the execution approach to the task complexity. |
| **Adopt?** | ✅ Yes — trust tier could also inform execution approach (simple task → single command, complex task → full loop). |

---

## Category 14: BMAD — Patterns to Adopt and Discard

### P14.1 — Story Files as Primary Handoff Mechanism (Adopt)

| Field | Value |
|-------|-------|
| **Source** | BMAD (used by Dan in NCAA eval) |
| **Practice** | Hyper-detailed story files contain everything the dev agent needs — full context, implementation details, acceptance criteria, architectural guidance. The SM agent creates the story; the dev agent consumes it. |
| **Reasoning** | Eliminates context loss between planning and execution. The dev agent "opens a story file with complete understanding of what to build, how to build it, and why." |
| **Assessment** | ✅ Sound. Dan's NCAA eval project used this extensively and it worked well. The key insight is that story files ARE the context bridge across session boundaries. |
| **Relevance** | 🔴 Direct — this is how our backlog items should be structured. |
| **Adopt?** | ✅ Yes — adapt for our skill-based architecture. |

### P14.2 — 4-Phase Lifecycle with Right-Sizing (Adopt Pattern, Discard Weight)

| Field | Value |
|-------|-------|
| **Source** | BMAD |
| **Practice** | Analysis → Planning → Solutioning → Implementation. Projects sized by level (L0: single atomic change, L1: small feature, L2: medium, L3: complex integration). Lower levels skip phases. |
| **Reasoning** | Not every task needs a full PRD + architecture doc. Right-sizing prevents ceremony overhead on simple tasks while ensuring complex tasks get adequate planning. |
| **Assessment** | ✅ Sound principle, but BMAD's implementation is too heavy (9 agents, 15 workflow commands). Matt Pocock achieves similar with 5 skills. |
| **Relevance** | 🔴 Direct — adopt the right-sizing principle, implement with lighter tooling. |
| **Adopt?** | 🟡 Adopt principle, not implementation. |

### P14.3 — Heavy Persona/Role System (Discard)

| Field | Value |
|-------|-------|
| **Source** | BMAD |
| **Practice** | 12+ specialized agent personas (Analyst, PM, Architect, SM, Developer, UX, QA, etc.) each with distinct personalities and prompts. |
| **Reasoning** | Specialized personas bring domain expertise to each phase. |
| **Assessment** | ❌ Over-engineered. Boris Cherny's team found removing persona overhead improved performance. The aj-geddes Claude Code port achieved 70-85% token optimization by going functional over persona-based. Dan's insights report showed the SM persona breaking (Claude wrote code instead of staying in character). Skills with clear instructions > personas with role-play. |
| **Relevance** | 🔴 Direct — informed by Dan's explicit pain point (agent broke persona). |
| **Adopt?** | ❌ No — use skills with clear instructions instead of personas. |

### P14.4 — Adversarial Code Review Workflow (Adopt)

| Field | Value |
|-------|-------|
| **Source** | BMAD, Dan's NCAA eval |
| **Practice** | Structured adversarial code review finding 3-10 specific issues per session. Review follows a checklist, finds issues, fixes them, runs tests, creates PR. |
| **Reasoning** | Adversarial framing ("find issues, don't just approve") produces higher-quality reviews. Dan's 86% fully-achieved rate with this workflow proves it works. |
| **Assessment** | ✅ Sound. Dan's insights data confirms this is his most-used workflow (24 sessions). |
| **Relevance** | 🔴 Direct — already partially adopted. |
| **Adopt?** | ✅ Yes — implement as subagent-based review skill (writer/reviewer pattern from Anthropic). |

---

## Category 15: Anthropic — Broader Organizational Practices

### P15.1 — Use Opus for Planning, Sonnet for Code Execution

| Field | Value |
|-------|-------|
| **Source** | Boris Cherny (Anthropic internal practice) |
| **Practice** | Use /model to select different models for different phases. Opus for plan mode (deeper reasoning needed). Sonnet for code generation (faster, cheaper, good enough for execution). |
| **Reasoning** | Different phases have different reasoning requirements. Planning needs deep thinking (Opus). Code generation following a solid plan needs speed (Sonnet). |
| **Assessment** | ✅ Sound. Practical cost and speed optimization without sacrificing quality where it matters. |
| **Relevance** | 🟡 Medium — useful optimization but not critical for v1 of our system. |
| **Adopt?** | 🔶 Defer — note as optimization for after core system works. |

### P15.2 — Glob+Grep Outperforms RAG for Codebase Search

| Field | Value |
|-------|-------|
| **Source** | Boris Cherny (Pragmatic Engineer podcast) |
| **Practice** | Claude Code's "agentic search" is just glob and grep, driven by the model. Anthropic tried vector databases, recursive model-based indexing, and other approaches. Plain glob and grep beat everything. |
| **Reasoning** | RAG adds complexity (stale indexes, permission issues, embedding drift). The model is smart enough to formulate good grep queries and navigate results. Inspired by how engineers at Instagram searched code when IDE tooling was broken. |
| **Assessment** | ✅ Sound. Simplicity wins. Don't over-engineer the search layer. This aligns with our "library-first" principle — use what's already built in rather than adding complexity. |
| **Relevance** | 🟡 Medium — confirms we should NOT build custom search infrastructure for the cookiecutter. Let Claude Code's built-in search do its job. |
| **Adopt?** | ✅ Yes — don't build custom codebase search. |

### P15.3 — Automate Recurring Review Comments into Lint Rules

| Field | Value |
|-------|-------|
| **Source** | Boris Cherny (Pragmatic Engineer podcast — his Meta practice) |
| **Practice** | Every time you leave the same kind of review comment 3-4 times, write a lint rule to automate it away. |
| **Reasoning** | Humans shouldn't catch the same class of error manually every time. If it's a pattern, make it deterministic. This is the "hooks for determinism" principle applied to code review. |
| **Assessment** | ✅ Sound. This is how our learning system should feed back into the anti-slop pipeline — learnings about recurring issues become new deterministic gates. |
| **Relevance** | 🔴 Direct — informs the learning system → anti-slop pipeline feedback loop. |
| **Adopt?** | ✅ Yes |

---

## Category 16: Nate B. Jones — Philosophical Frameworks for System Design

> Source: 27 episodes identified by Dan, researched via Acast descriptions, YouTube transcript archive, summary articles, and AnswerRocket podcast breakdown. Jones operates at a higher abstraction layer than Pocock/Cherny — he's less "here's my .claude/settings.json" and more "here's why your entire approach to AI is structurally wrong." These frameworks should serve as design evaluation criteria for our system.

### P16.1 — The 97.5% Failure Rate: The Fix Isn't Coding, It's Specification

| Field | Value |
|-------|-------|
| **Source** | "Your AI Agent Fails 97.5% of Real Work. The Fix Isn't Coding." |
| **Practice** | Most agent failures aren't model failures — they're specification failures. Teams can't articulate what "done" looks like, so agents produce confident nonsense. The specification bottleneck is the real constraint, not model capability. |
| **Reasoning** | AI dropped execution cost to near-zero, but that amplifies bad specs. Every vague instruction gets amplified into confident garbage. The fix: define concrete, testable quality criteria for every output. If you can't verify it, you can't trust it. |
| **Assessment** | ✅ Sound. This is the deepest justification for our grill-me → PRD → objective acceptance criteria pipeline. The entire front end of our system exists to solve the specification problem BEFORE execution begins. |
| **Relevance** | 🔴 Direct — foundational design principle. Our system's value proposition IS solving the specification bottleneck. |
| **Adopt?** | ✅ Yes — elevate to a core principle: "The system exists to make specifications precise enough that autonomous execution is reliable." |

### P16.2 — The Supervision Problem, Not the Prompting Problem

| Field | Value |
|-------|-------|
| **Source** | Acast episode on vibe coders scaling, multiple episodes |
| **Practice** | "Agents introduce a supervision problem, not just a prompting one." Better prompting alone doesn't solve agent failures. You need: version control as safety habit, scoped tasks to avoid context overflow, standing orders (persistent rules files) over repeated prompting, and small bets over sweeping changes. |
| **Reasoning** | Agents are "powerful but unsupervised contractors." Without save points, scoped tasks, and persistent rules, you're one bad session away from losing production work. The Claude Code data deletion incident proves this. |
| **Assessment** | ✅ Sound. This frames our entire anti-slop + trust tier + git guardrails architecture. We're not building a better prompter — we're building a supervision system. |
| **Relevance** | 🔴 Direct — reframes the project purpose. |
| **Adopt?** | ✅ Yes — adopt as a framing principle. |

### P16.3 — Domain Memory Transforms Agent Behavior

| Field | Value |
|-------|-------|
| **Source** | "AI Agents That Actually Work: The Pattern Anthropic Just Revealed", Acast episode on Anthropic's agent patterns |
| **Practice** | "Generalized agents without domain memory spiral into chaotic loops instead of making durable progress." Domain memory transforms agent behavior from reactive task-running to structured, compounding work. The initializer + coding agent pattern works because it provides the context the agent needs BEFORE it starts coding. |
| **Reasoning** | Agents are amnesiacs with tool belts. The harness design (domain memory + testing loops) matters more than model intelligence. The competitive advantage is "well-designed domain memory and the discipline to build testing loops that hold it accountable." |
| **Assessment** | ✅ Sound. This is the strongest argument for our UBIQUITOUS_LANGUAGE.md, learning system, and CLAUDE.md strategy. These aren't nice-to-haves — they're the domain memory that prevents chaotic loops. |
| **Relevance** | 🔴 Direct — validates our entire Phase 7 (Learning System) and the architectural decision to persist context across sessions. |
| **Adopt?** | ✅ Yes — domain memory is a first-class architectural concern, not an afterthought. |

### P16.4 — Stop Accepting Output That "Looks Right" — The Other 17%

| Field | Value |
|-------|-------|
| **Source** | "Stop accepting AI output that 'looks right.' The other 17% is everything and nobody is ready for it." |
| **Practice** | AI output passes a "looks right" test 83% of the time. The remaining 17% contains the errors that destroy trust, create bugs, and compound into systemic quality problems. Teams must build evaluation systems that catch the 17%, not celebrate the 83%. |
| **Reasoning** | The "looks right" trap is exactly why Dan defaulted to over-trusting — the mental energy to distinguish good from "looks right" was too high. The fix isn't more vigilance; it's automated evaluation systems that verify the 17%. |
| **Assessment** | ✅ Sound. This is the most precise articulation of why our anti-slop pipeline exists. Every gate in the pipeline is designed to catch part of the 17% that "looks right" but isn't. |
| **Relevance** | 🔴 Direct — Dan's pain point ("I have defaulted to just trusting it more than I should") is literally this problem. |
| **Adopt?** | ✅ Yes — the anti-slop pipeline IS the answer to the 17% problem. |

### P16.5 — AI Slop Is a Specification Failure, Not a Model Failure

| Field | Value |
|-------|-------|
| **Source** | "90% of AI Users Are Getting Mediocre Output", newsdefused.com summary |
| **Practice** | AI slop is drowning organizations because they haven't externalized their tacit knowledge — the unspoken expectations in people's heads. Once those expectations are written as rules or prompts, AI can work with them. If they aren't, you get generic filler. Jones's framework: every document must serve a goal, every decision must have a name, every action item an owner, every open question a next step. |
| **Reasoning** | The specification bottleneck is the core problem. AI forces teams to externalize tacit knowledge. Teams that don't get "corporate oatmeal" output. Teams that do get precision. |
| **Assessment** | ✅ Sound. This validates our ubiquitous language approach (externalizing domain knowledge), our design requirements with traceability (externalizing acceptance criteria), and our learning system (externalizing tacit operational knowledge). |
| **Relevance** | 🔴 Direct — the cookiecutter exists to externalize tacit knowledge into structures AI can work with. |
| **Adopt?** | ✅ Yes — add "externalize tacit knowledge" as a core principle. |

### P16.6 — Use AI for Evaluation, Not Just Generation

| Field | Value |
|-------|-------|
| **Source** | "90% of AI Users Are Getting Mediocre Output", multiple episodes |
| **Practice** | "Almost no one's checking [AI output]. Most organisations have embraced AI for writing but ignored its potential for evaluation." Use AI to run first-pass evaluations based on explicit quality checks before human review. Teach AI with examples of failure, not just success. |
| **Reasoning** | Generation without evaluation = slop factory. Every output should go through evaluation with testable criteria before it reaches a human. Including examples of BAD output helps the evaluator recognize failure patterns. |
| **Assessment** | ✅ Sound. This is our LLM-as-judge stochastic gates. But Jones adds a nuance: teach the judge with failure examples, not just success criteria. Our anti-slop gates should include "what bad looks like" alongside "what good looks like." |
| **Relevance** | 🔴 Direct — enhances our anti-slop gate design. Rubrics should include anti-patterns, not just patterns. |
| **Adopt?** | ✅ Yes — anti-slop rubrics must include failure examples. |

### P16.7 — The Compounding Gap and Identity Shift

| Field | Value |
|-------|-------|
| **Source** | "The Compounding Gap That Makes 2026 the Last Chance to Catch Up", "The Builders Who Figure This Out First Will Be Impossible to Catch" |
| **Practice** | AI advantages compound. Teams that close the capability gap first gain an edge that grows daily. But the shift requires an identity change — from "person who writes code" to "person who orchestrates agents and makes judgment calls." The skill gap is about specification, review, and orchestration, not coding. |
| **Reasoning** | Compounding works both directions. Teams that build good agent workflows improve faster (agents learn, systems get refined, trust calibrates). Teams that don't fall further behind every day. |
| **Assessment** | ✅ Sound. This is why the learning system (Phase 7) is critical — it's the compounding mechanism. Every learning makes the system better; every improvement makes the next task faster. |
| **Relevance** | 🟡 Medium — strategic framing rather than specific practice. But it justifies investing heavily in the learning system. |
| **Adopt?** | ✅ Yes — the learning system is how we compound. |

### P16.8 — Task Queues Replace Chat Interfaces

| Field | Value |
|-------|-------|
| **Source** | "Task Queues Are Replacing Chat Interfaces. Here's Why (plus a Claude Cowork Demo)" |
| **Practice** | The interaction model is shifting from chat (synchronous, human-paced) to task queues (asynchronous, agent-paced). You queue work, agents process it, you review results. This is fundamentally different from conversational AI. |
| **Reasoning** | Chat requires the human to be present. Task queues let the human define work and walk away — exactly the overnight Ralph Wiggum loop pattern. The queue IS the interface, not the chat. |
| **Assessment** | ✅ Sound. This validates our backlog-as-primary-interface design. Dan's workflow is already queue-based (insights report: 2.4 messages per session, fire and forget). Our system formalizes this. |
| **Relevance** | 🔴 Direct — the backlog IS the task queue. |
| **Adopt?** | ✅ Already the architecture. |

### P16.9 — "Clear Specs Produce Broken Output" — The Paradox

| Field | Value |
|-------|-------|
| **Source** | "The Skill That Separates AI Power Users From Everyone Else (Why 'Clear' Specs Produce Broken Output)" |
| **Practice** | Clarity isn't the same as completeness. A spec can be perfectly clear but miss critical context, edge cases, or constraints. The skill that separates power users is the ability to anticipate what the AI will misunderstand — to think about the spec from the AI's perspective, not the human's. |
| **Reasoning** | Humans fill gaps with common sense. AI fills gaps with statistical patterns. A "clear" spec that relies on implicit human knowledge will produce output that "looks right" but breaks in edge cases. Power users write specs that make the implicit explicit. |
| **Assessment** | ✅ Sound. This is why grill-me works — the interrogation process forces implicit assumptions to become explicit. It's also why our ubiquitous language matters — it makes domain-specific meaning explicit rather than leaving it to statistical inference. |
| **Relevance** | 🔴 Direct — validates grill-me, ubiquitous language, and the entire front-end ideation pipeline. |
| **Adopt?** | ✅ Yes — "make the implicit explicit" as a design principle. |

### P16.10 — Simulation Wins Over Direct Execution

| Field | Value |
|-------|-------|
| **Source** | "We're Getting AI Agents Backwards—Simulation Wins" |
| **Practice** | We're deploying agents at their most underleveraged point — direct execution. The real power is simulation: having agents explore multiple approaches, model outcomes, and identify risks BEFORE committing to execution. |
| **Reasoning** | Direct execution is a single path. Simulation explores the decision tree. An agent that simulates 5 approaches and picks the best one will outperform an agent that executes the first approach that seems reasonable. |
| **Assessment** | ✅ Sound. This is a more sophisticated version of plan mode. Our system could use this: during planning, have the agent simulate multiple implementation approaches (via subagents?) and evaluate tradeoffs before committing. |
| **Relevance** | 🟡 Medium — aspirational enhancement. Core system works without it, but this could significantly improve plan quality. |
| **Adopt?** | 🔶 Defer to Phase 2 — note as enhancement. The design-an-interface skill from Matt Pocock (parallel subagents generating radically different designs) is one implementation of this pattern. |

### P16.11 — The Harness Matters More Than the Model (78% vs 42%)

| Field | Value |
|-------|-------|
| **Source** | "Claude Code vs Codex: The Decision That Compounds Every Week You Delay" |
| **Practice** | "The model is the least important part. The harness is everything else: where the AI runs, what it remembers between sessions, which tools it can touch, how it manages multiple tasks, and how deep your dependency grows every week you build around it." The same Claude model scored 78% vs. 42% on identical benchmarks depending on the harness. |
| **Reasoning** | Claude Code and Codex embody opposite philosophies: Claude Code works in your environment with full access and builds up memory over time. Codex works in a sealed room with a copy of your code and slides finished results under the door. The choice compounds — switching later is harder than most people think. |
| **Assessment** | ✅ Sound. This is the single strongest external validation of our entire project. We're not picking a model — we're building the harness. The cookiecutter IS the harness. Skills, hooks, permissions, memory, backlog management, anti-slop gates — that's all harness, not model. |
| **Relevance** | 🔴 Direct — foundational validation. Our project is literally building a harness. |
| **Adopt?** | ✅ Already the premise. Elevate to a core principle. |

### P16.12 — The Bottleneck Moved from Capability to Cognitive Architecture

| Field | Value |
|-------|-------|
| **Source** | "THIS is Why You're Still Slow Even With AI (The Bottleneck Moved)" |
| **Practice** | "The constraint is how much I can concurrently think sensibly about." The bottleneck moved from capability to cognitive architecture. The shift requires an identity change — from "engineer who writes code" to "fleet commander." Two key distinctions: patterns you can delegate vs. taste you cannot; starting before you're ready produces better output than waiting for perfect specs. |
| **Reasoning** | Raw ability to build is no longer the limitation. Steve Yegge runs 10-20 parallel Claude Code instances. The bottleneck is keeping them fed with well-specified work, reviewing their output, and maintaining coherent taste across parallel streams. |
| **Assessment** | ✅ Sound. This reframes our entire system's value proposition. The cookiecutter doesn't make the agent smarter — it makes the HUMAN more effective at the fleet commander role by handling the supervision infrastructure (backlog, trust tiers, anti-slop, learning) so the human can focus on specification and taste. |
| **Relevance** | 🔴 Direct — the system exists to solve the cognitive architecture problem, not the capability problem. |
| **Adopt?** | ✅ Yes — the system's value prop is making the human a better fleet commander. |

### P16.13 — Skills as Externalized Expertise ("Knowledge Has a Home Now")

| Field | Value |
|-------|-------|
| **Source** | "NEW: Claude's 'Super Prompts' Will Save You DAYS of Work" |
| **Practice** | Skills are how you externalize trapped expertise — insights about how to evaluate vendors, structure financial models, build pitch decks. "That knowledge has been trapped in your head because it was too complex to turn into prompts. Now it has a home." Skills work across platforms (Claude, ChatGPT, Gemini) because they're just markdown files. |
| **Reasoning** | Complex expertise that took years to develop can't fit in a single prompt. Skills package that expertise into reusable, sharable, versionable artifacts. The portability across AI platforms is a bonus — it means your expertise isn't locked to one vendor. |
| **Assessment** | ✅ Sound. This is the strongest argument for our skill-based architecture over BMAD's persona-based approach. Skills externalize expertise. Personas externalize personality. Expertise compounds; personality is overhead. |
| **Relevance** | 🔴 Direct — validates skills as the primary architecture, not personas. |
| **Adopt?** | ✅ Already adopted. |

### P16.14 — Memory Should Be Tool-Agnostic and Portable (Open Brain)

| Field | Value |
|-------|-------|
| **Source** | "One Simple System Gave All My AI Tools a Memory. Here's How." |
| **Practice** | Build a shared memory layer (Postgres + vector search) accessible via MCP to ALL AI tools. The table becomes a shared surface that both human and agent can see. Memory shouldn't be locked into one AI platform. |
| **Reasoning** | Each AI tool maintains isolated memory — Claude doesn't know what you told ChatGPT. Open Brain creates a single source of truth accessible from any MCP-compatible tool. The human gets dashboards; the agents get semantic search. |
| **Assessment** | 🟡 Interesting but possibly over-engineered for our specific use case. Our system is Claude Code-native (D6), so cross-tool memory is less critical. However, the principle of "memory as shared surface between human and agent" is valuable — our learning store should be human-readable (markdown files, not hidden databases) so both Dan and the agent can reference it. |
| **Relevance** | 🟡 Medium — the principle matters more than the specific implementation. |
| **Adopt?** | 🔶 Adopt the principle (memory as shared surface), not the implementation (Postgres + MCP). Our learning store in markdown files already satisfies this — both human and agent can read/write them. |

### P16.15 — Expanding Ambition, Not Cutting Headcount

| Field | Value |
|-------|-------|
| **Source** | "AI Made Every Company 10x More Productive. The Ones Cutting Headcount Are Telling on Themselves." |
| **Practice** | The right response to 10x productivity isn't reducing human involvement — it's expanding ambition. More experiments, faster iteration, higher quality bar. The human becomes higher-leverage, not less necessary. |
| **Reasoning** | Cutting headcount captures a one-time savings. Expanding ambition captures compounding returns. The human's role shifts from execution to specification, review, and judgment — all higher-value activities. |
| **Assessment** | ✅ Sound. This reframes our trust tier design (Q5). The goal isn't "reduce human review to zero" — it's "make every minute of human review count." Auto-merge trivial PRs so the human spends their time on architecture decisions, not lint fixes. |
| **Relevance** | 🟡 Medium — philosophical but informs trust tier design. |
| **Adopt?** | ✅ Yes — trust tiers should route human attention to high-value review, not eliminate review. |

### P16.16 — Claude Opus 4.6: Adaptive Reasoning and Agent Teams

| Field | Value |
|-------|-------|
| **Source** | "Claude Opus 4.6: The Biggest AI Jump I've Covered. Here's What You Need to Know." |
| **Practice** | Opus 4.6 introduces adaptive reasoning depth (reads contextual clues to decide how hard to think), Agent Teams (parallel coding agents), 1M token context window, and context compaction during long-running tasks. The /effort parameter lets you manually control the quality-speed-cost tradeoff. |
| **Reasoning** | Adaptive reasoning means the model self-adjusts instead of requiring the human to choose between "fast" and "thorough." Agent Teams enable the parallel execution Boris Cherny already does manually with 5 terminal tabs. Context compaction prevents the context window from filling up during Ralph Wiggum loops. |
| **Assessment** | ✅ Sound. These capabilities directly support our architecture: Agent Teams for writer/reviewer patterns, adaptive reasoning for right-sizing execution, context compaction for overnight loops. |
| **Relevance** | 🔴 Direct — these are the capabilities our system is built on top of. |
| **Adopt?** | ✅ Yes — leverage Agent Teams for subagent-based review, /effort for right-sizing. |

---

# TIER 2 SOURCES

> Tier 2 sources were evaluated for novel practices beyond what Tier 1 already covers. Sources that primarily reinforce Tier 1 findings without adding new actionable practices are noted but not given full practice entries.

## Category 17: Obra/Superpowers — Mandatory Workflow Enforcement

> 94K+ GitHub stars. The most directly comparable framework to what we're building. Created by Jesse Vincent (obra). Key philosophical difference from our approach: Superpowers enforces workflow through auto-triggering skills that intercept agent behavior. Our approach enforces workflow through hooks + anti-slop gates.

### P17.1 — Mandatory Workflows, Not Suggestions

| Field | Value |
|-------|-------|
| **Source** | obra/superpowers |
| **Practice** | Skills auto-trigger based on context — they're not optional. When Claude detects you're building something, the brainstorming skill fires before any code is written. "If code appears before tests, Superpowers deletes it." This is enforcement, not advice. |
| **Reasoning** | Advisory instructions get ignored under pressure. Deterministic enforcement doesn't. Same reasoning as Boris Cherny's "hooks for determinism, CLAUDE.md for advisory." |
| **Assessment** | ✅ Sound. This validates our hook-based enforcement approach. Our PostToolUse hook for ruff, Stop hook for verification, and git guardrails are all mandatory enforcement — the same philosophy Superpowers implements through skill auto-triggering. |
| **Relevance** | 🔴 Direct — validates our enforcement approach. |
| **Adopt?** | ✅ Already adopted via hooks. Consider: should we also auto-trigger skills? |

### P17.2 — Two-Stage Subagent Review (Spec Compliance, Then Code Quality)

| Field | Value |
|-------|-------|
| **Source** | obra/superpowers |
| **Practice** | Code review happens in two phases via subagents: first check spec compliance (did it build what was asked?), then check code quality (is the implementation good?). Critical review issues block the merge. |
| **Reasoning** | Single-pass review conflates two different failure modes. Code can be well-written but not match the spec, or match the spec but be poorly written. Separating the checks improves catch rate for both. |
| **Assessment** | ✅ Sound. This refines our writer/reviewer anti-slop pattern. Two-stage review is better than single-stage. |
| **Relevance** | 🔴 Direct — enhances our anti-slop pipeline design. |
| **Adopt?** | ✅ Yes — implement two-stage review (spec compliance + code quality). |

### P17.3 — Git Worktree Isolation for Parallel Work

| Field | Value |
|-------|-------|
| **Source** | obra/superpowers, Steve Yegge/Gas Town |
| **Practice** | Each parallel agent works in its own git worktree, not a branch in the same checkout. Worktree isolation prevents agents from stepping on each other's files. Superpowers requires worktree setup before implementation begins. |
| **Reasoning** | Multiple agents working in the same directory create race conditions and merge conflicts. Worktrees give each agent a clean filesystem view while sharing the same git history. |
| **Assessment** | ✅ Sound for multi-agent workflows. Less critical for our current single-agent Ralph loops, but becomes essential if we adopt Agent Teams or parallel execution. |
| **Relevance** | 🟡 Medium — future enhancement for parallel execution. |
| **Adopt?** | 🔶 Defer — note for when we implement parallel agent execution. |

### P17.4 — Systematic 4-Phase Debugging

| Field | Value |
|-------|-------|
| **Source** | obra/superpowers |
| **Practice** | Debugging follows a mandatory 4-phase process: root cause tracing, defense-in-depth validation, condition-based waiting, and verification before marking complete. Not "try random fixes until tests pass." |
| **Reasoning** | Agents default to surface-level fixes (change the line that errors). Systematic debugging forces deeper analysis that prevents the same bug class from recurring. |
| **Assessment** | ✅ Sound. This is a skill we should adopt — structured debugging as an anti-slop measure for bug fixes. |
| **Relevance** | 🟡 Medium — a skill to include in the cookiecutter. |
| **Adopt?** | ✅ Yes — include as a debugging skill. |

---

## Category 18: Steve Yegge/Gas Town — Multi-Agent Orchestration Patterns

> Stage 8 tooling. Aspirational for our system but patterns are relevant. Key insight: "design becomes the bottleneck when execution is cheap."

### P18.1 — The "50 First Dates" Problem and Beads

| Field | Value |
|-------|-------|
| **Source** | Steve Yegge, Gas Town |
| **Practice** | Agents have no memory between sessions and create "conflicting swamps of markdown files." Beads solves this with git-backed structured issue tracking (JSONL in git, SQLite cache, hash-based IDs designed to prevent merge conflicts). The "land the plane" pattern: agents clean up state at session end and generate ready-to-paste prompts for the next session. |
| **Reasoning** | Session boundaries are the hardest problem in autonomous agent workflows. Without structured state persistence, each session starts from zero or inherits a mess. |
| **Assessment** | ✅ Sound. Our story files (from BMAD, D25) serve a similar purpose — structured handoff between sessions. The "land the plane" pattern is something we should adopt: at the end of each Ralph loop iteration, the agent should summarize what it did and what's left. |
| **Relevance** | 🟡 Medium — our story files + learning store serve this purpose, but the "land the plane" pattern is a specific enhancement. |
| **Adopt?** | ✅ Adopt "land the plane" pattern — end-of-session state cleanup and handoff. |

### P18.2 — Design Becomes the Bottleneck When Execution Is Cheap

| Field | Value |
|-------|-------|
| **Source** | Steve Yegge, Gas Town |
| **Practice** | "Gas Town churns through implementation plans so quickly that you have to do a LOT of design and planning to keep the engine fed." When execution is nearly free, design quality becomes the constraint. |
| **Reasoning** | This is P16.1 (specification bottleneck) and P16.12 (cognitive architecture bottleneck) from a different angle. Yegge observes it at scale (20-30 agents); Jones observes it philosophically. Same conclusion: the hard part is deciding WHAT to build, not building it. |
| **Assessment** | ✅ Sound. Reinforces our grill-me → PRD → spec pipeline as the highest-leverage part of the system. |
| **Relevance** | 🔴 Direct — validates investment in ideation/specification pipeline. |
| **Adopt?** | ✅ Already adopted — reinforces existing design. |

---

## Category 19: Spec-Driven Development Ecosystem (OpenSpec, Spec Kit)

> 137K+ combined GitHub stars across SDD tools. The SDD movement validates our approach from an independent direction.

### P19.1 — "Spec Quality Should Be Elevated to Parity with Code Quality"

| Field | Value |
|-------|-------|
| **Source** | SDD ecosystem (OpenSpec, Spec Kit, multiple articles) |
| **Practice** | Specifications are the primary artifact of software development. Code is a "last-mile implementation." Teams should shift from code review to plan review — it's easier to read a markdown spec than a large diff, and writing one forces real thought. |
| **Reasoning** | "Generating code is now cheap. Correctness is still expensive." The bottleneck is underspecification, not model capability. |
| **Assessment** | ✅ Sound. This is the SDD ecosystem independently arriving at the same conclusion as Nate B. Jones (P16.1). Our system already treats specs as first-class artifacts via grill-me → PRD → story files. |
| **Relevance** | 🔴 Direct — independent validation of our specification-first approach. |
| **Adopt?** | ✅ Already adopted. |

### P19.2 — Constitution as Governing Principles

| Field | Value |
|-------|-------|
| **Source** | Spec Kit (GitHub) |
| **Practice** | A "constitution" document encodes immutable principles — coding standards, TDD requirements, compliance rules, architectural constraints. Every subsequent agent action respects the constitution. If the constitution says "all database changes require migration scripts," the agent enforces that every time. |
| **Reasoning** | Without encoded principles, each session re-derives decisions from scratch. A constitution makes decisions persistent and enforceable. |
| **Assessment** | ✅ Sound. This maps to our CLAUDE.md + UBIQUITOUS_LANGUAGE.md. The constitution IS our CLAUDE.md — but kept minimal per D11/D20. Project-specific rules that must be followed every time. |
| **Relevance** | 🟡 Medium — validates our existing CLAUDE.md approach. The word "constitution" is a better framing than "context file." |
| **Adopt?** | ✅ Already adopted. Consider renaming conceptually — CLAUDE.md is the project constitution. |

### P19.3 — Context Budget as a Hard Constraint (50KB Limit)

| Field | Value |
|-------|-------|
| **Source** | OpenSpec |
| **Practice** | OpenSpec enforces a 50KB context limit to prevent prompt bloat. "Agents working with specs won't choke on oversized context windows." A blunt instrument, but keeps agents focused. |
| **Reasoning** | The arxiv paper (2602.11988) showed comprehensive context hurts performance. OpenSpec operationalizes this with a hard limit. |
| **Assessment** | ✅ Sound principle, though the specific 50KB number may be arbitrary. The principle is right: measure and limit context size. |
| **Relevance** | 🟡 Medium — reinforces our minimal CLAUDE.md approach. We might want a size check on CLAUDE.md as a lint rule. |
| **Adopt?** | 🔶 Consider — add a warning if CLAUDE.md exceeds a size threshold. |

---

## Category 20: HumanLayer — CLAUDE.md Engineering

### P20.1 — CLAUDE.md Is the Highest Leverage Point in the Harness

| Field | Value |
|-------|-------|
| **Source** | HumanLayer blog |
| **Practice** | "A bad line of CLAUDE.md affects every single artifact produced." Claude Code's system prompt already contains ~50 instructions. Adding more to CLAUDE.md competes for attention. Every line should be universally applicable — avoid including instructions that only matter for specific tasks (those belong in skills). |
| **Reasoning** | CLAUDE.md goes into every session. If it contains noise, every session is degraded. If it contains signal, every session benefits. This is why it's both the highest leverage and highest risk file. |
| **Assessment** | ✅ Sound. This is the strongest practical argument for D11 (minimal CLAUDE.md) and D21 (learnings in separate file). The HumanLayer team's analysis of Claude Code's system prompt (~50 built-in instructions) quantifies why CLAUDE.md must be lean. |
| **Relevance** | 🔴 Direct — validates our core CLAUDE.md decisions. |
| **Adopt?** | ✅ Already adopted. |

---

## Category 21: Claude Code Tactical Practices (YouTube Playlist — 12 videos)

> These videos cover deeply tactical Claude Code practices. Several introduce genuinely novel patterns not found in any other Tier 1 or Tier 2 source.

### P21.1 — Context Rot: Proactive Context Management

| Field | Value |
|-------|-------|
| **Source** | "Context Rot: Why Claude Gets Dumber With Every Message" |
| **Practice** | Context rot is a structural problem — agent output degrades as context fills because attention weights on early instructions weaken. Key rules: (1) Use /clear proactively between tasks, not as a last resort. (2) If you've corrected Claude twice on the same issue, the context is cluttered — /clear. (3) Set a mental alarm at 60% context fill. (4) /compact with explicit instructions about what to preserve. (5) A clean 160K budget beats a polluted 80K budget every time. |
| **Reasoning** | Context degradation isn't linear — it accelerates after ~65% fill. The "Lost in the Middle" paper showed attention is weakest in the middle of context. As conversation grows, initial instructions sink into the attention trough. |
| **Assessment** | ✅ Sound. This operationalizes what we knew theoretically. Our Ralph loops MUST include context management — either automatic rotation at a threshold, or /clear between iterations with structured handoff (complements D35 "land the plane"). |
| **Relevance** | 🔴 Direct — context rot is the #1 threat to overnight Ralph loop quality. |
| **Adopt?** | ✅ Yes — build context rotation into Ralph loop design. |

### P21.2 — Git Worktree as Standard Practice

| Field | Value |
|-------|-------|
| **Source** | "I'm using claude --worktree for everything now", "Devs can no longer avoid learning Git worktree" |
| **Practice** | Claude Code's `--worktree` flag creates isolated git worktrees per task. Each agent session gets its own filesystem. Combined with Agent Teams, this enables true parallel development without merge conflicts. |
| **Reasoning** | Multiple agents in the same checkout create race conditions. Worktrees solve this at the filesystem level. Boris Cherny's 5-parallel-sessions workflow implicitly uses this. |
| **Assessment** | ✅ Sound. This should be standard practice in our cookiecutter, especially for Agent Teams and parallel execution. |
| **Relevance** | 🔴 Direct — needed for parallel execution patterns. |
| **Adopt?** | ✅ Yes — include git worktree setup in cookiecutter. |

### P21.3 — Never Run /init (Codebase Readiness > Auto-Generation)

| Field | Value |
|-------|-------|
| **Source** | "Never Run claude /init", "Your codebase is NOT ready for AI (here's how to fix it)" |
| **Practice** | Auto-generated CLAUDE.md files are generic and wasteful. Hand-craft your CLAUDE.md with only project-specific, non-obvious conventions. Make your codebase AI-ready by having clear structure, good naming, consistent patterns — not by adding more context files. |
| **Reasoning** | Aligns with the arxiv finding (LLM-generated context files hurt performance 3%) and HumanLayer's analysis (every line of CLAUDE.md competes with 50 built-in system instructions). Auto-generated files add noise, not signal. |
| **Assessment** | ✅ Sound. Validates D11 (minimal CLAUDE.md) from a different angle. Our cookiecutter should generate a CLAUDE.md template with clear sections and guidance, not auto-populate it. |
| **Relevance** | 🔴 Direct — the cookiecutter must generate a thoughtful template, not auto-fill garbage. |
| **Adopt?** | ✅ Already aligned with D11/D20. |

### P21.4 — Karpathy's AutoResearch Pattern: Self-Improving Skills

| Field | Value |
|-------|-------|
| **Source** | "Andrej Karpathy's Math Proves Agent Skills Will Fail. Here's What to Build Instead.", "Build Self-Improving Claude Code Skills", "Stop Fixing Your Claude Skills. Autoresearch Does It For You" |
| **Practice** | Skills fail ~30% of the time and you don't notice. The AutoResearch pattern fixes this: (1) Define 3-6 binary yes/no eval criteria for a skill's output. (2) Run the skill against test inputs, score pass rate. (3) Let an agent analyze failures, propose mutations to the skill's prompt. (4) Keep changes that improve pass rate, discard those that don't. (5) Run overnight. One practitioner went from 41% → 92% in 4 rounds. |
| **Reasoning** | Karpathy's core insight: "The bottleneck isn't model capability — it's the feedback signal." Without evals, you can't distinguish improvements from regressions. Binary assertions produce clean signals; 1-7 scales produce noise the agent games. 6 explicit mutation operators (add constraint, add negative example, restructure, tighten vague language, remove bloat, add counterexample) outperform random prompt variation. |
| **Assessment** | ✅ Sound and **novel**. This is the missing piece in our learning system. D27 says recurring learnings should become deterministic gates. AutoResearch says skills themselves should be continuously improved via eval loops. Our anti-slop rubrics, our skill prompts, our CLAUDE.md guidance — all can be targets for AutoResearch optimization. This is how the system ACTUALLY gets better over time, not just through human-curated learnings. |
| **Relevance** | 🔴 Direct — this is the compounding mechanism that makes the harness get better over time. |
| **Adopt?** | ✅ Yes — build AutoResearch capability into the cookiecutter. Skills should have eval files alongside them. The learning system should include an AutoResearch loop for skill optimization. |

### P21.5 — AI Evals as Foundation

| Field | Value |
|-------|-------|
| **Source** | "If You Don't Understand AI Evals, Don't Build AI" |
| **Practice** | Without evals, you're guessing. Every skill, every anti-slop gate, every prompt should have measurable success criteria. Evals must be: binary (pass/fail, not 1-7), automated (no human in the loop for routine checks), comprehensive (test the failure modes, not just the happy path), and versioned (track improvement over time). |
| **Reasoning** | This is the foundation AutoResearch is built on. If you can't measure it, you can't improve it. Our anti-slop pipeline is an eval system — but we haven't yet defined eval files for our skills themselves. |
| **Assessment** | ✅ Sound. This reframes our entire quality system: anti-slop gates are evals for code output, but we also need evals for our own system components (skills, prompts, rubrics). |
| **Relevance** | 🔴 Direct — evals are the foundation of everything. |
| **Adopt?** | ✅ Yes — every skill in the cookiecutter should ship with an eval file. |

### P21.6 — Meta Staff Engineer Practices

| Field | Value |
|-------|-------|
| **Source** | "How I use Claude Code (Meta Staff Engineer Tips)" |
| **Practice** | Staff-level practices: (1) Use /clear often — every new task gets a clean context. (2) Queue multiple prompts — Claude processes them intelligently. (3) Review commit diffs, not conversation output. (4) Use git worktrees for parallel work. (5) Customize the GitHub PR review prompt to reduce noise. |
| **Reasoning** | Staff engineers have developed these practices through high-volume production use. The "review diffs not conversations" insight is particularly relevant — our human review should focus on git diffs, not agent chatter. |
| **Assessment** | ✅ Sound. Mostly reinforces existing practices but the "review diffs not conversations" point is new and important for our trust tier design. |
| **Relevance** | 🟡 Medium — reinforces existing practices with one new insight. |
| **Adopt?** | ✅ "Review diffs not conversations" should inform trust tier review UI. |

---

## Category 22: ACE Paper — Formal Framework for Self-Improving Context (arxiv 2510.04618)

> ICLR 2026 paper from Stanford/SambaNova. Formalizes the learning system architecture our project needs.

### P22.1 — Context as Evolving Playbooks, Not Static Files

| Field | Value |
|-------|-------|
| **Source** | Zhang et al., "Agentic Context Engineering" (arxiv 2510.04618, ICLR 2026) |
| **Practice** | Treat context (CLAUDE.md, learnings, skills) as evolving playbooks that accumulate, refine, and organize strategies through a Generator → Reflector → Curator pipeline. Context grows via structured incremental updates, not monolithic rewrites. |
| **Reasoning** | Two failure modes in prior approaches: "brevity bias" (summarization drops domain insights for conciseness) and "context collapse" (iterative rewriting erodes details over time). ACE prevents both by using itemized bullets with metadata rather than free-form prose. Results: +10.6% on agent benchmarks. |
| **Assessment** | ✅ Sound and academically validated. This is the formal framework for our learning store design. Our markdown learning files should use structured bullets with metadata (ID, helpful/harmful counters), not unstructured prose. |
| **Relevance** | 🔴 Direct — foundational for Phase 7 (Learning System) architecture. |
| **Adopt?** | ✅ Yes — learning store entries should be structured bullets with usage metadata. |

### P22.2 — Incremental Delta Updates Over Monolithic Rewrites

| Field | Value |
|-------|-------|
| **Source** | ACE paper |
| **Practice** | Context updates are itemized deltas (add bullet, update counter, prune redundant entry) merged deterministically by lightweight non-LLM logic. Never rewrite the entire context. Multiple deltas can merge in parallel. Periodic deduplication via semantic similarity prunes redundancy. |
| **Reasoning** | Monolithic rewrites introduce variance and information loss. Incremental updates are deterministic, auditable, and parallelizable. The "grow-and-refine" principle: append new bullets with unique IDs, update existing in-place, deduplicate only when context exceeds budget. |
| **Assessment** | ✅ Sound. Specifies the update mechanism for our learning store: never rewrite — append entries, update counters, prune when size exceeds threshold. Git history preserves everything. |
| **Relevance** | 🔴 Direct — specifies the update mechanism for our learning store. |
| **Adopt?** | ✅ Yes — learning store uses append-only deltas with periodic pruning. |

### P22.3 — Helpful/Harmful Counters on Context Bullets

| Field | Value |
|-------|-------|
| **Source** | ACE paper |
| **Practice** | Each context bullet has counters tracking how often it was marked helpful vs. harmful during actual use. High helpful:harmful ratios indicate durable strategies; low ratios indicate candidates for pruning. |
| **Reasoning** | Not all learnings are equally valuable. Without usage tracking, the learning store becomes a dumping ground. With counters, the system can auto-prune low-value entries and surface high-value ones. |
| **Assessment** | ✅ Sound. Every learning entry should track: when added, times referenced, times associated issue recurred vs. was prevented. Low-utility entries get flagged for human review. |
| **Relevance** | 🔴 Direct — solves the "learning store bloat" problem. |
| **Adopt?** | ✅ Yes — learning entries include usage metadata. |

---

## Category 23: Anthropic March 2026 Harness Design (Latest Research)

> Published March 24, 2026. Most current harness engineering research.

### P23.1 — Three-Agent System; Context Resets No Longer Needed with Opus 4.6

| Field | Value |
|-------|-------|
| **Source** | Anthropic engineering blog, "Harness design for long-running application development" (March 24, 2026) |
| **Practice** | Latest harness uses three agents (up from two). With Opus 4.6, context resets between sessions are no longer needed — the model no longer exhibits "context anxiety." The Agent SDK's automatic compaction handles context growth. Agents run as one continuous session across the whole build. "The space of interesting harness combinations doesn't shrink as models improve — it moves." |
| **Reasoning** | Each agent addresses a specific gap. The third agent specializes in a domain the other two don't cover well. Opus 4.6's improved coherence removes the need for the context reset workaround that was load-bearing in the Sonnet 4.5 harness. |
| **Assessment** | ✅ Sound and current. Implications: (1) D37 (context rotation in Ralph loops) may need revision — test whether Opus 4.6 + SDK compaction eliminates the need. (2) Three-agent pattern supports our two-stage review (D34) plus a third specialized role. |
| **Relevance** | 🔴 Direct — most current Anthropic harness research. May modify D37. |
| **Adopt?** | 🔶 Evaluate — test Opus 4.6 + SDK compaction before committing to manual context rotation. |

### P23.2 — GAN-Inspired Generator/Evaluator for Subjective Quality

| Field | Value |
|-------|-------|
| **Source** | Anthropic March 2026 harness blog |
| **Practice** | For subjective quality (design, writing), use a generator + evaluator architecture. The evaluator grades against named dimensions with specific criteria (design quality, originality, craft, fidelity). Building the evaluator criteria was the hardest part — turning "is this good?" into concrete, gradable dimensions. |
| **Reasoning** | This is Anthropic's solution to Karpathy's "taste problem" (P13.2). Decompose taste into named dimensions, build an evaluator that grades each. The evaluator prompt IS the anti-slop rubric. |
| **Assessment** | ✅ Sound. Our LLM-as-judge anti-slop gates should use named quality dimensions with specific criteria per dimension, not a single "is this good?" prompt. |
| **Relevance** | 🔴 Direct — specifies how to build effective LLM-as-judge gates. |
| **Adopt?** | ✅ Yes — anti-slop rubrics decompose quality into named dimensions. |

---

## Category 24: GitHub Agentic Primitives Framework

### P24.1 — Three-Layer Reliability Framework

| Field | Value |
|-------|-------|
| **Source** | GitHub Blog, "How to build reliable AI workflows with agentic primitives and context engineering" |
| **Practice** | Reliability = three layers: (1) Structured markdown prompts, (2) Agent primitives (reusable building blocks — skills, tools, commands), (3) Context engineering (strategic info management). Validation gates with explicit human approval at critical decision points. |
| **Reasoning** | Each layer addresses a different failure mode. Maps to our architecture: CLAUDE.md = layer 1, skills + hooks = layer 2, .claudeignore + progressive disclosure = layer 3. |
| **Assessment** | ✅ Sound framing. No new practices but useful as a mental model for explaining the system. |
| **Relevance** | 🟡 Medium — useful framing for documentation. |
| **Adopt?** | ✅ Adopt as documentation framing. |

---

## Category 25: Academic Papers — Agent Architecture, Context, and Evaluation

### P25.1 — OpenDev: Compound AI System Architecture for Coding Agents (arxiv 2603.05344)

| Field | Value |
|-------|-------|
| **Source** | "Building Effective AI Coding Agents for the Terminal" (March 2026) |
| **Practice** | A coding agent should be a "compound AI system" — a structured ensemble of agents and workflows, each independently bound to a user-configured LLM. Different execution phases (thinking, coding, compaction) benefit from different model capabilities. Architectural separation between REPL commands (user-triggered, synchronous, no LLM) and agent tools (LLM-selected, async, approval-gated, undo-tracked). |
| **Reasoning** | State-of-the-art AI results come from composing multiple models, not single model calls (Zaharia et al.). The system is model-agnostic by construction — switching providers requires config change, not code change. Capabilities are continuously upgradeable. |
| **Assessment** | ✅ Sound. Validates our multi-model approach (Opus for planning, Sonnet for execution). The command vs. tool separation maps to our slash commands vs. agent-invoked skills. |
| **Relevance** | 🟡 Medium — validates existing architecture decisions. |
| **Adopt?** | ✅ Already aligned. |

### P25.2 — ACON: Failure-Driven Context Compression Optimization (arxiv 2510.00615)

| Field | Value |
|-------|-------|
| **Source** | "Acon: Optimizing Context Compression for Long-horizon LLM Agents" (Oct 2025) |
| **Practice** | Treat context compression as an optimization problem: find cases where full context succeeded but compressed context failed, use an LLM to identify what the compression lost, revise compression guidelines to preserve that class of information. Results: 26-54% reduction in peak token usage while preserving accuracy. Gradient-free, works with any API model. |
| **Reasoning** | Naive compression (truncation, generic summarization) loses critical details. ACON optimizes WHAT to preserve during compression by learning from failures. The optimized compressor can be distilled into a smaller model (95%+ accuracy at lower cost). |
| **Assessment** | ✅ Sound and directly applicable. Our /compact instructions should be informed by failure analysis — when compaction causes issues, the compaction prompt should be updated to preserve that class of information. This is AutoResearch applied to context management. |
| **Relevance** | 🔴 Direct — specifies how to optimize context compaction in our Ralph loops. |
| **Adopt?** | ✅ Yes — treat compaction prompts as optimizable (analogous to skill optimization via AutoResearch). |

### P25.3 — Context Length Alone Hurts Performance Despite Perfect Retrieval (arxiv 2510.05381)

| Field | Value |
|-------|-------|
| **Source** | "Context Length Alone Hurts LLM Performance Despite Perfect Retrieval" (Oct 2025) |
| **Practice** | Even when a model can perfectly retrieve all evidence (100% exact match recitation), performance still degrades substantially as input length increases. The problem is NOT retrieval failure — it's processing degradation. Longer contexts hurt even when the model can "see" everything. |
| **Reasoning** | This overturns the assumption that bigger context windows = better performance. Performance degradation from length is a separate phenomenon from "lost in the middle." Implications: our CLAUDE.md minimalism (D11) isn't just about avoiding attention issues in the middle — even perfectly-attended-to context degrades processing quality when there's too much of it. |
| **Assessment** | ✅ Sound and academically rigorous. This is the strongest possible justification for our minimal context approach. Every unnecessary token in CLAUDE.md actively degrades output quality, even if Claude "reads" it all perfectly. |
| **Relevance** | 🔴 Direct — strongest justification for D11 (minimal CLAUDE.md). |
| **Adopt?** | ✅ Already adopted. This paper is the academic foundation. |

### P25.4 — Coding Agents as Long-Context Processors (arxiv 2603.20432)

| Field | Value |
|-------|-------|
| **Source** | "Coding Agents are Effective Long-Context Processors" (March 2026) |
| **Practice** | Instead of scaling context windows, externalize long text into the file system and let coding agents interact with it via tools (grep, read, write). Agents outperform direct long-context processing by 17.3% on average across benchmarks. Two key capabilities: native tool proficiency (executable interactions > semantic queries) and file system familiarity. |
| **Reasoning** | This validates Boris Cherny's finding that glob+grep beats RAG (P15.2). The agent doesn't need everything in context — it needs the ability to FIND things in the file system. Context is for working memory; the file system is for storage. |
| **Assessment** | ✅ Sound. Reinforces our architecture: don't put everything in CLAUDE.md. Put it in well-organized files and let Claude search for what it needs. The learning store, ubiquitous language, and project docs should be files Claude can grep, not context it carries everywhere. |
| **Relevance** | 🔴 Direct — validates file-system-first over context-first architecture. |
| **Adopt?** | ✅ Already aligned with our approach. |

### P25.5 — LLM-as-Judge for SE: Systematic Failures in Code Verification (arxiv 2508.12358)

| Field | Value |
|-------|-------|
| **Source** | "Uncovering Systematic Failures of LLMs in Verifying Code Against Natural Language Specifications" (Aug 2025) |
| **Practice** | Current LLMs achieve only 52-78% accuracy (RCRR) when judging whether code meets natural language specifications WITHOUT test cases. Step-by-step prompting can DEGRADE performance in code verification (counterintuitive — works for reasoning but hurts for verification). LLMs exhibit consistent error patterns that can be studied and compensated for. |
| **Reasoning** | This is the academic quantification of Nate B. Jones's "17% that looks right" problem (P16.4). LLM judges are NOT reliable as sole quality gates. They need to be combined with deterministic checks (tests, lint) and their systematic biases need to be understood and compensated for. |
| **Assessment** | ✅ Sound and sobering. Our anti-slop pipeline design is validated: LLM-as-judge gates (stochastic) MUST be layered on top of deterministic gates (tests, lint, type checks). Never rely on LLM judgment alone. The two-stage review (D34) helps — but even the LLM reviewer has systematic blind spots. |
| **Relevance** | 🔴 Direct — quantifies the limits of LLM-as-judge in our anti-slop pipeline. |
| **Adopt?** | ✅ Already adopted via multi-layer anti-slop design. This paper quantifies why. |

### P25.6 — LLM-as-Judge Survey: Multi-Dimensional Evaluation (arxiv 2503.02246, 2510.24367)

| Field | Value |
|-------|-------|
| **Source** | "From Code to Courtroom: LLMs as the New Software Judges" (SE 2030 vision paper), "LLM-as-a-Judge for SE" survey |
| **Practice** | Structured review across multiple dimensions (functionality, complexity, style, documentation, defects) outperforms single-pass review. Multi-evaluator frameworks (like SWE-Judge's 5 independent evaluators with strategy selection) improve reliability. Key criteria for LLM judges: must evaluate WITHOUT requiring reference solutions; must produce explanations alongside scores; must be evaluated for agreement with human judgment (Cohen's Kappa). |
| **Reasoning** | This validates both D34 (two-stage review: spec compliance + code quality) and D40 (decompose quality into named dimensions). The academic consensus: single-pass LLM review is unreliable; structured multi-dimensional review is more robust. |
| **Assessment** | ✅ Sound. Our anti-slop rubrics should follow this pattern: define 3-5 evaluation dimensions, each with its own criteria and binary pass/fail. The evaluator produces explanations for failures, not just scores. |
| **Relevance** | 🔴 Direct — validates and extends D34 and D40. |
| **Adopt?** | ✅ Already adopted. These papers provide the academic foundation. |

### P25.7 — IoT-SkillsBench: Human-Expert Skills >> LLM-Generated Skills (arxiv 2603.19583)

| Field | Value |
|-------|-------|
| **Source** | "Skilled AI Agents for Embedded and IoT Systems Development" (March 2026) |
| **Practice** | Compared three agent configurations: no skills, LLM-generated skills, and human-expert skills. LLM-generated skills provided INCONSISTENT benefits and sometimes DEGRADED performance by reinforcing incorrect assumptions. Human-expert skills achieved near-perfect success rates with moderate token overhead. "The effectiveness depends not merely on providing skills, but on the quality and grounding of those skills." |
| **Reasoning** | This is the academic validation of our arxiv 2602.11988 finding (LLM-generated context files hurt by 3%) applied specifically to skills. Auto-generated skills are worse than no skills in some cases. Human-curated, domain-grounded skills are dramatically better. |
| **Assessment** | ✅ Sound. This validates D11 (never auto-generate context files) and extends it to skills: our cookiecutter should provide human-crafted skill templates, not auto-generated ones. AutoResearch (D36) can then OPTIMIZE those human-written skills — but the starting point must be human expertise, not LLM guesswork. |
| **Relevance** | 🔴 Direct — validates human-crafted skills as the starting point, with AutoResearch as the optimization layer. |
| **Adopt?** | ✅ Already aligned. |

The following sources were evaluated but did not add new actionable practices beyond what Tier 1 already covers. They're noted here for completeness:

- **John Kim, Stefan Wirth, Joshua Morony** — YouTube tutorial creators. Good for learning Claude Code basics but no novel methodology contributions.
- **Bart Slodyczka, Nick Saraev** — AI automation content creators. Focus on business automation, not agentic coding methodology.
- **Aakash Gupta, The AI Automators, Simon Scrapes** — AI news/strategy content. Similar strategic framing to Nate B. Jones but less architecturally specific.
- **Ivan Kahl** — Claude Code tutorials. Reinforces Anthropic best practices without novel additions.
- **Arjun Roychowdhury** — AI coding content. No unique practices found.
- **Michia Rohrssen** — AI development content. No unique practices found beyond what other sources cover.
- **AGENTS.md** — Cross-platform context file standard (Linux Foundation backed). Relevant as an interoperability consideration but doesn't add practices for our Claude Code-native system. CLAUDE.md remains our primary context file; AGENTS.md is noted for cross-tool scenarios.
- **Geoffrey Huntley** — Ralph Wiggum originator. Already fully captured in tracker (D5, D24). Key unique insight already catalogued: "Better to fail predictably than succeed unpredictably."

---

## Category 26: Anthropic Engineering Blog — Deep Dive Findings

### P26.1 — Self-Evaluation Bias: Agents Praise Their Own Work

| Field | Value |
|-------|-------|
| **Source** | Anthropic engineering blog, harness design post (March 2026) |
| **Practice** | "When asked to evaluate work they've produced, agents tend to respond by confidently praising the work—even when quality is obviously mediocre." Generator and evaluator MUST be separate agents. |
| **Reasoning** | Self-evaluation bias is structural. The agent has sunk-cost attachment to its output. A fresh agent with no generation history provides unbiased evaluation. |
| **Assessment** | ✅ Sound. Definitive justification for writer/reviewer pattern and D34 (separate review agents). |
| **Relevance** | 🔴 Direct — explains WHY separate review agents work. |
| **Adopt?** | ✅ Already adopted. |

### P26.2 — Progressive Disclosure: Three-Level Skill Architecture

| Field | Value |
|-------|-------|
| **Source** | Anthropic engineering blog, Agent Skills post |
| **Practice** | Three levels: (1) Metadata only (~30-50 tokens) at startup for ALL skills. (2) SKILL.md body on trigger. (3) Additional files on demand within the skill. "The amount of context bundled into a skill is effectively unbounded" because the agent loads pieces on demand. |
| **Reasoning** | Loading all skill content at startup exhausts context. Progressive disclosure keeps startup minimal while making deep expertise available. |
| **Assessment** | ✅ Sound. Official Anthropic architecture guidance. All our skills must follow this pattern. |
| **Relevance** | 🔴 Direct — specifies skill architecture. |
| **Adopt?** | ✅ Yes — mandatory three-level progressive disclosure. |

### P26.3 — Sandboxing: 84% Fewer Permission Prompts

| Field | Value |
|-------|-------|
| **Source** | Anthropic engineering blog, sandboxing post |
| **Practice** | Filesystem + network isolation replaces per-action approval with boundary-based security. 84% fewer permission prompts internally. Both isolations required — without network, agent can exfiltrate; without filesystem, agent can escape. |
| **Reasoning** | Permission prompts are the enemy of autonomous operation. Sandboxing gives security of per-action approval with speed of autonomous operation. |
| **Assessment** | ✅ Sound. Worth evaluating as alternative to /permissions (D13) for Ralph loops. |
| **Relevance** | 🟡 Medium — alternative security model for autonomous execution. |
| **Adopt?** | 🔶 Evaluate for Ralph loop security. |

### P26.4 — Feature Requirements as Failing Checklist

| Field | Value |
|-------|-------|
| **Source** | Anthropic engineering blog, effective harnesses post |
| **Practice** | Initializer agent writes 200+ feature requirements all marked "failing." Coding agent turns them "passing." Agent can't claim "done" while items still fail. Prevents one-shotting and premature completion. |
| **Reasoning** | Without explicit checklist, agent's "done" is subjective and tends toward premature completion. A failing-to-passing checklist makes progress objective. |
| **Assessment** | ✅ Sound and specific. Our story files should include testable checklists, all initially incomplete. |
| **Relevance** | 🔴 Direct — specifies story file internal structure. |
| **Adopt?** | ✅ Yes — story files include failing-to-passing feature checklists. |

---

## Category 27: Plugin Ecosystem Analysis

### P27.1 — Feature-Dev Plugin: 89K Installs, Same Problem We're Solving

| Field | Value |
|-------|-------|
| **Source** | Anthropic official marketplace |
| **Practice** | Seven-phase workflow: requirements → codebase exploration (parallel agents) → architecture → implementation → testing → review → documentation. Smart enough to skip phases for trivial changes. 89K installs — most popular Claude Code plugin. |
| **Assessment** | ✅ We should compose with this plugin rather than rebuild its functionality. Our cookiecutter adds the harness, learning system, backlog management, and anti-slop configuration on top of existing plugins. |
| **Relevance** | 🔴 Direct — shifts architecture from "build everything" to "compose and configure." |
| **Adopt?** | 🔶 Evaluate — extend feature-dev or build independently? |

### P27.2 — Code-Review Plugin: 4 Parallel Agents with Confidence Scoring

| Field | Value |
|-------|-------|
| **Source** | Anthropic official marketplace |
| **Practice** | Four agents in parallel: two check CLAUDE.md compliance, one scans for bugs, one analyzes git history for context-based issues. Confidence scoring (0-100) filters noise — only issues above threshold (default 80) appear. |
| **Assessment** | ✅ More sophisticated than our planned two-stage review. Use this plugin directly, customize its review prompt with our anti-slop rubric dimensions. |
| **Relevance** | 🔴 Direct — don't reinvent this. Customize it. |
| **Adopt?** | ✅ Yes — use official code-review plugin as baseline. |

### P27.3 — Cookiecutter as Composition Layer, Not Component Builder

| Field | Value |
|-------|-------|
| **Source** | Plugin ecosystem analysis (9,000+ plugins, 101 official) |
| **Practice** | The plugin ecosystem is mature. Our cookiecutter should include a settings.json that configures the right plugins, a CLAUDE.md template, skill templates with eval files, hook configurations, and workflow guidance — NOT rebuild plugin functionality. Team distribution via settings.json checked into the codebase. |
| **Assessment** | ✅ Sound. This is the most consequential architectural insight from this research round. The cookiecutter's value is the WORKFLOW and CONFIGURATION, not the individual components. |
| **Relevance** | 🔴 Direct — redefines what the cookiecutter actually produces. |
| **Adopt?** | ✅ Yes — cookiecutter = composition + configuration + learning system. |

---

## Category 28: Dan Shipper / Every — Compound Engineering

> Boris Cherny directly references Dan Shipper's work. "Compounding engineering turns every PR, bug fix, and code review into permanent lessons." Two engineers shipped like a team of 15.

### P28.1 — The "Compound" Step: Codify Learnings After Every Cycle

| Field | Value |
|-------|-------|
| **Source** | Dan Shipper, Kieran Klaassen, Every.to |
| **Practice** | Four-step loop: Plan → Work → Assess → Compound. The "Compound" step is the key: after every cycle, codify what you learned — what issues arose, what patterns worked, what was missed — back into prompts, subagents, slash commands, and CLAUDE.md. "80% of compound engineering is in the plan and review parts, while 20% is in the work." |
| **Reasoning** | "In normal engineering, every feature makes the next one harder. In compounding engineering, every feature makes the next one easier." Without the codify step, you're just doing fast normal engineering. The codify step is what makes it compound. |
| **Assessment** | ✅ Sound. This is the practitioner-tested implementation of our learning system (Phase 7). Boris Cherny's team does this — tagging @.claude on PRs to update CLAUDE.md. Dan Shipper named it and systematized it. Our cookiecutter should include this loop as the default workflow. |
| **Relevance** | 🔴 Direct — the compound step IS our learning system. |
| **Adopt?** | ✅ Yes — the Plan → Work → Assess → Compound loop should be the default workflow. |

### P28.2 — 12-Subagent Parallel Review

| Field | Value |
|-------|-------|
| **Source** | Kieran Klaassen, Every.to |
| **Practice** | Every's compound engineering plugin reviews code with 12 subagents in parallel, each checking from a different perspective. "A critical bug I would have otherwise missed." |
| **Reasoning** | More review angles = more failure modes caught. 12 is aggressive but the parallelism means no wall-clock cost. This is the most sophisticated review system we've found — more than Anthropic's 4-agent code-review plugin. |
| **Assessment** | ✅ Sound but possibly over-engineered for a solo developer. Their plugin is available — evaluate whether to use it directly. |
| **Relevance** | 🟡 Medium — interesting but may be more than Dan needs for a solo workflow. |
| **Adopt?** | 🔶 Evaluate — compare Every's 12-agent review vs. Anthropic's 4-agent review for our use case. |

### P28.3 — "Implementation Should Be Boring" (Boris Tane)

| Field | Value |
|-------|-------|
| **Source** | Boris Tane (boristane.com) |
| **Practice** | Three-round annotation cycle: Claude generates plan → Dan annotates with corrections/priorities → Claude updates → repeat. By the time implementation starts, every decision has been made. "I want implementation to be boring. The creative work happened in the annotation cycles." Prompt: "implement it all, mark it as completed in the plan document, do not stop until all tasks are completed." |
| **Reasoning** | If implementation is creative, the spec wasn't good enough. A good plan is one where implementation is mechanical execution against a checklist. This is the ultimate expression of P16.1 (specification bottleneck) — solve all the hard problems in the plan, not in the code. |
| **Assessment** | ✅ Sound and practically demonstrated. The annotation cycle is a concrete implementation of grill-me — human judgment injected at the planning stage, not the execution stage. |
| **Relevance** | 🔴 Direct — specifies how plan → implementation handoff should work. |
| **Adopt?** | ✅ Yes — plan annotation cycles until implementation is boring. |

---

## Category 29: Academic Papers — Agent Memory and Self-Improvement

### P29.1 — Trajectory-Informed Memory: Three Types of Learnings (arxiv 2603.10600)

| Field | Value |
|-------|-------|
| **Source** | "Trajectory-Informed Memory Generation for Self-Improving Agent Systems" (March 2026) |
| **Practice** | Extract three types of learnings from agent execution traces: (1) Strategy tips from successful patterns. (2) Recovery tips from failure handling. (3) Optimization tips from inefficient but successful executions. Each learning has provenance tracking back to the source trajectory. Naive experience accumulation leads to error propagation — quality-aware curation is essential. |
| **Reasoning** | Not all learnings come from failures. An agent that succeeds inefficiently is a learning opportunity too. And generic advice ("be careful with API calls") provides no value — learnings must be specific and contextual. Learnings must be retrievable by context (task type, domain, semantic similarity) because a wrong learning retrieved at the wrong time degrades performance. |
| **Assessment** | ✅ Sound and directly applicable. Our learning store should categorize entries as strategy/recovery/optimization, include provenance (which task generated the learning), and support contextual retrieval (which types of tasks should see this learning). |
| **Relevance** | 🔴 Direct — specifies the internal taxonomy of our learning store. |
| **Adopt?** | ✅ Yes — learning entries include type (strategy/recovery/optimization) and provenance. |

### P29.2 — Self-Improving Coding Agent: 17-53% Performance Gains (arxiv 2504.15228)

| Field | Value |
|-------|-------|
| **Source** | "A Self-Improving Coding Agent" (April 2025, updated May 2025) |
| **Practice** | An agent system can autonomously edit its own orchestration code to improve performance. Performance gains of 17-53% on SWE-bench Verified. This is "non-gradient-based learning" — the agent reflects on its failures, edits its own prompts/tools, and retests. Data-efficient and doesn't require fine-tuning. |
| **Reasoning** | This is the academic validation of AutoResearch (D36) applied to the agent system itself, not just individual skills. The agent improves its own harness. Combined with our learning store, this means the system can improve not just its knowledge but its own workflow. |
| **Assessment** | ✅ Sound. 17-53% improvement is massive. The key constraint: the self-improvement must be bounded (eval-gated, human-reviewable) or the agent can optimize for the wrong thing. Our AutoResearch loops should be eval-gated with human review of accepted changes. |
| **Relevance** | 🔴 Direct — validates AutoResearch at the system level, not just skill level. |
| **Adopt?** | ✅ Already adopted via D36. This paper validates the approach academically. |

### P29.3 — Memory Survey: Agent Memory Is Fragmented and Needs Taxonomy (arxiv 2512.13564)

| Field | Value |
|-------|-------|
| **Source** | "Memory in the Age of AI Agents: A Survey" (Dec 2025, ICLR 2026 scope) |
| **Practice** | Agent memory research is fragmented — loosely defined terms, inconsistent taxonomies. The survey proposes a unified taxonomy: memory forms (what), functions (how), and dynamics (when/why). Key distinction: episodic memory (specific experiences), semantic memory (generalized knowledge), procedural memory (how-to), and working memory (active context). |
| **Reasoning** | Our learning store needs clear categories. The episodic/semantic/procedural distinction maps well: episodic = "on task X, we hit bug Y and fixed it with Z"; semantic = "always use pattern A for problem class B"; procedural = "the workflow for deploying is X → Y → Z." |
| **Assessment** | ✅ Sound. Provides the theoretical framework for categorizing our learning store entries alongside the practical ACE framework (P22.1-P22.3). |
| **Relevance** | 🟡 Medium — theoretical framework that informs but doesn't change our design. |
| **Adopt?** | 🔶 Note — useful vocabulary for documentation and design discussions. |

---

## Category 30: Code Quality — Timeless Principles and AI-Specific Failure Modes

> This category addresses "what makes code good?" from a software engineering perspective, then maps where AI-generated code systematically fails on these dimensions. These principles should be embedded in our anti-slop rubrics and review prompts.

### P30.1 — The Timeless Principles (SOLID, DRY, KISS, YAGNI, SRP)

| Field | Value |
|-------|-------|
| **Source** | Martin Fowler, Robert C. Martin (Clean Code), Hunt & Thomas (Pragmatic Programmer), multiple 2025-2026 code quality guides |
| **Practice** | Five enduring principles that define maintainable code: **SOLID** (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion), **DRY** (Don't Repeat Yourself — but use the Rule of Three: duplicate once if needed, refactor on third occurrence), **KISS** (simplest solution that works), **YAGNI** (don't build features speculatively), and **SRP** applied at every level (function does one thing, class has one reason to change). |
| **Reasoning** | These principles are timeless because they address the fundamental constraint of software: code is read 10x more than it's written (Robert C. Martin). They reduce cognitive load, make code easier to modify, and prevent technical debt accumulation. AI doesn't change these principles — it makes them more important, because AI generates code faster than humans can review it. |
| **Assessment** | ✅ Sound and foundational. These should be embedded in our CLAUDE.md template and anti-slop rubric as the baseline quality bar. Not as abstract platitudes but as concrete, checkable criteria. |
| **Relevance** | 🔴 Direct — defines what "quality code" means in our system. |
| **Adopt?** | ✅ Yes — encode as named dimensions in anti-slop rubrics. |

### P30.2 — Meaningful Naming as the Highest-Leverage Readability Practice

| Field | Value |
|-------|-------|
| **Source** | Clean Code (Martin), cognitive complexity research, readability studies |
| **Practice** | Of all code quality practices, meaningful naming has the strongest empirical support for improving readability. A study analyzing 25 code features found naming consistency was the single most influential factor in readability judgments. Specific guidance: use domain language (ubiquitous language), not generic programming terms. `calculate_final_price()` not `compute()`. `is_leap_year()` not `flag`. Variable names should reveal intent without needing a comment to explain. |
| **Reasoning** | Naming is the primary channel through which code communicates its purpose to humans. Poor names force readers to build mental models from scratch; good names let readers leverage existing domain knowledge. This is where AI-generated code most often erodes over time (see P30.6 — Model Collapse). |
| **Assessment** | ✅ Sound. Our anti-slop rubric should include a "naming quality" dimension: Do names reveal intent? Do they use domain language? Are they consistent across the codebase? This is checkable by an LLM reviewer even though linters can't catch it. |
| **Relevance** | 🔴 Direct — highest-leverage readability practice for the anti-slop rubric. |
| **Adopt?** | ✅ Yes — "naming quality" as a named dimension in anti-slop rubrics. |

### P30.3 — Cognitive Complexity as the Measurable Proxy for Readability

| Field | Value |
|-------|-------|
| **Source** | SonarSource cognitive complexity metric, University of Stuttgart study (24,000 evaluations), Miller's Law |
| **Practice** | Cognitive complexity measures mental effort to understand code, scored by: nesting depth (each level adds load), flow-breaking constructs (break, continue, early returns), and control structure complexity. Unlike cyclomatic complexity (which counts execution paths), cognitive complexity correlates with developer-perceived difficulty. Miller's Law: working memory holds 3-4 items (not 7 as popularly claimed). Code that requires tracking more than 3-4 things simultaneously exceeds human capacity. |
| **Reasoning** | This is the measurable version of "is this code easy to understand?" SonarQube's cognitive complexity metric can be automated in CI. Functions with cognitive complexity > 15 should be refactored. Deeply nested code (3+ levels) should be flattened using early returns, guard clauses, or extracted helper functions. |
| **Assessment** | ✅ Sound and measurable. Our cookiecutter should include cognitive complexity checks as a deterministic gate. This is one of the few quality dimensions that can be automated rather than requiring LLM judgment. |
| **Relevance** | 🔴 Direct — can be added to our deterministic quality gates (alongside ruff, mypy, tests). |
| **Adopt?** | ✅ Yes — add cognitive complexity threshold to deterministic gates. |

### P30.4 — Small Functions with Single Responsibility

| Field | Value |
|-------|-------|
| **Source** | Clean Code, Pragmatic Programmer, multiple practitioner guides |
| **Practice** | Functions should do one thing, do it well, and do it only. Concrete heuristics: if a function needs a comment to explain what it does, the name is wrong or the function does too much. If a function has more than one level of abstraction, it should be split. If a function takes more than 3 parameters, it probably needs a data structure. Extract complex conditionals into well-named boolean functions (`is_eligible_for_discount()` not `if age > 65 and member_since < 2020 and total > 100`). |
| **Reasoning** | Small functions are easier to name (because they do one thing), easier to test (because they have one behavior), easier to reuse (because they aren't coupled to unrelated logic), and easier to replace (because their contract is clear). AI tends to write long functions that handle multiple concerns — this is the most common quality gap to check for. |
| **Assessment** | ✅ Sound. "Function length and responsibility" should be a named dimension in our anti-slop rubric. Concrete threshold: functions over 30 lines should be flagged for review; functions over 50 lines should be split. |
| **Relevance** | 🔴 Direct — defines a concrete quality dimension for review. |
| **Adopt?** | ✅ Yes — "function responsibility" as anti-slop rubric dimension with concrete thresholds. |

### P30.5 — Five Levels of Readable Code (from Formatting to Domain Language)

| Field | Value |
|-------|-------|
| **Source** | Carlos Schults "5 Levels of Readable Code," Eric Evans (DDD ubiquitous language) |
| **Practice** | Code readability has a hierarchy: **Level 1** — Basic formatting (naming, indentation, no magic numbers). **Level 2** — Idiomatic code (follows language conventions; Pythonic Python). **Level 3** — Structural clarity (SRP, small functions, clear abstractions). **Level 4** — Cohesive architecture (modules organized by domain, not by technical layer). **Level 5** — Domain language (code uses the same terms domain experts use; ubiquitous language from DDD). Non-idiomatic code increases cognitive load because it violates the reader's mental model of the language. |
| **Reasoning** | This hierarchy gives us a maturity model for code quality. Level 1-2 can be enforced by linters and formatters (deterministic). Level 3 can be partially measured by cognitive complexity. Levels 4-5 require human or LLM judgment — this is where our stochastic anti-slop gates add value. AI-generated code typically passes Level 1-2 but fails at Level 4-5 (it uses generic patterns instead of domain-specific ones). |
| **Assessment** | ✅ Sound. Maps cleanly to our two-layer quality system: deterministic gates handle Levels 1-2, LLM-as-judge gates handle Levels 3-5. Our ubiquitous language file (already in tracker) is the tool for enforcing Level 5. |
| **Relevance** | 🔴 Direct — provides the maturity model for our quality system. |
| **Adopt?** | ✅ Yes — use as the framework for structuring anti-slop rubric dimensions. |

### P30.6 — AI-Specific Code Smell: "Model Collapse" (Domain Language Erosion)

| Field | Value |
|-------|-------|
| **Source** | Code Smell 314 (dev.to/mcsee), SoftwareSeni anti-patterns analysis |
| **Practice** | When AI modifies code repeatedly without human oversight, domain language erodes: "Customer" becomes "data," "Order" becomes "item," "apply_pricing_tier()" becomes "calculate_total_with_discount()." Each AI iteration moves further from domain language toward generic programming constructs. The code becomes "technically functional but semantically hollow" — AI slop. |
| **Reasoning** | AI optimizes for local token generation without understanding the domain model. It replaces specific domain terms with generic ones because generic patterns appear more frequently in training data. This is the exact opposite of Level 5 readability (ubiquitous language). Our ubiquitous language file acts as the antidote — the reviewer can check whether AI-modified code still uses the correct domain terms. |
| **Assessment** | ✅ Sound and novel. This is an AI-SPECIFIC quality problem that traditional code review wouldn't catch. "Domain language preservation" should be a named dimension in our anti-slop rubric. The ubiquitous language file gives the reviewer the reference to check against. |
| **Relevance** | 🔴 Direct — identifies a quality failure mode unique to AI-generated code. |
| **Adopt?** | ✅ Yes — "domain language preservation" as anti-slop dimension, checked against ubiquitous language file. |

### P30.7 — AI-Specific Code Smell: Context Blindness (Cross-File Duplication)

| Field | Value |
|-------|-------|
| **Source** | SoftwareSeni analysis, arxiv code smell studies |
| **Practice** | AI reimplements logic that already exists elsewhere in the codebase because it can't retain full project context beyond its window. Result: multiple parallel implementations of the same functionality (e.g., three different authentication approaches in three different files). Code duplication percentage serves as a "context blindness indicator." |
| **Reasoning** | Larger context windows reduce but don't eliminate this. The agent generates new code more readily than it searches for existing implementations. This is why glob+grep (P15.2) and file-system-first architecture (P25.4) matter — the agent needs habits of SEARCHING before CREATING. |
| **Assessment** | ✅ Sound. Our CLAUDE.md should include an instruction: "Before implementing any utility or helper, search the codebase for existing implementations." Our anti-slop rubric should include "unnecessary duplication" as a dimension, with the reviewer specifically checking whether the new code duplicates existing functionality. |
| **Relevance** | 🔴 Direct — specifies a CLAUDE.md instruction and anti-slop dimension. |
| **Adopt?** | ✅ Yes — add "search before creating" to CLAUDE.md; add "unnecessary duplication" to anti-slop rubric. |

### P30.8 — AI-Specific Code Smell: Refactoring Avoidance

| Field | Value |
|-------|-------|
| **Source** | SoftwareSeni analysis, OX Security |
| **Practice** | AI avoids refactoring 80-90% of the time. When asked to add a feature, it adds the feature wherever requested without considering whether the existing code should be restructured first. It "implements prompts directly without considering refactoring opportunities, architectural patterns, or maintainability trade-offs." This leads to growing complexity, god functions, and coupled modules over time. |
| **Reasoning** | AI doesn't think "this new feature would fit better if I restructured the existing authentication module first." Humans make that judgment call. This is why the plan phase (D49 — implementation should be boring) must include a refactoring assessment: "Does the existing code need restructuring to accommodate this feature cleanly?" The review phase should check: "Did the agent add code without refactoring when refactoring was warranted?" |
| **Assessment** | ✅ Sound. "Refactoring consideration" should be part of the planning phase, not just the review phase. The plan annotation cycle should explicitly ask: "Is the existing code structured to accommodate this feature, or does it need restructuring first?" |
| **Relevance** | 🔴 Direct — specifies a planning-phase check and review-phase dimension. |
| **Adopt?** | ✅ Yes — add refactoring assessment to plan phase; "refactoring avoidance" to anti-slop rubric. |

### P30.9 — AI-Specific Code Smell: Excessive Cognitive Complexity

| Field | Value |
|-------|-------|
| **Source** | arxiv 2508.14727 ("Assessing the Quality and Security of AI-Generated Code") |
| **Practice** | Claude 3.7 Sonnet generated 422 instances of high cognitive complexity in one study (compared to GPT-4o's 112). LLMs "optimize for local token generation without accounting for global complexity metrics." The code works but is hard to understand because the AI doesn't feel the cognitive burden of reading it later. All evaluated LLMs produced code smells — no model generates consistently defect-free code. |
| **Reasoning** | The key academic finding: "LLMs face challenges with foresight, strategic planning, and understanding of non-local consequences." They generate placeholder structures without populating them, create dead/unused code, and produce incomplete error handling. Static analysis tools (SonarQube, ruff) can catch these deterministically. |
| **Assessment** | ✅ Sound. This validates our two-layer approach: cognitive complexity and dead code detection should be deterministic gates (automated, every PR); architectural coherence and naming quality should be stochastic LLM-as-judge gates. |
| **Relevance** | 🔴 Direct — specifies which quality dimensions are deterministic vs. stochastic. |
| **Adopt?** | ✅ Yes — cognitive complexity and dead code as deterministic gates. |

### P30.10 — The "Taste" Gap: What Linters Can't Catch

| Field | Value |
|-------|-------|
| **Source** | Karpathy "taste problem" (P13.2), Anthropic GAN evaluator (P23.2), Qodo code quality analysis |
| **Practice** | There is a permanent gap between what deterministic tools can check (formatting, unused imports, type errors, cognitive complexity) and what constitutes "good" code. The gap includes: architectural fit (does this code belong here?), appropriate abstraction level (is this too abstract or too concrete?), naming quality (do names reveal intent?), domain language preservation (does the code speak the business language?), and unnecessary complexity (is there a simpler way?). This gap requires human judgment or LLM-as-judge gates. |
| **Reasoning** | AI writes functional but architecturally bland code. It passes all deterministic checks but produces code that experienced developers would call "meh." This is the taste gap. Anthropic's solution (P23.2): decompose taste into named dimensions with specific criteria, then build an evaluator that grades each. Our anti-slop rubric IS the taste specification. |
| **Assessment** | ✅ Sound and actionable. Our anti-slop rubric should have two tiers: Tier 1 (deterministic, automated): formatting, type checking, cognitive complexity, dead code, test coverage. Tier 2 (stochastic, LLM-judged): naming quality, domain language, function responsibility, architectural fit, unnecessary duplication, refactoring avoidance. |
| **Relevance** | 🔴 Direct — specifies the complete anti-slop rubric structure. |
| **Adopt?** | ✅ Yes — two-tier anti-slop rubric (deterministic + stochastic). |

---

## Category 31: Architectural Principles for AI-Ready Codebases

> Drawn from Matt Pocock's "Your codebase is not ready for AI," John Ousterhout's "A Philosophy of Software Design," and Ian Bull's relational algebra analysis. What works for humans also works for AI — but AI punishes bad architecture harder because it can't compensate.

### P31.1 — Deep Modules with Clear Interfaces (Ousterhout / Pocock)

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock (aihero.dev), John Ousterhout ("A Philosophy of Software Design"), Ian Bull analysis |
| **Practice** | Modules should be "deep" — simple interface, complex implementation hidden behind it. Instead of a web of interconnected shallow modules (hard to navigate, hard to test, hard to keep in your head), design modules that expose a small, clear API and hide implementation complexity. "Give each module its own folder with a clear public interface. The AI can see all the services on the file system, read their types, and understand what they do — without digging into the implementation." |
| **Reasoning** | When a human works in a messy codebase, they compensate — they build context over time, learn tribal knowledge, know that module X secretly depends on database table Y. AI can't compensate. It takes architecture at face value. If interfaces don't tell the truth about what modules do, AI produces code that looks correct locally but breaks things globally. Deep modules with honest interfaces are the architectural foundation for AI-readability. |
| **Assessment** | ✅ Sound and critical. This is the module-level version of SRP. Our CLAUDE.md should include guidance on module design: "Each module should have a clear public interface (exported types and functions) in its __init__.py. Implementation details should be internal. AI should be able to understand what a module does by reading its interface, not its implementation." |
| **Relevance** | 🔴 Direct — specifies the module architecture pattern. |
| **Adopt?** | ✅ Yes — CLAUDE.md guidance on module interface design. |

### P31.2 — Progressive Disclosure of Complexity in Codebase Architecture

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock, Anthropic skills architecture |
| **Practice** | A well-designed codebase has progressive disclosure of complexity: at the top level, you see a handful of well-named services with clear interfaces. If you need more detail, you read the types and contracts. Only if you need to modify implementation do you look inside. "Instead of holding hundreds of interrelated modules in your head, you keep seven or eight chunks. The AI manages what's inside each one. You only worry about designing the interfaces and how they fit together." |
| **Reasoning** | This maps directly to Miller's Law (working memory holds 3-4 items, generously 7±2). Both humans and AI process code more effectively when the top-level structure is navigable without understanding implementation. This is the same principle Anthropic uses for skills (P26.2 — three-level progressive disclosure) applied to the codebase itself. |
| **Assessment** | ✅ Sound. The cookiecutter's src layout should model this: top-level package has clear submodules, each with an __init__.py that exports only the public interface. Internal implementation files are prefixed with underscore or organized in an _internal/ subdirectory. |
| **Relevance** | 🔴 Direct — specifies how the cookiecutter organizes the generated project. |
| **Adopt?** | ✅ Yes — cookiecutter template uses progressive disclosure in package structure. |

### P31.3 — "Sinks, Not Pipes" — Design for Deletability and Decoupling

| Field | Value |
|-------|-------|
| **Source** | Ian Bull analysis, Matt Pocock rule 8 |
| **Practice** | A "pipe" does its work then triggers something else (tight coupling). A "sink" accepts input, does its work, and returns a result without side effects or hidden dependencies. Build sinks, not pipes. Matt Pocock: "The economics of refactoring have changed. It's now cheaper to delete code and re-do it than to refactor it. This means that highly decoupled systems, where modules are easy to delete, will benefit most from AI." |
| **Reasoning** | If module A calls module B which triggers module C, an AI modifying module B can't predict the impact on C. If B is a sink that returns a value, the caller decides what to do next — the coupling is visible at the call site. Deletability is the strongest test of decoupling: if you can't delete a module without cascading changes, it's too coupled. |
| **Assessment** | ✅ Sound. This should be a CLAUDE.md architectural principle: "Prefer pure functions and explicit return values over side effects and implicit triggers. If a function modifies state, make the state change explicit in the return type or function name." |
| **Relevance** | 🟡 Medium — architectural guidance, not a per-PR check. |
| **Adopt?** | ✅ Yes — include as an architectural principle in CLAUDE.md. |

### P31.4 — Thoughtfully Designed Interfaces as the Primary Quality Investment

| Field | Value |
|-------|-------|
| **Source** | Matt Pocock "design-an-interface" skill, SOLID (ISP, DIP), Steve Yegge "design becomes bottleneck" |
| **Practice** | Interface design is where the human applies taste. When execution is cheap (AI writes implementation), the bottleneck moves to design: "What goes into which module? What does the public API look like? What are the contracts between components?" Matt Pocock's `design-an-interface` skill generates multiple radically different interface designs using parallel sub-agents so the human can choose. The Interface Segregation Principle (ISP) says: no client should depend on methods it doesn't use. The Dependency Inversion Principle (DIP) says: depend on abstractions, not implementations. |
| **Reasoning** | Interfaces are the one thing AI can't judge well on its own — they require understanding the full system context and future evolution. The human's job in the AI-native workflow is increasingly about designing interfaces and reviewing whether AI-written implementations honor those interfaces correctly. |
| **Assessment** | ✅ Sound. This is the architectural version of D49 ("implementation should be boring"). The creative work is interface design; implementation is mechanical. Our plan phase should explicitly include interface design before implementation begins. |
| **Relevance** | 🔴 Direct — specifies what the human does during planning. |
| **Adopt?** | ✅ Yes — plan phase includes interface design as explicit step. |

---

## Category 32: Python-Specific Code Quality Practices

> Python's dynamic typing is its greatest strength and greatest risk. These practices compensate for the type system's permissiveness while maintaining Python's expressiveness. AI-generated Python code is especially prone to these issues because the interpreter won't catch them.

### P32.1 — Never Pass Dicts as Args When You Know the Shape

| Field | Value |
|-------|-------|
| **Source** | Dan (project owner, personal rule), Real Python best practices, type checking guides |
| **Practice** | Dicts should only be passed as function arguments when there are genuinely no requirements about what keys should be present. If specific keys are required, use a dataclass, TypedDict, NamedTuple, or Pydantic model instead. If you MUST pass a dict with required keys (e.g., interfacing with legacy code), use assert statements or runtime validation to verify key presence. This is symptomatic of the broader challenge: Python's dynamic typing lets you be lazy about interfaces, and AI exploits this laziness because `dict[str, Any]` is the path of least resistance. |
| **Reasoning** | A function signature `def process(data: dict)` tells you nothing — you have to read the implementation to know what keys it needs. A signature `def process(order: OrderData)` is self-documenting. The dict version hides the interface; the typed version IS the interface. AI defaults to dicts because they're flexible and appear frequently in training data. The human must enforce structured types. |
| **Assessment** | ✅ Sound and strongly held by the project owner. This should be a CLAUDE.md rule and an anti-slop rubric check: "Does any function accept a dict when a dataclass or TypedDict would be more appropriate?" |
| **Relevance** | 🔴 Direct — personal quality standard of the project owner. |
| **Adopt?** | ✅ Yes — CLAUDE.md rule: "Never accept dict as a parameter when the expected shape is known. Use dataclass, TypedDict, NamedTuple, or Pydantic model." |

### P32.2 — Type Hints Everywhere, mypy --strict on New Code

| Field | Value |
|-------|-------|
| **Source** | PEP 484, Real Python, mypy documentation, multiple type checking guides |
| **Practice** | All function parameters have type hints. Return type is explicitly annotated. Optional parameters use `X | None` (not bare Optional). Generic types specify element types (`list[str]`, not `list`). No `Any` without justification — `Any` opts out of type checking entirely. Run `mypy --strict` on new code; use per-module overrides for legacy code. Use `Protocol` for duck-typed interfaces. Prefer `dataclass` for new structured types, `TypedDict` for dict-shaped data from external sources (APIs, JSON). |
| **Reasoning** | Type hints are Python's compensation for dynamic typing. They catch 15% more bugs than manual review alone. They make code self-documenting — the function signature IS the interface contract. AI-generated code often uses correct but overly broad types (`dict[str, Any]` instead of a typed model). mypy --strict enforces that type hints are present and meaningful. |
| **Assessment** | ✅ Sound. The cookiecutter should ship with mypy configured at strict level for the src/ package, with pyproject.toml settings ready to go. The PostToolUse hook should run mypy after edits (alongside ruff). |
| **Relevance** | 🔴 Direct — specifies the type checking configuration for the cookiecutter. |
| **Adopt?** | ✅ Yes — mypy --strict configured in pyproject.toml, PostToolUse hook runs mypy. |

### P32.3 — Dataclasses Over Raw Dicts for Internal Data Structures

| Field | Value |
|-------|-------|
| **Source** | Real Python, Meeshkan TypedDict vs dataclass analysis, Python community consensus |
| **Practice** | For new code: use `@dataclass` for structured internal data (configuration, domain objects, command parameters). Use `TypedDict` when interfacing with dict-shaped external data (JSON APIs, database rows). Use Pydantic `BaseModel` for validated external input (API request bodies, user input). Never use raw dicts for data that flows through more than one function — create a type. Key principle: if a dict is passed to more than one function, it should be a dataclass. |
| **Reasoning** | Dataclasses give you: typed fields with defaults, `__init__` / `__repr__` / `__eq__` for free, IDE autocomplete on field access, mypy validation on field types, and a single source of truth for what the data structure contains. Raw dicts give you none of this. The migration path: raw dict → TypedDict (adds type checking) → dataclass (adds full type safety + methods). |
| **Assessment** | ✅ Sound. The CLAUDE.md should include this hierarchy: Pydantic for external input validation, dataclass for internal domain objects, TypedDict for dict-shaped API responses. Never raw dict for structured data. |
| **Relevance** | 🔴 Direct — specifies the data modeling hierarchy. |
| **Adopt?** | ✅ Yes — CLAUDE.md includes data modeling hierarchy. |

### P32.4 — Protocol Over ABC for Duck-Typed Interfaces

| Field | Value |
|-------|-------|
| **Source** | mypy documentation, Python typing guides |
| **Practice** | Use `typing.Protocol` to define interfaces when you want structural subtyping (duck typing with type safety). Protocol says "any object with these methods/attributes satisfies this type" without requiring inheritance. Use `ABC` only when you need shared implementation (template method pattern). Protocol is strictly for type checking; ABC is for shared behavior. |
| **Reasoning** | Protocol gives you the benefits of interfaces in typed languages while preserving Python's duck typing philosophy. AI tends to use concrete classes and inheritance when Protocol would be more appropriate — this is a code review check point. |
| **Assessment** | ✅ Sound. Include in CLAUDE.md: "Prefer Protocol over ABC for defining interfaces. Use ABC only when the base class provides shared implementation." |
| **Relevance** | 🟡 Medium — important for larger projects. |
| **Adopt?** | ✅ Yes — CLAUDE.md guidance. |

### P32.5 — Explicit Imports, No Wildcard, No Circular

| Field | Value |
|-------|-------|
| **Source** | PEP 8, ruff import rules, Python community consensus |
| **Practice** | Always use explicit imports (`from module import ClassName`), never wildcard (`from module import *`). Organize imports in standard order (stdlib → third-party → local). No circular imports — if module A imports from module B and B imports from A, the architecture is wrong (restructure, extract shared types to a common module, or use TYPE_CHECKING for type-only imports). Use `__all__` in `__init__.py` to define the public API. |
| **Reasoning** | Wildcard imports hide where names come from, making code harder to understand and refactor. Circular imports are always a sign of poor module boundaries. `__all__` makes the public interface explicit — essential for progressive disclosure (P31.2). AI frequently creates circular imports when adding cross-module functionality because it doesn't consider the dependency graph. |
| **Assessment** | ✅ Sound. Ruff's isort rules handle import ordering automatically. Circular import detection should be a CI check. `__all__` in every `__init__.py` should be a CLAUDE.md convention. |
| **Relevance** | 🔴 Direct — import hygiene is automated + enforceable. |
| **Adopt?** | ✅ Yes — ruff handles formatting; CLAUDE.md requires `__all__` in `__init__.py`. |

### P32.6 — Comprehensive Error Handling: No Bare Except, No Silent Failures

| Field | Value |
|-------|-------|
| **Source** | PEP 8, Clean Code, AI code smell studies |
| **Practice** | Never use bare `except:` — always catch specific exceptions. Never silently swallow exceptions (`except SomeError: pass`). Use custom exception classes for domain errors. Log or re-raise with context. AI-generated code commonly produces incomplete error handling: empty catch blocks, overly broad exception types, and missing error cases (especially in async code). |
| **Reasoning** | Silent failures are the hardest bugs to diagnose. AI produces them because incomplete error handling avoids the complexity of deciding what to do on failure — it's the path of least resistance. Every `except` block should either handle the error meaningfully, log it and re-raise, or convert it to a domain-appropriate exception. |
| **Assessment** | ✅ Sound. Ruff catches bare `except:` (E722) and some empty handlers. The anti-slop rubric should include "error handling completeness" as a dimension: does every error path either handle, log+reraise, or convert the exception? |
| **Relevance** | 🔴 Direct — partially automated (ruff), partially LLM-judged. |
| **Adopt?** | ✅ Yes — ruff rules + anti-slop dimension. |

### P32.7 — Python-Specific Deterministic Quality Stack

| Field | Value |
|-------|-------|
| **Source** | Python ecosystem consensus, cookiecutter design |
| **Practice** | The complete deterministic quality stack for Python 3.12+: **ruff** (formatting + linting, replaces black + isort + flake8 + pylint), **mypy --strict** (type checking), **pytest + pytest-cov** (testing + coverage), **cognitive complexity plugin** (complexity threshold), **bandit or ruff security rules** (security scanning). All run in CI on every PR. All configured in pyproject.toml. PostToolUse hook runs ruff + mypy after every file edit. |
| **Reasoning** | This stack catches Level 1-2 quality issues (P30.5) deterministically — no LLM judgment needed. It's the foundation the stochastic anti-slop gates build on. The key principle: deterministic gates should catch everything they can, so the LLM reviewer can focus on the things only a language model can judge (naming, domain language, architectural fit). |
| **Assessment** | ✅ Sound. The cookiecutter must ship with this entire stack pre-configured in pyproject.toml, with CI pipeline templates and PostToolUse hooks ready to go. |
| **Relevance** | 🔴 Direct — specifies the cookiecutter's quality tooling. |
| **Adopt?** | ✅ Yes — all tools pre-configured in cookiecutter output. |

---

## Category 33: Cognitive Load Theory Applied to Code Design

> The psychological science that explains why reading unfamiliar code is exhausting and what code design decisions directly mitigate that exhaustion. This is the theoretical foundation for everything in Categories 30-32.

### The Core Science

**Miller's Law (1956):** Working memory holds ~7±2 chunks of information simultaneously. But the critical update from Cowan (2001): the real capacity is closer to **3-4 chunks** for unfamiliar material. The less familiar you are with the domain, the fewer chunks you can hold. This directly explains Dan's experience: "I can hold at max 7 things... the more unfamiliar I am, the fewer I can hold."

**Chunking:** The size of a "chunk" is subjective — it depends on the reader's existing knowledge. For an experienced Python developer, `@dataclass` is one chunk. For a newcomer, it's several: "what's a decorator? what's a dataclass? what fields does it have?" Familiar patterns compress into single chunks; unfamiliar ones expand into many.

**Cognitive Load Theory (Sweller, 1988)** breaks mental effort into three types:

1. **Intrinsic load** — the irreducible complexity of the problem itself. A distributed consensus algorithm IS complex; you can't make it simple without losing its essence. This maps to Fred Brooks's "essential complexity."

2. **Extraneous load** — the unnecessary mental effort imposed by how the code is written, organized, and presented. Bad names, deep nesting, hidden side effects, inconsistent patterns, scattered logic. This maps to Brooks's "accidental complexity." **This is the enemy. Every code design decision should aim to minimize this.**

3. **Germane load** — the productive mental effort spent building lasting understanding. Learning the domain model, recognizing patterns, building intuition about the codebase. This is the "good" cognitive load — we want to redirect freed capacity toward this.

**The thesis of cognitive load theory applied to code: minimize extraneous load so that the reader's limited working memory is available for intrinsic and germane processing.**

### P33.1 — Every Code Decision Is a Cognitive Load Decision

| Field | Value |
|-------|-------|
| **Source** | Cognitive Load Theory (Sweller), zakirullin/cognitive-load (GitHub, 4.8K stars), thevaluable.dev analysis |
| **Practice** | Every code design decision either adds or removes extraneous cognitive load. Concrete sources of extraneous load in code: (1) Poor naming forces the reader to build a mental mapping from arbitrary symbols to meaning. (2) Deep nesting forces the reader to maintain a stack of conditions. (3) Long functions force the reader to hold many variables and states simultaneously. (4) Hidden side effects force the reader to trace execution paths outside the current function. (5) Inconsistent patterns force the reader to re-learn conventions within the same codebase. (6) Scattered logic forces the reader to jump between files to understand a single concept. (7) Unnecessary abstraction forces the reader to dereference indirection that adds no value. |
| **Reasoning** | The burnout Dan describes is exactly what happens when extraneous load exceeds working memory capacity. The reader's brain isn't tired from the PROBLEM — it's tired from the PRESENTATION. A complex algorithm wrapped in clear abstractions with good names is LESS tiring to read than a trivial algorithm wrapped in clever tricks and poor naming. |
| **Assessment** | ✅ Sound and empirically validated. This reframes our entire quality system: every practice in Categories 30-32 is justified by its cognitive load impact. Naming quality reduces extraneous load. Small functions reduce extraneous load. Type hints reduce extraneous load (the reader doesn't have to guess types). Progressive disclosure reduces extraneous load. Consistent patterns reduce extraneous load. |
| **Relevance** | 🔴 Direct — the theoretical foundation for our quality system. |
| **Adopt?** | ✅ Yes — frame all quality guidance through cognitive load lens. |

### P33.2 — "Hand-Holding" Code: Design for Sequential Comprehension

| Field | Value |
|-------|-------|
| **Source** | Cognitive load research, progressive disclosure principle, code readability studies |
| **Practice** | Code should be readable top-to-bottom without requiring the reader to jump around. Specific techniques: (1) **Put the "what" before the "how"** — function signature and docstring tell you what it does; implementation shows how. (2) **Early returns / guard clauses** — handle edge cases first, then the happy path. The reader can discard edge cases from working memory once past the guard. (3) **One level of abstraction per function** — a function should either orchestrate (call other functions) OR implement logic, never both. (4) **Colocate related code** — helpers used by only one function should be near that function, not in a separate utils.py. (5) **Introduce variables for intermediate results** — `visible_names = neighbors.not('.hidden').data('name')` is easier than chaining everything in one expression. |
| **Reasoning** | This is literally hand-holding: each line prepares the reader for the next. When you introduce a variable with a descriptive name, you're creating a chunk that the reader can carry forward. When you use guard clauses, you're letting the reader discard conditions. When you keep one level of abstraction, you're keeping all chunks at the same size. The reader never has to zoom in and out. |
| **Assessment** | ✅ Sound. These should be embedded in our CLAUDE.md as writing conventions the AI follows and the reviewer checks for. "Write code that can be read top-to-bottom. Use guard clauses. Name intermediate results. Keep one level of abstraction per function." |
| **Relevance** | 🔴 Direct — specifies how the AI should write code for human reviewers. |
| **Adopt?** | ✅ Yes — CLAUDE.md conventions for readable code flow. |

### P33.3 — Familiarity Reduces Chunk Size: Use Conventions and Patterns Readers Already Know

| Field | Value |
|-------|-------|
| **Source** | Miller's chunking theory, zakirullin analysis, Carlos Schults "idiomatic code" |
| **Practice** | Familiar patterns compress into single chunks. Unfamiliar ones expand into many. Implications: (1) **Idiomatic Python** — follow PEP 8, use Pythonic constructs (list comprehensions, context managers, generators). Non-idiomatic code triggers "wait, what is this?" and expands a single-chunk pattern into many. (2) **Consistent patterns across the codebase** — if you use dataclasses for configuration in one module, use them everywhere. If you use Protocol for interfaces, don't switch to ABC in another module. (3) **Standard project structure** — src layout, tests mirror src, conftest.py at test root, pyproject.toml for all config. Readers who've seen this structure before can navigate it as one chunk. (4) **Avoid "clever" code** — every clever trick incurs a learning penalty for every future reader. "Familiarity is not the same as simplicity. They feel the same but for very different reasons." |
| **Reasoning** | The zakirullin/cognitive-load repo (4.8K GitHub stars) makes this point brilliantly: a developer who wrote the code thinks it's clear because they have familiarity. But familiarity is personal — it doesn't transfer. Only genuine simplicity transfers. Standard patterns have the advantage of being familiar to MANY readers, so they compress into small chunks for the widest audience. |
| **Assessment** | ✅ Sound. Our CLAUDE.md should say: "Follow PEP 8 and Pythonic idioms. Use consistent patterns across the codebase. Prefer standard library and well-known patterns over clever solutions. If you find yourself writing a comment to explain a clever trick, replace the trick with a clear but boring implementation." |
| **Relevance** | 🔴 Direct — specifies conventions for cognitive load reduction. |
| **Adopt?** | ✅ Yes — CLAUDE.md conventions. |

### P33.4 — The 40-Minute Confusion Test (zakirullin)

| Field | Value |
|-------|-------|
| **Source** | zakirullin/cognitive-load |
| **Practice** | "Once you onboard new people on your project, try to measure the amount of confusion they have (pair programming may help). If they're confused for more than ~40 minutes in a row — you've got things to improve in your code." |
| **Reasoning** | This is a practical, measurable heuristic for extraneous cognitive load. If a competent developer can't orient themselves within 40 minutes, the problem is the code, not the developer. Applied to AI: if a fresh Claude Code session can't understand the codebase well enough to make productive changes within its first few tool calls, the codebase architecture needs improvement. |
| **Assessment** | ✅ Sound as a heuristic. We can't measure this directly in our cookiecutter, but we can use it as a design principle: "The codebase should be navigable by a fresh agent session within minutes. Clear module structure, __init__.py exports, and CLAUDE.md guidance make this possible." |
| **Relevance** | 🟡 Medium — a useful design principle rather than an enforceable gate. |
| **Adopt?** | ✅ Yes — as design philosophy, not as a gate. |

### P33.5 — Decision Fatigue: Reduce the Number of Decisions the Reader Must Make

| Field | Value |
|-------|-------|
| **Source** | Cognitive load research, coding conventions analysis |
| **Practice** | Every ambiguity in code forces a decision: "What type is this? What does this function return? Is this parameter optional? Where is this defined? What does this abbreviation mean?" Each decision consumes working memory. Techniques to eliminate decisions: (1) **Type hints eliminate "what type is this?"** (2) **Descriptive names eliminate "what does this mean?"** (3) **Consistent conventions eliminate "how is this done here?"** (4) **__all__ exports eliminate "what's the public API?"** (5) **Failing-to-passing checklists eliminate "what's left to do?"** |
| **Reasoning** | Decision fatigue accumulates. By the time a reader has made 20 micro-decisions about types, names, and conventions, they have no working memory left for the actual logic. This is why type-hinted, well-named, consistently-structured code FEELS easier even when the underlying logic is complex — the extraneous decisions have been pre-made by the code author. |
| **Assessment** | ✅ Sound. This ties together why type hints (D56), naming quality (P30.2), consistent conventions (P33.3), and dicts-vs-dataclasses (D55) ALL reduce cognitive load through the same mechanism: eliminating micro-decisions the reader would otherwise have to make. |
| **Relevance** | 🔴 Direct — unifying theory that explains WHY all our quality practices work. |
| **Adopt?** | ✅ Yes — use as the explanatory framework in CLAUDE.md and documentation. |

### P33.6 — Extraneous Load Checklist for Code Review

| Field | Value |
|-------|-------|
| **Source** | Synthesized from cognitive load theory + code quality research |
| **Practice** | The reviewer should ask these questions, each targeting a specific source of extraneous cognitive load: (1) **Can I understand what this function does from its name and signature alone?** (If no → naming/typing problem) (2) **Can I read this function top-to-bottom without jumping to another file?** (If no → scattered logic) (3) **Are there more than 3 levels of nesting?** (If yes → flatten with guard clauses or extraction) (4) **Does this function do more than one thing?** (If yes → split) (5) **Are there any "wait, what?" moments?** (If yes → naming, cleverness, or missing context problem) (6) **Does this code use the same patterns as the rest of the codebase?** (If no → inconsistency) (7) **Could a developer unfamiliar with this module understand the change without reading unrelated files?** (If no → coupling or missing abstraction) |
| **Reasoning** | Each question maps to a specific source of extraneous cognitive load identified by the theory. This checklist can be used by both human reviewers and LLM-as-judge gates. It turns the abstract concept of "cognitive load" into concrete, answerable questions. |
| **Assessment** | ✅ Sound and actionable. This checklist should be part of our anti-slop rubric's stochastic (LLM-judged) tier. The LLM reviewer runs through these questions for every PR. |
| **Relevance** | 🔴 Direct — specifies the cognitive load review checklist. |
| **Adopt?** | ✅ Yes — include in anti-slop rubric as the "readability" dimension. |

---

## Category 34: Repo Mental Model & Documentation Design (Learning Science)

> How to make it as easy as possible for a new user (human or AI) to understand what they're getting into. Draws on cognitive psychology, instructional design, and developer documentation best practices.

### The Learning Science Foundation

**Ausubel's Advance Organizers (1960s):** Before presenting detailed new information, give learners an organizational framework that connects to what they already know. The advance organizer bridges existing knowledge and new content. In a repo: before diving into code, give the reader a map of the territory.

**Vygotsky's ZPD / Bruner's Scaffolding (1970s):** Learning happens most effectively in the zone between "can do alone" and "can't do even with help." Scaffolding provides temporary support structures gradually removed as competence grows. The "I do, We do, You do" pattern: show the complete picture, walk through it together, then let the learner work independently.

**Paivio's Dual Coding Theory (1986):** The brain has two processing channels — verbal (words) and visual (images). Information presented in BOTH channels is retained significantly better than either alone. A diagram + explanation > explanation alone. **This is the scientific justification for visuals in documentation.**

**Sweller's Cognitive Load Theory (Category 33):** Applied to docs: reduce extraneous load (confusing layout, unclear language, wrong information order) so the reader's working memory is available for germane load (building their mental model of the system).

### P34.1 — The ARCHITECTURE.md File: High-Level Mental Map

| Field | Value |
|-------|-------|
| **Source** | matklad (Alex Kladov, Rust developer) |
| **Practice** | Add ARCHITECTURE.md next to README. Describes high-level architecture ONLY — things unlikely to frequently change. "It takes 2x more time to write a patch if unfamiliar, but 10x more time to figure out WHERE to change." Keep it short. Only include things that change rarely. |
| **Reasoning** | The "10x to find where" insight is key. New developers (and AI agents) don't struggle with HOW — they struggle with WHERE. ARCHITECTURE.md is Ausubel's advance organizer applied to code. |
| **Assessment** | ✅ Sound. Cookiecutter generates ARCHITECTURE.md template: module hierarchy, what each module does, how data flows, what conventions are used. Under 200 lines. Updated rarely. |
| **Relevance** | 🔴 Direct — cookiecutter deliverable. |
| **Adopt?** | ✅ Yes — generate ARCHITECTURE.md template. |

### P34.2 — C4 Model: Progressive Disclosure in Architecture Diagrams

| Field | Value |
|-------|-------|
| **Source** | Simon Brown (C4 Model) |
| **Practice** | Four zoom levels: **Context** (system + external interactions), **Container** (major building blocks), **Component** (inside a container), **Code** (detailed diagrams — rarely needed). Each level is a separate diagram. Read from Context inward, stopping at needed detail. Each diagram: 5-7 elements max (Miller's Law). |
| **Reasoning** | This IS progressive disclosure applied to visual docs. New user starts at Context ("it's a CLI that talks to GitHub and a local database"). Needs more? Container level ("parser, planner, executor modules"). Only go to Component when modifying internals. |
| **Assessment** | ✅ Sound. For our cookiecutter: C4 Levels 1-2 as Mermaid diagrams in ARCHITECTURE.md. |
| **Relevance** | 🔴 Direct — visual documentation format. |
| **Adopt?** | ✅ Yes — Mermaid diagrams at C4 Levels 1-2. |

### P34.3 — Dual Coding: Every Major Concept Gets Words AND a Visual

| Field | Value |
|-------|-------|
| **Source** | Paivio's Dual Coding Theory (1986), Caviglioli (2019) |
| **Practice** | Every major concept should have a prose explanation AND a diagram. Workflow = text + flowchart. Module relationships = list + dependency graph. Data flow = narrative + sequence diagram. The visual doesn't replace text — they encode differently in the brain and reinforce each other. Critical: don't show text and talk simultaneously (both compete for the phonological loop). Show diagram THEN explain, or explain THEN show. |
| **Reasoning** | The brain processes words and images via separate subsystems. When both activate, the brain has two retrieval paths instead of one. Empirically validated across decades of research. |
| **Assessment** | ✅ Sound. Documentation pairs prose with Mermaid diagrams for: module architecture, workflow (Plan→Work→Assess→Compound), data flow, and anti-slop pipeline. Each diagram: simple (5-7 elements) + short prose explanation. |
| **Relevance** | 🔴 Direct — documentation format standard. |
| **Adopt?** | ✅ Yes — prose + diagram for every major concept. |

### P34.4 — Scaffolded Onboarding: "I Do, We Do, You Do"

| Field | Value |
|-------|-------|
| **Source** | Bruner's scaffolding theory, developer onboarding research |
| **Practice** | Structure docs as a scaffolded learning path: **Level 1 (I do — show):** One-command quickstart. "Run this, see output." < 5 minutes. **Level 2 (We do — guided):** Tutorial that modifies something simple. Introduces key concepts in context. **Level 3 (You do — independent):** Reference docs for when they know what they want but need specifics. API docs, config reference, troubleshooting. |
| **Reasoning** | Most READMEs try to do all three at once and fail at all of them. Separating them lets each section do its job. The quickstart MUST be copy-pasteable with zero decisions — proving setup works before investing in learning. |
| **Assessment** | ✅ Sound. Three-section README: Quickstart (< 5 min, proves it works), Tutorial (guided first project), Reference (everything else). |
| **Relevance** | 🔴 Direct — README structure. |
| **Adopt?** | ✅ Yes — three-section scaffolded README. |

### P34.5 — Advance Organizers: Tell Them What They're About to Learn

| Field | Value |
|-------|-------|
| **Source** | Ausubel (1960s), instructional design research |
| **Practice** | Before detailed information, provide: (1) What the system IS in one sentence. (2) The 3-5 core concepts they'll need. (3) How those concepts relate (simple diagram). (4) Connection to what they already know ("If you've used cookiecutter before, this is similar but with X"). This goes at the TOP of README, before quickstart. |
| **Reasoning** | Learners who receive an advance organizer retain significantly more from subsequent instruction. The organizer creates "mental hooks" for new information. Without it, details float disconnected in working memory. With it, each detail snaps into place. |
| **Assessment** | ✅ Sound. README opens with: one-sentence description, "Core Concepts" box (3-5 terms with one-line definitions), relationship diagram, THEN quickstart. |
| **Relevance** | 🔴 Direct — README opening section. |
| **Adopt?** | ✅ Yes — advance organizer at top of README. |

### P34.6 — ADRs for "Why" Documentation

| Field | Value |
|-------|-------|
| **Source** | Michael Nygard (ADR pattern) |
| **Practice** | ADR documents: context, decision, alternatives, consequences. Answers "Why was it done this way?" Numbered, immutable (superseded not edited), checked into git. Code shows WHAT. Comments show HOW. ADRs show WHY. |
| **Reasoning** | When a new developer asks "Why dataclasses instead of Pydantic for internal types?" the ADR explains reasoning. Without ADRs, this knowledge lives only in heads. AI agents also benefit — when modifying architecture, an agent that reads ADRs understands constraints to preserve. |
| **Assessment** | ✅ Sound. Cookiecutter includes `project/decisions/` with ADR template. Our D1-D60 decision log is already ADR-like. |
| **Relevance** | 🔴 Direct — cookiecutter deliverable. |
| **Adopt?** | ✅ Yes — `project/decisions/` directory with ADR template. |

### P34.7 — Complete README Template (Synthesized)

| Field | Value |
|-------|-------|
| **Source** | Synthesized from learning science + documentation research |
| **Practice** | **(1) Advance Organizer** — One-sentence description. Core Concepts box (3-5 terms). Relationship diagram (Mermaid). "If you've used X, this is like Y but with Z." **(2) Quickstart** — Prerequisites. One copy-paste command block. Expected output. < 5 minutes. Zero decisions. **(3) Tutorial** — Guided first task. Step-by-step with WHY each step matters. Introduces 2-3 core concepts in context. **(4) Architecture** — Link to ARCHITECTURE.md. C4 Level 1-2 diagrams. **(5) Reference** — Configuration, CLI, file structure, troubleshooting. **(6) Contributing** — How to contribute. Link to ADRs. Code quality standards. |
| **Assessment** | ✅ Sound. This is the complete README template the cookiecutter generates. Each section serves a different reader at a different stage. No section tries to do two jobs. |
| **Relevance** | 🔴 Direct — specifies the README template. |
| **Adopt?** | ✅ Yes. |

### P34.8 — Mermaid Diagrams: Rich Visual Encoding Standard

| Field | Value |
|-------|-------|
| **Source** | Mermaid documentation, dual coding theory (Paivio), GitHub rendering capabilities |
| **Practice** | Mermaid supports multiple independent visual channels — use them to encode information at high density. A monochrome boxes-and-arrows diagram wastes the visual channel. Our standard: architecture diagrams use at least color + shape + line style to encode three dimensions simultaneously. All GitHub-compatible via `classDef`/`linkStyle` (NOT CSS `<style>` blocks, which don't render in GitHub). **Node fill color** → component type or layer (blue = data, green = business logic, orange = API). **Node shape** → architectural role (rectangle = module, diamond = decision, circle = external, hexagon = data store). **Stroke weight** → importance (thick = public API, thin = internal). **Line style** (stroke-dasharray) → relationship type (solid = direct dependency, dashed = async/optional, dotted = event). **Line weight** → coupling strength (thick = high traffic, thin = loose). Include a legend in every diagram using color/shape encoding. Maintain a reusable `classDef` palette block across all project diagrams for consistency. 5-7 elements max per diagram. |
| **Reasoning** | Within the visual channel, there are SUB-channels (color, shape, size, line style) processed in parallel by the brain. A diagram using 4 visual dimensions conveys 4x the information of monochrome at similar cognitive load — the channels reinforce, they don't compete. This is how maps work: color = terrain, line weight = road importance, shape = landmark type, line style = boundary. One map view encodes what would take paragraphs. Renders natively in GitHub/GitLab. Plain text = diffable, versionable, AI-editable. Solves "diagrams go stale" — updated in the same PR as code. Choose a colorblind-safe palette (avoid red/green only distinctions). |
| **Assessment** | ✅ Sound. Cookiecutter includes a Mermaid style guide: color palette, shape conventions, line meanings, and a reusable `classDef` block. The style guide itself is a convention (P33.3) — once readers learn "blue = data layer," every future diagram is instantly readable. |
| **Relevance** | 🔴 Direct — diagram styling standard + style guide deliverable. |
| **Adopt?** | ✅ Yes — rich visual encoding with standardized conventions. |

---

## Resolved: Development Process — Zoom-Based Progressive Concretization (D74, D75)

> **Status:** Resolved. Formerly Q12.

### The Process

At any point, you're at a **zoom level** (outer = purpose, inner = implementation). At that level, you run one loop:

1. **Identify** the 3-4 most important open questions at this level
2. **Self-check** (D75): "Can I answer these from higher-level artifacts?" If yes → resolve without prompting the human. If no → formulate the SPECIFIC uncertainty and escalate as one focused question.
3. **Resolve** — produce artifacts: advance organizer, ARCHITECTURE.md, type signatures, tests, code. The artifact at each level IS documentation — it's the tool for thinking, not an afterthought.
4. **Verify** consistency with all levels above. If inconsistent → zoom back up to where the conflict lives.
5. **Zoom in** to the next level, where resolutions above reveal the next questions.

**When no questions remain, implementation is mechanical.** Zoom back out after implementation to verify all documentation is still accurate. Compound step: codify learnings.

### Key Properties

- **One loop, not named steps.** The loop repeats at every zoom level. You're never "in step 3."
- **Human involvement is pull-based.** The agent works autonomously and pulls the human in only when it hits genuine ambiguity the higher-level artifacts don't resolve. No routine checkpoints.
- **The D75 self-check gate is the critical mechanism.** Before escalating, the agent asks: "Can I derive the answer from decisions already made?" This means the quality of outer zoom levels directly determines how autonomous inner levels can be. Precise purpose = few interruptions. Vague purpose = constant escalation. This is P16.1 (specification bottleneck) made operational.
- **Documentation is never an afterthought.** Each zoom level's artifact IS documentation — it was the tool for thinking. By the time implementation is done, the docs already exist.
- **Same process for new repos and new features.** A new repo starts at the outermost zoom. A new feature starts at whatever level has unresolved questions.
- **Model routing follows zoom level (D72).** Outer = Opus (judgment). Inner = cheaper models (mechanical). The zoom level IS the routing signal.
- **Working memory is never exceeded (P33.5).** 3-4 questions per level. Focused questions to the human, not batch reviews.

### Grounding in Research

| Principle | How it manifests |
|-----------|-----------------|
| Ausubel advance organizers (P34.5) | Each level's artifact IS the advance organizer for the next level |
| Bruner scaffolding (P34.4) | Each level scaffolds the one below it |
| Paivio dual coding (P34.3) | Diagrams produced at each level alongside prose |
| C4 progressive disclosure (P34.2) | The zoom levels ARE C4 levels |
| Cowan 3-4 chunks (P33.1) | Never more than 3-4 questions per level |
| Decision fatigue (P33.5) | Self-check gate prevents unnecessary human decisions |
| Implementation should be boring (P28.3) | If all levels above are resolved, implementation is mechanical |
| Specification bottleneck (P16.1) | Quality of outer levels determines autonomy of inner levels |
| Human mental energy (D70) | Pull-based involvement minimizes human cognitive draw |

---

## Cross-Cutting Concern: Token Efficiency Through Prompt Alignment (D65)

> Not a category of practices but an economic principle that affects all multi-agent architecture decisions.

**The problem:** If the dev agent writes code that fails 3 of 6 anti-slop dimensions, you pay for: (1) dev agent generating code, (2) review agent(s) reading and grading, (3) dev agent reading feedback and rewriting, (4) review agent(s) re-checking. That's 3-5x the token cost of getting it right the first time. In a Ralph loop running overnight, this compounds dramatically.

**The principle:** The dev agent's context should be aligned with what checkers expect — but NOT via a checklist that bloats context.

**The tension (D65 vs D11/P25.3):** Adding a "Quality Gates Summary" to the dev prompt saves tokens on failed review cycles BUT adds tokens to EVERY invocation. If the dev agent passes review 90% of the time, those extra tokens are pure overhead on 9/10 runs. Context length alone degrades performance (P25.3). The cure can be worse than the disease.

**The resolution — conventions, not checklists:** Instead of a "here's what will be checked" section, write CLAUDE.md conventions that naturally produce code passing review. "Use dataclasses, not dicts, for known shapes" is one line that's simultaneously good coding guidance AND review-failure prevention. The dev agent doesn't need to know it's being checked — it just needs to follow good conventions.

**Where each type of quality feedback lives:**
- **Deterministic gates** (ruff, mypy, complexity) → PostToolUse hooks give instant feedback. Zero context cost. The dev agent sees errors and self-corrects in the same session.
- **Coding conventions** (naming, types, module patterns) → CLAUDE.md, ~10-15 concise lines. Small context cost, prevents the most common review failures.
- **Stochastic dimensions** (architectural fit, domain language, unnecessary duplication) → Reviewer prompt only. The dev agent CAN'T fully prevent these — they require system-level judgment. Don't waste dev context on them.
- **Persistent failure patterns** → When the compound step identifies a recurring review failure, promote ONE targeted line to CLAUDE.md conventions. Not a growing checklist — a curated, minimal set.

**The compound step economics (still valid):** Every convention added is simultaneously a quality improvement AND a future token savings. But the discipline is: add conventions ONLY for persistent patterns (D27: 3+ recurrences), and REMOVE conventions when they become unnecessary (the codebase has enough examples that the agent follows the pattern without being told). The CLAUDE.md should get SHORTER over time as the codebase itself becomes the teacher.

**Connections:**
- D27 (recurring learnings → deterministic gates) = eliminate the review cycle entirely for known patterns
- D47 (compound step) = the mechanism by which token savings accumulate over time
- P15.3 (recurring review comments → lint rules) = Boris Cherny's version of the same principle
- P16.11 (harness > model, 78% vs 42%) = a well-prompted dev agent IS a better harness
- P28.1 (compound engineering) = each cycle makes the next cycle cheaper

---

## Cross-Cutting Principle: Build the Theory, Instrument for Reality (D69)

> Applies to EVERY research-backed component in the system.

**The principle:** Every design choice based on research ships with its full recommended structure from day one. Don't plan to "add later" — later never comes, and structural features can't be easily retrofitted. BUT treat every research-backed design as a hypothesis under active test.

**Every component ships with four things:**

1. **The structure the research recommends** — build it fully, don't water it down preemptively
2. **A retrospective prompt with pointed questions** — run periodically to detect whether the structure is earning its keep
3. **Clear criteria for what "broken" looks like** — so you notice failure instead of just accumulating unused structure
4. **A documented fallback** — if it doesn't work, simplify AND capture WHY so the next attempt is better-informed

**Applied to each major component:**

| Component | "Broken" Looks Like | Retrospective Questions |
|-----------|-------------------|----------------------|
| Learning store (D68) | Entries accumulate but never referenced; counters stuck at zero; type tags don't map to real patterns; file grows without pruning | Are counters being updated? Are type tags useful? Are entries retrieved at the right times? Is anyone pruning? |
| Anti-slop rubric dimensions (D50) | A dimension never flags anything; a dimension flags everything (false positive noise); reviewers ignore a dimension's output | Are all 6 dimensions producing actionable findings? Which are never triggered? Which are always overridden? |
| Process ordering / cognitive scaffolding (Q12) | Steps feel like busywork rather than scaffolding; humans skip steps routinely; later steps don't benefit from earlier ones | Does each step's output actually help with the next step? Which steps get skipped and why? Where does the process feel like friction vs. flow? |
| CLAUDE.md conventions (D65) | Conventions that the agent follows anyway (no value added); conventions that the agent ignores despite being listed; the file grows without pruning | Are conventions preventing review failures? Which ones are redundant with the codebase's own examples? Which are ignored? |
| Mermaid style guide (D63, Q13) | Diagrams don't use the defined encoding channels; readers don't understand the visual conventions; diagrams look good but don't convey more info than plain boxes | Are the visual channels being used? Do readers understand them without the legend? Are diagrams more informative than monochrome alternatives? |
| Compound step (D47) | Codification happens but learnings are never referenced; learnings are referenced but don't change behavior; the step is routinely skipped under time pressure | Is codification happening? Are new learnings changing future agent behavior? Is anyone reading retrospective output? |
| Zoom process (D74) | Human prompted at inner levels for things derivable from outer artifacts (spec quality problem); agent proceeds confidently but fails review (D75 self-check too permissive); zoom levels feel bureaucratic not progressive; artifacts accumulate but go unread; loops back to higher levels don't happen when they should | Does each zoom level's artifact help resolve questions at the next level? Are there levels that feel like busywork? Does D75 escalate too often or too rarely? Are loops back happening when needed? Are artifacts being read? |

---

## Cross-Cutting Principle: Human Mental Energy as the Scarce Resource (D70, D71)

> "AI is cheap, human input is expensive. But the cost of human input is not measured in time — it's measured in mental energy."

### The Principle

Every human touchpoint in the system — prompts for input, documentation to read, architecture to understand, code to review, decisions to make — depletes a finite, non-renewable-within-session resource: cognitive capacity. The system must treat every interaction with the human as a **draw on a limited budget** and optimize ruthlessly to minimize that draw.

This is NOT about making things faster. It's about making them **less mentally exhausting.** A 5-minute task that requires intense concentration depletes more capacity than a 20-minute task that flows naturally. The metric is mental energy consumed, not clock time elapsed.

### Measuring Cognitive Load (What the Science Says)

**NASA-TLX (Task Load Index):** The most widely used subjective workload measure (4,400+ citations). Six subscales: mental demand, physical demand, temporal demand, performance, effort, frustration. However: recent research (Bolton et al., 2023) found the overall composite score is "mathematically meaningless." Individual subscales remain valid. For our purposes: **mental demand and frustration** are the two subscales that matter most.

**Practical proxy measures for our system:**
- **Steps skipped** — when humans routinely skip a workflow step, it's extraneous load they're refusing to pay
- **Questions asked** — when humans ask "what does this mean?" or "where is X?" the documentation has failed
- **Review passes needed** — when code requires 3+ review cycles, either the dev prompt or the quality gates are creating unnecessary iteration
- **"Wait, what?" moments** — when a human reading code or docs has to stop and re-read, that's a measurable extraneous load event (P33.6)
- **Decision fatigue indicators** — when a human starts accepting suggestions without evaluating them, they've exceeded capacity

**The honest truth:** There's no great objective measure of cognitive load that's practical for our context. The best approach is Sweller's framework (intrinsic/extraneous/germane) applied qualitatively via retrospective questions, combined with the behavioral proxies above. The retrospective prompt for each component (D69) IS our measurement instrument.

### Five SE Principles That Flip (D71)

When human mental energy is the scarce resource and AI computation is cheap:

**1. "Working software over comprehensive documentation" → Good docs save more mental energy than they cost.**

The Agile Manifesto assumed documentation was expensive to write and maintain. With AI, documentation is cheap to produce and cheap to keep updated (Mermaid diagrams in the same PR, AI-generated docstrings, ADRs written by the agent). But the READING of documentation saves enormous human mental energy by providing advance organizers (P34.5) and reducing "where is X?" questions. The equation has flipped: the cost of writing docs dropped to near-zero while the cost of NOT having docs (human mental energy spent figuring things out) remained constant.

**2. YAGNI partially flips → Upfront cognitive structure IS needed, even if not functionally required yet.**

Traditional YAGNI says don't build features until you need them. But D68 showed: "start simple, add later" for STRUCTURAL features means "never add." If a data structure (learning store entries with IDs and counters) or a documentation convention (ARCHITECTURE.md) reduces future cognitive load, building it now IS needed — the "Ya" in YAGNI is satisfied, just not by a functional requirement. It's satisfied by a cognitive load requirement. YAGNI still applies to FUNCTIONAL features. It does NOT apply to COGNITIVE INFRASTRUCTURE.

**3. "Don't over-engineer" → "Don't under-design."**

Traditional wisdom says the simplest solution that works is the best. But "works" traditionally meant "functions correctly." When you include "is easy for a human to understand, modify, and maintain" in the definition of "works," the simplest FUNCTIONAL solution is often NOT the simplest COGNITIVE solution. A refactor that adds a few more files but dramatically clarifies the mental model is worth doing even though the code "worked" before. When a refactor reduces extraneous cognitive load, it should almost always be done. The cost of the refactor (AI tokens, cheap) is almost always less than the cost of the ongoing cognitive load (human mental energy, expensive).

**4. "Move fast and break things" → "Move thoughtfully and save brains."**

Speed of shipping is not the bottleneck when AI generates code. The bottleneck is human cognitive capacity to review, understand, and steer. Moving fast at the cost of comprehensibility is a false economy — you save AI time and spend human mental energy. Move at the speed of HUMAN COMPREHENSION, not the speed of AI generation.

**5. "Premature optimization is the root of all evil" gains a sibling → "Premature COGNITIVE optimization is the root of all good."**

Knuth was right about performance optimization — don't optimize execution speed before you've profiled. But COGNITIVE optimization (making code easier to understand) should happen as early as possible. The earlier you establish clear naming, consistent patterns, and well-designed interfaces, the less cognitive debt accumulates. Unlike performance debt, cognitive debt compounds silently — you don't get a stack trace when a developer's brain overflows.

### Surfacing Epiphanies: How to Discover Lower-Load Approaches

Sometimes there exists a fundamentally different approach that has dramatically lower extraneous cognitive load — but you don't see it because you're already invested in the current approach. How to surface these:

**1. Plan-phase brainstorming with multiple alternatives (D49 + grill-me):**
Don't let the agent propose ONE plan. Require 2-3 fundamentally different approaches. For each, explicitly ask: "What mental model does the user need to understand this?" The approach with the simplest mental model often wins even if it requires more code.

**2. The "explain it to a newcomer" test:**
During plan review, ask: "If someone unfamiliar with this codebase read this code, how many things would they need to hold in their head simultaneously?" If the answer is > 4 (Cowan's limit), there's likely a simpler mental model hiding behind the current one.

**3. Retrospective epiphany capture:**
After every significant feature, ask: "Now that we've built it, is there a way to restructure it that would be immediately obvious to a newcomer?" This captures the epiphany that comes from hindsight. If the answer is yes, DO THE REFACTOR. AI makes refactoring cheap. Human mental energy makes it worth doing.

**4. Cross-pollination from the learning store:**
Patterns that appear across multiple features may suggest a higher-level abstraction that dramatically simplifies the mental model. The learning store's "strategy" entries (P29.1) can surface these. If three features all solved a similar problem three different ways, there's an epiphany hiding: there should be one way.

**5. "If I were starting over" prompt:**
Periodically ask (in the compound step): "If we were starting this module from scratch today, knowing what we know now, what would we do differently?" If the answer involves a fundamentally simpler mental model, that's an epiphany worth a refactor.

---

## Next Steps

1. ☑ Deep dive on all Tier 1 sources (6 sources, 62+ practices)
2. ☑ Tier 2 source survey (8+ sources, 26+ additional practices)
3. ☑ Discover novel sources (ACE paper, Anthropic harness, GitHub primitives, Dan Shipper, Boris Tane)
4. ☑ Academic paper survey (10 papers across context, memory, evaluation, self-improvement)
5. ☑ Anthropic engineering blog deep dive (6 posts)
6. ☑ Plugin ecosystem analysis (9K+ plugins, feature-dev 89K installs)
7. ☑ Practitioner deep dives (Dan Shipper compound engineering, Boris Tane annotation cycles)
8. ☑ Code quality research (timeless principles + AI-specific failure modes)
9. ☑ Architectural principles for AI-ready codebases (Pocock, Ousterhout, SOLID)
10. ☑ Python-specific code quality practices (type hints, dataclasses, mypy, error handling)
11. ☑ Cognitive load theory applied to code design (Miller, Sweller, Cowan, zakirullin)
12. ☑ Category taxonomy (33 categories → 7 themes)
13. ☑ Complement/conflict map (10 clusters, 8 tensions)
14. ☑ Reasoning audit (131 practices → 3 tiers, 0 unsound)
15. ☑ Documentation & onboarding design (learning science: advance organizers, scaffolding, dual coding)
16. ☐ Ideation session with Dan on findings and architecture implications
17. ☐ Phase 1 architecture design

---

*This is a living document. Updated as research continues.*
