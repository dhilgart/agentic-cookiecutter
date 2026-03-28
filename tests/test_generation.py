"""Test that cookiecutter generates a valid project structure."""

from pathlib import Path


def test_file_tree_exists(generated_project: Path) -> None:
    """All expected files and directories are generated."""
    expected_files = [
        "CLAUDE.md",
        "ARCHITECTURE.md",
        "README.md",
        "UBIQUITOUS_LANGUAGE.md",
        "pyproject.toml",
        ".claude/settings.json",
        ".claude/hooks.json",
        ".claude/commands/commit-push-pr.md",
        ".claude/skills/plan/SKILL.md",
        ".claude/skills/review/SKILL.md",
        ".claude/skills/review/eval.md",
        ".claude/skills/compound/SKILL.md",
        "src/test_project/__init__.py",
        "tests/conftest.py",
        "docs/decisions/0000-template.md",
        "docs/learnings/learnings.md",
        "docs/instrumentation.md",
        "docs/mermaid-style-guide.md",
        "stories/template.md",
        "stories/done/.gitkeep",
        ".github/workflows/ci.yml",
    ]
    for filepath in expected_files:
        assert (generated_project / filepath).exists(), f"Missing: {filepath}"


def test_no_raw_template_variables(generated_project: Path) -> None:
    """No unrendered cookiecutter variables remain in generated files."""
    for path in generated_project.rglob("*"):
        if path.is_file() and path.suffix in (".md", ".toml", ".json", ".yml", ".py"):
            content = path.read_text()
            assert "{{cookiecutter." not in content, (
                f"Unrendered template variable in {path.relative_to(generated_project)}"
            )


def test_package_name_in_init(generated_project: Path) -> None:
    """__init__.py contains the project description."""
    init_py = generated_project / "src/test_project/__init__.py"
    content = init_py.read_text()
    assert "A test project." in content


def test_pyproject_has_correct_metadata(generated_project: Path) -> None:
    """pyproject.toml has the correct project name and author."""
    pyproject = (generated_project / "pyproject.toml").read_text()
    assert 'name = "test-project"' in pyproject
    assert 'name = "Test Author"' in pyproject
    assert 'email = "test@example.com"' in pyproject


def test_claude_md_under_50_lines(generated_project: Path) -> None:
    """CLAUDE.md must be minimal — under 50 lines per D11."""
    claude_md = (generated_project / "CLAUDE.md").read_text()
    line_count = len(claude_md.strip().splitlines())
    assert line_count < 50, f"CLAUDE.md is {line_count} lines, must be under 50"


def test_hypothesis_excluded_by_default(generated_project: Path) -> None:
    """Hypothesis is not in pyproject.toml when use_hypothesis is 'no'."""
    pyproject = (generated_project / "pyproject.toml").read_text()
    assert "hypothesis" not in pyproject


def test_mutmut_excluded_by_default(generated_project: Path) -> None:
    """Mutmut is not in pyproject.toml when use_mutmut is 'no'."""
    pyproject = (generated_project / "pyproject.toml").read_text()
    assert "mutmut" not in pyproject


def test_hypothesis_included_when_opted_in(generated_project_all_opts: Path) -> None:
    """Hypothesis is in pyproject.toml when use_hypothesis is 'yes'."""
    pyproject = (generated_project_all_opts / "pyproject.toml").read_text()
    assert "hypothesis" in pyproject


def test_mutmut_included_when_opted_in(generated_project_all_opts: Path) -> None:
    """Mutmut is in pyproject.toml when use_mutmut is 'yes'."""
    pyproject = (generated_project_all_opts / "pyproject.toml").read_text()
    assert "mutmut" in pyproject


def test_git_initialized(generated_project: Path) -> None:
    """Post-gen hook initializes a git repo."""
    assert (generated_project / ".git").is_dir()
