# CLAUDE.md

## Project
{{cookiecutter.description}}

## Setup
```bash
uv sync
uv run pytest
```

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
