"""Post-generation hook: initialize the generated project."""

import subprocess
import sys

USE_HYPOTHESIS = "{{ cookiecutter.use_hypothesis }}"
USE_MUTMUT = "{{ cookiecutter.use_mutmut }}"


def run(cmd: list[str]) -> bool:
    """Run a command, return True on success."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"WARNING: '{' '.join(cmd)}' failed: {result.stderr.strip()}")
        return False
    return True


def init_git() -> None:
    """Initialize a git repo with an initial commit."""
    run(["git", "init"])
    run(["git", "checkout", "-b", "main"])
    run(["git", "add", "."])
    run(["git", "commit", "-m", "Initial commit from agentic-cookiecutter"])


def print_next_steps() -> None:
    """Print post-generation instructions."""
    print()
    print("=" * 60)
    print("  Project generated successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  cd {{ cookiecutter.project_slug }}")
    print("  uv sync")
    print("  uv run pytest")
    print()
    opt_in = []
    if USE_HYPOTHESIS == "yes":
        opt_in.append("hypothesis (property-based testing)")
    if USE_MUTMUT == "yes":
        opt_in.append("mutmut (mutation testing)")
    if opt_in:
        print(f"Opt-in features enabled: {', '.join(opt_in)}")
        print()


if __name__ == "__main__":
    init_git()
    print_next_steps()
