#!/usr/bin/env python3
"""Reject unresolved Git conflict markers in tracked text files."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CONFLICT_MARKER = re.compile(r"^(?:<{7}|={7}|>{7})(?:\s|$)")


def tracked_files() -> list[Path]:
    """Return tracked files so generated and ignored content is not inspected."""
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / name.decode() for name in result.stdout.split(b"\0") if name]


errors: list[str] = []
for path in tracked_files():
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        continue
    for line_number, line in enumerate(lines, 1):
        if CONFLICT_MARKER.match(line):
            errors.append(f"{path.relative_to(ROOT)}:{line_number}: conflict marker")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("No unresolved conflict markers found in tracked files.")
