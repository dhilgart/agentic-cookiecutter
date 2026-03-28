# CLAUDE.md

Cookiecutter template for Python projects using an agentic coding workflow with Claude Code.

## Project Structure

This is a **cookiecutter repo**, not a regular Python project. Two scopes:

- **Cookiecutter scope** (this repo): `cookiecutter.json`, `hooks/`, `docs/`, `tests/`, this file.
- **Template scope** (child repos): everything inside `{{cookiecutter.project_slug}}/`. This directory IS the generated project. Jinja2 variables like `{{cookiecutter.project_slug}}` get replaced at generation time.

Only edit template scope files when changing what generated repos look like.
Only edit cookiecutter scope files when changing how generation works.

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
- Test the cookiecutter by generating a project and verifying it works, not by running template files directly.

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

## Commands

```bash
# Generate a project from the template
cookiecutter .

# Generate with defaults (no prompts)
cookiecutter . --no-input

# Test: generate + verify
cd /tmp && cookiecutter /path/to/this/repo --no-input && cd my-project && uv sync && uv run pytest

# Cruft compatibility check
cruft check
```

## Quality Gates

- `ruff format` and `ruff check` on all Python files (template and cookiecutter scope)
- Generated projects must pass `mypy --strict` and `pytest` after generation
- Hook scripts (`hooks/pre_gen_project.py`, `hooks/post_gen_project.py`) must be tested

## What NOT to Do

- Don't put phase0 research docs inside `{{cookiecutter.project_slug}}/` — they stay in cookiecutter scope.
- Don't hardcode project-specific values in template files — use `{{cookiecutter.variable}}`.
- Don't add Python implementation code to the template `src/` — it generates typed stubs and `__init__.py` exports only.
- Don't install plugins or skills that don't exist yet — verify availability first.
