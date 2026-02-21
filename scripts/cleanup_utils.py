#!/usr/bin/env python3
"""Shared utilities for template cleanup scripts.

Provides idempotent file operations: delete, modify text/JSON, remove code blocks.
All operations skip silently if targets are already removed.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Return the repository root directory (parent of scripts/)."""
    return Path(__file__).resolve().parent.parent


def delete_files(root: Path, relative_paths: list[str]) -> list[str]:
    """Delete files by relative path. Returns list of actually deleted paths."""
    deleted = []
    for rel in relative_paths:
        p = root / rel
        if p.exists():
            p.unlink()
            deleted.append(rel)
            print(f"  Deleted: {rel}")
        else:
            print(f"  Already gone: {rel}")
    return deleted


def delete_directories(root: Path, relative_paths: list[str]) -> list[str]:
    """Delete directories recursively. Returns list of actually deleted paths."""
    deleted = []
    for rel in relative_paths:
        p = root / rel
        if p.exists():
            shutil.rmtree(p)
            deleted.append(rel)
            print(f"  Deleted dir: {rel}")
        else:
            print(f"  Already gone: {rel}")
    return deleted


def _display_path(file_path: Path) -> str:
    """Return a display-friendly relative path, or the full path if not under root."""
    try:
        return str(file_path.relative_to(get_project_root()))
    except ValueError:
        return str(file_path)


def _read_file(file_path: Path) -> str | None:
    """Read a file, returning None if it doesn't exist."""
    if not file_path.exists():
        print(f"  Skipped (missing): {file_path}")
        return None
    return file_path.read_text(encoding="utf-8")


def _write_file(file_path: Path, content: str) -> None:
    """Write content to a file with UTF-8 encoding."""
    file_path.write_text(content, encoding="utf-8", newline="\n")


def remove_lines_matching(file_path: Path, patterns: list[str]) -> bool:
    """Remove lines matching any regex pattern. Collapses resulting double blank lines.

    Returns True if the file was modified.
    """
    content = _read_file(file_path)
    if content is None:
        return False

    lines = content.splitlines(keepends=True)
    compiled = [re.compile(p) for p in patterns]
    new_lines = [line for line in lines if not any(p.search(line) for p in compiled)]

    # Collapse runs of 3+ newlines into 2
    result = "".join(new_lines)
    result = re.sub(r"\n{3,}", "\n\n", result)

    if result != content:
        _write_file(file_path, result)
        print(f"  Modified: {_display_path(file_path)}")
        return True
    return False


def remove_block(
    file_path: Path,
    anchor_pattern: str,
    *,
    open_char: str = "{",
    close_char: str = "}",
) -> bool:
    """Remove a code block containing the anchor pattern.

    Finds the line matching anchor_pattern, walks backward to the opening brace/bracket
    at the same or lesser indentation, walks forward counting depth to the closing
    brace/bracket, and removes the entire block including a trailing comma if present.

    Returns True if the file was modified.
    """
    content = _read_file(file_path)
    if content is None:
        return False

    lines = content.splitlines(keepends=True)
    anchor_re = re.compile(anchor_pattern)

    # Find the anchor line
    anchor_idx = None
    for i, line in enumerate(lines):
        if anchor_re.search(line):
            anchor_idx = i
            break

    if anchor_idx is None:
        print(f"  No match for '{anchor_pattern}' in {file_path.name}")
        return False

    # Walk backward to find the opening brace/bracket
    # If the anchor line itself contains the opener, start there
    start_idx = anchor_idx
    if open_char not in lines[anchor_idx]:
        for i in range(anchor_idx - 1, -1, -1):
            stripped = lines[i].strip()
            if open_char in stripped:
                start_idx = i
                break

    # Walk forward from start counting depth
    depth = 0
    end_idx = start_idx
    for i in range(start_idx, len(lines)):
        depth += lines[i].count(open_char)
        depth -= lines[i].count(close_char)
        if depth <= 0:
            end_idx = i
            break

    # Check if the closing line has a trailing comma (e.g., "},")
    # or the next line is just a comma
    if end_idx + 1 < len(lines) and lines[end_idx + 1].strip() == ",":
        end_idx += 1

    # Remove the block
    new_lines = lines[:start_idx] + lines[end_idx + 1 :]

    result = "".join(new_lines)
    # Collapse runs of 3+ newlines into 2
    result = re.sub(r"\n{3,}", "\n\n", result)

    if result != content:
        _write_file(file_path, result)
        print(f"  Modified (block removed): {_display_path(file_path)}")
        return True
    return False


