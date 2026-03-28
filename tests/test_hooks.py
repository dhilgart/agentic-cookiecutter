"""Test pre-generation validation hooks."""

from pathlib import Path

import pytest
from cookiecutter.exceptions import FailedHookException
from cookiecutter.main import cookiecutter

from conftest import DEFAULT_CONTEXT, TEMPLATE_DIR


def test_rejects_invalid_project_slug(tmp_path: Path) -> None:
    """Project slug with uppercase or special chars is rejected."""
    context = {**DEFAULT_CONTEXT, "project_slug": "Bad_Project!"}
    with pytest.raises(FailedHookException):
        cookiecutter(
            TEMPLATE_DIR,
            no_input=True,
            extra_context=context,
            output_dir=str(tmp_path),
        )


def test_rejects_slug_starting_with_digit(tmp_path: Path) -> None:
    """Project slug starting with a digit is rejected."""
    context = {**DEFAULT_CONTEXT, "project_slug": "1bad"}
    with pytest.raises(FailedHookException):
        cookiecutter(
            TEMPLATE_DIR,
            no_input=True,
            extra_context=context,
            output_dir=str(tmp_path),
        )


def test_rejects_old_python_version(tmp_path: Path) -> None:
    """Python version below 3.12 is rejected."""
    context = {**DEFAULT_CONTEXT, "python_version": "3.11"}
    with pytest.raises(FailedHookException):
        cookiecutter(
            TEMPLATE_DIR,
            no_input=True,
            extra_context=context,
            output_dir=str(tmp_path),
        )


def test_accepts_python_313(tmp_path: Path) -> None:
    """Python 3.13 is accepted."""
    context = {**DEFAULT_CONTEXT, "python_version": "3.13"}
    cookiecutter(
        TEMPLATE_DIR,
        no_input=True,
        extra_context=context,
        output_dir=str(tmp_path),
    )
    assert (tmp_path / "test-project").is_dir()
