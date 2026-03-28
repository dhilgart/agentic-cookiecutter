"""Shared fixtures for cookiecutter template tests."""

from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter


TEMPLATE_DIR = str(Path(__file__).parent.parent)

DEFAULT_CONTEXT = {
    "project_name": "Test Project",
    "project_slug": "test-project",
    "package_name": "test_project",
    "description": "A test project.",
    "author_name": "Test Author",
    "author_email": "test@example.com",
    "python_version": "3.12",
    "use_hypothesis": "no",
    "use_mutmut": "no",
}


@pytest.fixture()
def generated_project(tmp_path: Path) -> Path:
    """Generate a project with default settings, return its path."""
    cookiecutter(
        TEMPLATE_DIR,
        no_input=True,
        extra_context=DEFAULT_CONTEXT,
        output_dir=str(tmp_path),
    )
    return tmp_path / "test-project"


@pytest.fixture()
def generated_project_all_opts(tmp_path: Path) -> Path:
    """Generate a project with all optional features enabled."""
    context = {**DEFAULT_CONTEXT, "use_hypothesis": "yes", "use_mutmut": "yes"}
    cookiecutter(
        TEMPLATE_DIR,
        no_input=True,
        extra_context=context,
        output_dir=str(tmp_path),
    )
    return tmp_path / "test-project"
