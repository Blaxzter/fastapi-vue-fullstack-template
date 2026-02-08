#!/usr/bin/env python3
"""Run pytest for pre-commit hook."""

import os
import subprocess
import sys
from pathlib import Path


def main():
    """Run tests using uv or python -m pytest."""
    backend_dir = Path(__file__).parent.parent.parent / "backend"
    os.chdir(backend_dir)

    # Try to use uv if available
    try:
        result = subprocess.run(
            ["uv", "run", "pytest"],
            check=False,
        )
        sys.exit(result.returncode)
    except FileNotFoundError:
        # Fall back to python -m pytest
        result = subprocess.run(
            [sys.executable, "-m", "pytest"],
            check=False,
        )
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