def remove_json_keys(file_path: Path, dot_paths: list[str]) -> bool:
    """Remove keys from a JSON file by dot-separated paths.

    E.g., 'breadcrumbs.examples' removes data["breadcrumbs"]["examples"].
    Returns True if the file was modified.
    """
    content = _read_file(file_path)
    if content is None:
        return False

    data = json.loads(content)
    modified = False

    for dot_path in dot_paths:
        keys = dot_path.split(".")
        obj = data
        try:
            for key in keys[:-1]:
                obj = obj[key]
            if keys[-1] in obj:
                del obj[keys[-1]]
                modified = True
        except (KeyError, TypeError):
            pass  # Key already missing

    if modified:
        result = json.dumps(data, indent=4, ensure_ascii=False) + "\n"
        _write_file(file_path, result)
        print(f"  Modified (JSON keys): {_display_path(file_path)}")
    return modified


def replace_in_file(file_path: Path, old: str, new: str) -> bool:
    """Replace exact string in a file. Returns True if replaced."""
    content = _read_file(file_path)
    if content is None:
        return False

    if old not in content:
        return False

    result = content.replace(old, new)
    _write_file(file_path, result)
    print(f"  Modified (replace): {_display_path(file_path)}")
    return True


def confirm_action(description: str, items: list[str]) -> bool:
    """Ask user for confirmation. Returns True if confirmed. Respects --yes flag."""
    print(f"\n{description}\n")
    for item in items:
        print(f"  - {item}")

    if "--yes" in sys.argv:
        print("\n(Auto-confirmed via --yes flag)")
        return True

    print()
    response = input("Continue? [y/N] ")
    return response.strip().lower() == "y"


def print_next_steps(steps: list[str]) -> None:
    """Print post-cleanup instructions."""
    print("\n" + "=" * 60)
    print("Next steps:")
    print("=" * 60)
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")
    print()


# Cleanup script files that should be removed after use
CLEANUP_SCRIPTS = [
    "scripts/remove_examples.py",
    "scripts/remove_project_task_domain.py",
    "scripts/cleanup_utils.py",
]

# Justfile recipe blocks to remove (matched by recipe name)
CLEANUP_JUSTFILE_RECIPES = [
    "remove-examples",
    "remove-domain",
    "clean-template",
]


def self_clean(root: Path) -> None:
    """Remove this script, sibling cleanup scripts (if already gone), and justfile recipes.

    Only removes cleanup_utils.py when both cleanup scripts are gone.
    """
    this_file = Path(__file__).resolve()

    # Delete the calling script (not cleanup_utils.py, which is this file)
    caller = Path(sys.argv[0]).resolve()
    if caller.exists() and caller != this_file:
        caller.unlink()
        print(f"  Self-deleted: {_display_path(caller)}")

    # Only delete cleanup_utils.py if no other cleanup scripts remain
    other_cleanup_scripts = [
        root / "scripts/remove_examples.py",
        root / "scripts/remove_project_task_domain.py",
    ]
    if not any(p.exists() for p in other_cleanup_scripts):
        if this_file.exists():
            this_file.unlink()
            print(f"  Self-deleted: {_display_path(this_file)}")

    # Remove cleanup recipes from justfile
    _remove_justfile_recipes(root)


def _remove_justfile_recipes(root: Path) -> None:
    """Remove the template cleanup section from the justfile."""
    justfile = root / "justfile"
    if not justfile.exists():
        return

    content = justfile.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)

    # Find and remove the "Template Cleanup" section
    # It starts with "# ── Template Cleanup" and ends before the next "# ──" section
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if "Template Cleanup" in line and line.strip().startswith("#"):
            # Include the blank line before the section header if present
            start_idx = i - 1 if i > 0 and lines[i - 1].strip() == "" else i
        elif start_idx is not None and i > start_idx + 1:
            # Look for the next section header or end of file
            if line.strip().startswith("# ──"):
                end_idx = i
                break

    if start_idx is not None:
        if end_idx is None:
            end_idx = len(lines)
        new_lines = lines[:start_idx] + lines[end_idx:]
        result = "".join(new_lines)
        result = re.sub(r"\n{3,}", "\n\n", result)
        _write_file(justfile, result)
        print("  Modified: justfile (removed cleanup recipes)")
