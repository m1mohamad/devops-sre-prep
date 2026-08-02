#!/usr/bin/env python3
"""Reject Markdown constructs in documentation that do not work well in Obsidian."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"
MKDOCS_BLOCK = re.compile(r"^\s*(?:!!!|\?\?\?\+?|===)(?:\s|$)")
MARKDOWN_LINK = re.compile(r"!?\[[^]]*]\(\s*<?([^)>\s]+)", re.IGNORECASE)
LOCAL_PATH = re.compile(
    r"^(?:file:(?://)?|/|~/|[A-Za-z]:[\\/])",
    re.IGNORECASE,
)
LAYOUT_HTML = re.compile(
    r"</?(?:div|span|center|details|summary|section|aside|columns?|grid|br)(?:\s|>|/)",
    re.IGNORECASE,
)


def visible_lines(text: str) -> list[tuple[int, str]]:
    """Return lines outside fenced code blocks, where prose rules apply."""
    result: list[tuple[int, str]] = []
    fence: str | None = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token[0]
            elif token[0] == fence:
                fence = None
            continue
        if fence is None:
            result.append((number, line))
    return result


errors: list[str] = []
for path in sorted(DOCS_ROOT.rglob("*.md")):
    relative = path.relative_to(ROOT)
    for line_number, line in visible_lines(path.read_text(encoding="utf-8")):
        if MKDOCS_BLOCK.match(line):
            errors.append(f"{relative}:{line_number}: MkDocs-only block syntax")
        for match in MARKDOWN_LINK.finditer(line):
            if LOCAL_PATH.match(match.group(1)):
                errors.append(
                    f"{relative}:{line_number}: absolute local filesystem link: "
                    f"{match.group(1)}"
                )
        if LAYOUT_HTML.search(line):
            errors.append(f"{relative}:{line_number}: layout-only embedded HTML")

if errors:
    print("\n".join(errors))
    sys.exit(1)

print("Obsidian compatibility valid for docs/.")
