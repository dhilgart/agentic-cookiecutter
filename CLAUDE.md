# CLAUDE.md

Cookiecutter template for Python projects using an agentic coding workflow with Claude Code.

## Project Structure

This is a **forge** — the factory that produces configured workspaces. Three concepts:

- **Forge** (this repo): `cookiecutter.json`, `hooks/`, `docs/`, `tests/`, `.claude/`, this file.
- **Template**: everything inside `{{cookiecutter.project_slug}}/`. This directory IS the generated project. Jinja2 variables like `{{cookiecutter.project_slug}}` get replaced at generation time.
- **Child**: a repo generated from the template via `cookiecutter .`.

Only edit the template when changing what children look like.
Only edit forge files when changing how generation works.
See `UBIQUITOUS_LANGUAGE.md` for full terminology.

## Key Context

Read these before making architectural decisions:

- `docs/phase0/phase1-design-inputs.md` — Complete spec for what to build (80 decisions synthesized)
- `docs/phase0/agentic-workflow-tracker.md` — Decision log with rationale (D1-D80)
- `docs/phase0/phase0-research-catalogue.md` — Research backing (reference, not required reading)

## Conventions

- Python 3.12+. Type hints on everything. `mypy --strict`.
- Use `dataclass` or `TypedDict` for structured data. Never pass `dict` when shape is known.
- Template variables in cookiecutter use `{{cookiecutter.variable_name}}` syntax.
- Jinja2 conditionals for opt-in features: `{% if cookiecutter.use_hypothesis == "yes" %}`.
- Test the cookiecutter by generating a child and verifying it works, not by running template files directly.

## Commit Convention

This forge uses **Conventional Commits** enforced by commitizen + pre-commit.

Valid commit types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.

Format: `type(scope): description` — scope is optional. Never use `review` or other non-standard types.

Examples:
- `feat: add hypothesis toggle to cookiecutter variables`
- `fix(hooks): validate project_slug before generation`
- `docs: update phase0 decision log`

## Cookiecutter Variables

Defined in `cookiecutter.json`. Current variables:

- `project_name` — Human-readable name
- `project_slug` — Directory/package name (auto-derived)
- `package_name` — Python import name (auto-derived)
- `description` — One-line description
- `author_name`, `author_email`
- `python_version` — Default "3.12"
- `use_hypothesis` — "yes" or "no"
- `use_mutmut` — "yes" or "no"

## Setup

```bash
uv sync
uv run pre-commit install --hook-type commit-msg
```

## Commands

```bash
# Run forge tests
uv run pytest

# Generate a child from the template
uv run cookiecutter .

# Generate with defaults (no prompts)
uv run cookiecutter . --no-input

# Test: generate + verify child
cd /tmp && uv run cookiecutter /path/to/this/repo --no-input && cd my-project && uv sync && uv run pytest

# Cruft compatibility check
cruft check
```

## Quality Gates

- `ruff format` and `ruff check` on all Python files (forge and template)
- Children must pass `mypy --strict` and `pytest` after generation
- Hook scripts (`hooks/pre_gen_project.py`, `hooks/post_gen_project.py`) must be tested

## What NOT to Do

- Don't put phase0 research docs inside the template — they stay in the forge.
- Don't hardcode project-specific values in template files — use `{{cookiecutter.variable}}`.
- Don't add Python implementation code to the template `src/` — it generates typed stubs and `__init__.py` exports only.
- Don't install plugins or skills that don't exist yet — verify availability first.
