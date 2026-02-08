#!/usr/bin/env bash

set -e

cd backend

# Try to use uv if available, otherwise fall back to python -m pytest
if command -v uv &> /dev/null; then
    uv run pytest
else
    # Fallback to python -m pytest if uv is not available
    python -m pytest
fi
