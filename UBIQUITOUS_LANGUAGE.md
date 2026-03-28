# Ubiquitous Language — agentic-cookiecutter

Terms used in developing and maintaining this cookiecutter. These are
cookiecutter-scope terms and do NOT propagate to generated child repos.

---

## Terms

**Cookiecutter scope** — Files and concerns belonging to this repo itself:
`cookiecutter.json`, `hooks/`, `docs/`, `tests/`, `.claude/`. Changes here
affect how generation works.

**Template scope** — Everything inside `{{cookiecutter.project_slug}}/`.
This directory IS the generated project. Changes here affect what generated
repos look like.

**Generation** — The act of running `cookiecutter .` to produce a child repo
from this template. Jinja2 variables are substituted at generation time.

**Child repo** — A project generated from this cookiecutter. Has no ongoing
relationship to this repo (unlike cruft, which tracks drift).

**Drift** — When a child repo diverges from the current cookiecutter template.
Measured with `cruft check`.

**Skill** — A markdown file in `.claude/skills/` that encodes a repeatable
workflow for Claude Code. Lives in template scope; symlinked into cookiecutter
scope.

**Hook script** — A Python file in `hooks/` that runs before or after
cookiecutter generation (`pre_gen_project.py`, `post_gen_project.py`).
These are cookiecutter hooks, NOT Claude Code hooks.

**Claude Code hook** — An entry in `.claude/hooks.json` that triggers a
shell command on Claude Code events (PostToolUse, Stop, PreToolUse).
Distinct from hook scripts.

**Quality gate** — An automated check that must pass before a change is
accepted. Tiers: deterministic (tools) and stochastic (LLM-judged).

**Opt-in feature** — A cookiecutter variable that conditionally includes
content in the generated repo (e.g. `use_hypothesis`). Controlled via
Jinja2 conditionals.

---

## Anti-vocabulary

- ~~plugin~~ when referring to skills → use **skill**
- ~~template variables~~ → use **cookiecutter variables**
- ~~child project~~ → use **child repo**
