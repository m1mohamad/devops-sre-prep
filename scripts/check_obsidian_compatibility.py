#!/usr/bin/env python3
"""Reject MkDocs-only constructs that do not render as Markdown in Obsidian."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"

# These block syntaxes require pymdownx extensions. In Obsidian they are shown
# as punctuation and indented text instead of the intended content blocks.
INCOMPATIBLE_BLOCKS = (
    (re.compile(r"^\s*!!!(?:\s|$)"), "MkDocs admonition (!!!)"),
    (re.compile(r"^\s*\?\?\?(?:\+)?(?:\s|$)"), "MkDocs collapsible admonition (???)"),
    (re.compile(r'^\s*===\s+["\']'), "MkDocs content tab (===)"),
)


def incompatible_lines(path: Path) -> list[tuple[int, str]]:
    """Return incompatible syntax outside fenced code blocks in *path*."""
    issues: list[tuple[int, str]] = []
    fence: str | None = None

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_match:
            marker = fence_match.group(1)
            if fence is None:
                fence = marker[0]
            elif marker[0] == fence:
                fence = None
            continue
        if fence is not None:
            continue

        for pattern, description in INCOMPATIBLE_BLOCKS:
            if pattern.match(line):
                issues.append((line_number, description))
                break

    return issues


def main() -> int:
    failures: list[str] = []
    markdown_files = sorted(DOCS_ROOT.rglob("*.md"))

    for path in markdown_files:
        for line_number, description in incompatible_lines(path):
            relative_path = path.relative_to(ROOT)
            failures.append(f"{relative_path}:{line_number}: {description}")

    if failures:
        print("Obsidian-incompatible Markdown found:")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1

    print(f"Obsidian compatibility check passed ({len(markdown_files)} files scanned).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
