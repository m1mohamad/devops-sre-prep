#!/usr/bin/env python3
"""Reject copied Mermaid diagrams and prose templates in architecture pages."""

from __future__ import annotations

from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted((ROOT / "docs/architecture").glob("*.md"))
BLOCK = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
errors: list[str] = []


def normalize_mermaid(value: str) -> str:
    """Remove formatting and local Mermaid IDs while retaining semantic labels."""
    value = re.sub(r"%%.*", "", value)
    value = re.sub(
        r"\b[A-Za-z_][\w-]*(?=\s*(?:\[|\(|\{|\>))", "NODE", value
    )
    value = re.sub(r"\b(participant|actor)\s+\w+\s+as\s+", r"\1 NODE as ", value)
    value = re.sub(r"\b(subgraph)\s+\w+", r"\1 NODE", value)
    return re.sub(r"\s+", " ", value).strip().lower()


def paragraphs(value: str) -> set[str]:
    value = re.sub(r"^---\n.*?\n---\n", "", value, flags=re.DOTALL)
    value = BLOCK.sub("", value)
    result = set()
    for paragraph in re.split(r"\n\s*\n", value):
        if paragraph.startswith(("#", "*", "|", "```")):
            continue
        normalized = re.sub(r"\W+", " ", paragraph.lower()).strip()
        if len(normalized.split()) >= 20:
            result.add(normalized)
    return result


documents = {page: page.read_text(encoding="utf-8") for page in PAGES}
diagrams = {page: [normalize_mermaid(x) for x in BLOCK.findall(text)] for page, text in documents.items()}

for page, blocks in diagrams.items():
    if page.name != "index.md" and not blocks:
        errors.append(f"{page.relative_to(ROOT)}: architecture page has no Mermaid diagram")

for index, left in enumerate(PAGES):
    for right in PAGES[index + 1 :]:
        for left_block in diagrams[left]:
            for right_block in diagrams[right]:
                similarity = SequenceMatcher(None, left_block, right_block).ratio()
                if similarity >= 0.88:
                    errors.append(
                        f"{left.relative_to(ROOT)} and {right.relative_to(ROOT)}: "
                        f"near-identical Mermaid blocks ({similarity:.0%})"
                    )
        left_paragraphs, right_paragraphs = paragraphs(documents[left]), paragraphs(documents[right])
        denominator = min(len(left_paragraphs), len(right_paragraphs))
        if denominator and len(left_paragraphs & right_paragraphs) / denominator > 0.50:
            errors.append(
                f"{left.relative_to(ROOT)} and {right.relative_to(ROOT)}: more than 50% "
                "of substantial paragraphs are identical"
            )

generic = {
    "authenticated contract": re.compile(r"authenticated contract", re.I),
    "runtime workers": re.compile(r"runtime workers", re.I),
    "external dependency": re.compile(r"external dependency", re.I),
}
for label, pattern in generic.items():
    hits = [page for page, text in documents.items() if pattern.search(text)]
    if len(hits) > 1:
        errors.append(f"generic label {label!r} repeated in: {', '.join(x.name for x in hits)}")

title_control_hits = []
templates = [
    re.compile(r"For .+?, start from the contract visible to its consumer", re.I),
    re.compile(r"Describe a production change involving .+?\.", re.I),
    re.compile(r"What is the consumer-facing contract for .+?\?", re.I),
]
for page, text in documents.items():
    title = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if title and re.search(rf"\b{re.escape(title.group(1))}\s+control\b", text, re.I):
        title_control_hits.append(page.name)
    for template in templates:
        if template.search(text):
            errors.append(f"{page.relative_to(ROOT)}: title-substitution template detected")
if len(title_control_hits) > 1:
    errors.append(f"generic '<Page Title> control' labels repeated in: {', '.join(title_control_hits)}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"Architecture similarity valid across {len(PAGES)} files.")
