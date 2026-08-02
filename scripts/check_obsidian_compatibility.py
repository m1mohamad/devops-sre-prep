#!/usr/bin/env python3
"""Reject non-portable Markdown constructs that do not work in Obsidian."""

from pathlib import Path
import re
import sys

DOCS = Path(__file__).resolve().parents[1] / "docs"
MKDOCS_ONLY = re.compile(r"^\s*(?:!!!|\?\?\?\+?|===\s+[\"'])")
LOCAL_PATH = re.compile(r"(?:file:///|/home/|~/|(?<![A-Za-z])[A-Za-z]:[\\/])", re.IGNORECASE)
LAYOUT_HTML = re.compile(
    r"</?(?:div|span|center|section|aside|columns|column|grid|br|details|summary)\b",
    re.IGNORECASE,
)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


def errors_for(path: Path) -> list[tuple[int, str]]:
    """Return line-numbered compatibility errors outside fenced code blocks."""
    errors: list[tuple[int, str]] = []
    fence_char: str | None = None
    fence_length = 0

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fence_match = FENCE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if fence_char is None:
                fence_char, fence_length = marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                fence_char, fence_length = None, 0
            continue
        if fence_char is not None:
            continue

        if MKDOCS_ONLY.search(line):
            errors.append((line_number, "MkDocs-only admonition or tab syntax"))
        if LOCAL_PATH.search(line):
            errors.append((line_number, "absolute local filesystem link"))
        if LAYOUT_HTML.search(line):
            errors.append((line_number, "HTML layout construct"))
    return errors


def main() -> int:
    markdown_files = sorted(DOCS.rglob("*.md"))
    failures = 0
    for path in markdown_files:
        for line_number, reason in errors_for(path):
            print(f"{path.relative_to(DOCS.parent)}:{line_number}: {reason}")
            failures += 1
    if failures:
        print(f"Obsidian compatibility check failed ({failures} errors).", file=sys.stderr)
        return 1
    print(f"Obsidian compatibility check passed ({len(markdown_files)} files scanned).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
