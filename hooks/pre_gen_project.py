"""Pre-generation hook: validate cookiecutter inputs before generating."""

import re
import sys

PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
PACKAGE_NAME = "{{ cookiecutter.package_name }}"
PYTHON_VERSION = "{{ cookiecutter.python_version }}"

# project_slug must be a valid directory name: lowercase, hyphens, digits
if not re.match(r"^[a-z][a-z0-9-]*$", PROJECT_SLUG):
    print(
        f"ERROR: '{PROJECT_SLUG}' is not a valid project slug. "
        "Use only lowercase letters, digits, and hyphens. Must start with a letter."
    )
    sys.exit(1)

# package_name must be a valid Python identifier
if not PACKAGE_NAME.isidentifier():
    print(
        f"ERROR: '{PACKAGE_NAME}' is not a valid Python package name. "
        "Must be a valid Python identifier (letters, digits, underscores)."
    )
    sys.exit(1)

# python_version must be 3.12+
version_match = re.match(r"^3\.(\d+)$", PYTHON_VERSION)
if not version_match or int(version_match.group(1)) < 12:
    print(
        f"ERROR: Python version '{PYTHON_VERSION}' is not supported. "
        "Minimum is 3.12."
    )
    sys.exit(1)
