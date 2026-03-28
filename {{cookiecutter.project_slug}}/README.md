# {{cookiecutter.project_name}}

{{cookiecutter.description}}

**Core Concepts:** <!-- 3-5 key terms from UBIQUITOUS_LANGUAGE.md -->

```mermaid
graph LR
    A[Input] --> B[{{cookiecutter.project_name}}] --> C[Output]
```

---

## Quickstart

**Prerequisites:** Python {{cookiecutter.python_version}}+, [uv](https://docs.astral.sh/uv/)

```bash
git clone <repo-url>
cd {{cookiecutter.project_slug}}
uv sync
uv run pytest
```

Expected output: all tests pass.

---

## Tutorial

_Walk through the first real task a user would accomplish, explaining WHY at each step._

---

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for module structure and data flow.

---

## Reference

### Configuration

_Document configuration options here._

### CLI

_Document CLI commands here._

### File Structure

```
{{cookiecutter.project_slug}}/
├── src/{{cookiecutter.package_name}}/   # Package source
├── tests/                               # Test suite
├── docs/decisions/                      # Architecture Decision Records
├── docs/learnings/                      # Project learnings log
└── stories/                             # Feature story files
```

### Troubleshooting

_Common issues and solutions._

---

## Contributing

- ADRs in `docs/decisions/` for significant architectural choices
- Code quality: ruff + mypy --strict + pytest required
- See [ARCHITECTURE.md](ARCHITECTURE.md) for conventions
