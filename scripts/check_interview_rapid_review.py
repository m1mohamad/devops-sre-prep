#!/usr/bin/env python3
"""Validate the final interview rapid review and Core Path recall answer key."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
RAPID = ROOT / "docs/study/interview/10-platform-interview-rapid-review.md"
ANSWERS = ROOT / "docs/study/core-path/recall-answers.md"
CORE = ROOT / "docs/study/core-path/index.md"

RAPID_HEADINGS = [
    "# Platform Interview Rapid Review",
    "## How to Use This Page",
    "## Final 90-Minute Review Plan",
    "## The Answer Structure",
    "## 30-Second Introduction",
    "## 90-Second Introduction",
    "## Five Reusable Experience Stories",
    "## Platform Engineering Questions",
    "## Reliability and Operations Questions",
    "## Data, Security, and Cost Questions",
    "## Rapid Technical Troubleshooting",
    "## Leadership and Ambiguity Questions",
    "## Questions to Ask the Interviewer",
    "## Final Interview Checklist",
    "## Related Deep Dives",
]

QUESTIONS = [
    "What is platform engineering?",
    "What is a golden path?",
    "How do you decide what belongs on a golden path?",
    "How do you measure platform success?",
    "How do you prioritize platform roadmap work?",
    "How do you define an SLO?",
    "How do you lead a production incident?",
    "Argo CD says Healthy, but users report errors. What now?",
    "How do you design rollback?",
    "How do you operate PostgreSQL reliably?",
    "How do you operate Redis reliably?",
    "How do you approach platform cost?",
    "How do you implement compliance without blocking delivery?",
    "How do you balance security with developer experience?",
    "A Pod is Pending",
    "Users see 502 responses although readiness is green",
    "Terraform plans to replace a critical resource",
    "Design a secure CI/CD flow",
    "How do you upgrade Kubernetes safely?",
    "CPU is normal, but latency is rising",
    "Tell me about a decision you made with incomplete information",
    "How do you handle disagreement with application teams?",
    "How do you mentor engineers?",
    "How do you reduce operational toil?",
    "What would you do in your first 90 days?",
]

QUESTION_FIELDS = [
    "**30-second ideal answer**",
    "**Strong answer includes**",
    "**Trade-off or assumption**",
    "**Experience prompt**",
    "**Common weak answer**",
]
ANSWER_FIELDS = ["**Ideal answer**", "**Key distinctions**", "**Common weak answer**"]
INTEGRATIONS = {
    "docs/study/interview/index.md": "10-platform-interview-rapid-review.md",
    "docs/study/index.md": "interview/10-platform-interview-rapid-review.md",
    "docs/study/00-interview-dashboard.md": "interview/10-platform-interview-rapid-review.md",
    "START-HERE.md": "docs/study/interview/10-platform-interview-rapid-review.md",
    "mkdocs.yml": "study/interview/10-platform-interview-rapid-review.md",
}


def visible_prose(text: str) -> str:
    """Remove YAML front matter and fenced code while preserving Markdown prose."""
    text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.DOTALL)
    visible: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            character = marker.group(1)[0]
            fence = None if fence == character else character if fence is None else fence
        elif fence is None:
            visible.append(line)
    return "\n".join(visible)


def section(text: str, heading: str) -> str | None:
    """Return a level-three section by its exact heading."""
    match = re.search(
        rf"(?ms)^### {re.escape(heading)}\s*$\n(.*?)(?=^### |^## |\Z)", text
    )
    return match.group(1) if match else None


def validate_links(errors: list[str], path: Path, text: str) -> None:
    """Reject absolute Markdown links in new content."""
    for match in re.finditer(r"!?\[[^]]*]\(\s*<?([^) >]+)", visible_prose(text)):
        target = match.group(1)
        if re.match(r"^(?:[A-Za-z][A-Za-z0-9+.-]*:|/|~|[A-Za-z]:[\\/])", target):
            errors.append(f"{path.relative_to(ROOT)} has non-relative link: {target}")


def main() -> int:
    errors: list[str] = []
    for path in (RAPID, ANSWERS):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        print("Interview rapid-review validation failed:\n" + "\n".join(f"- {e}" for e in errors))
        return 1

    rapid_text = RAPID.read_text(encoding="utf-8")
    answer_text = ANSWERS.read_text(encoding="utf-8")
    rapid_prose = visible_prose(rapid_text)
    answer_prose = visible_prose(answer_text)

    positions: list[int] = []
    for heading in RAPID_HEADINGS:
        matches = list(re.finditer(rf"(?m)^{re.escape(heading)}$", rapid_prose))
        if len(matches) != 1:
            errors.append(f"rapid-review heading must occur once: {heading}")
        else:
            positions.append(matches[0].start())
    if len(positions) == len(RAPID_HEADINGS) and positions != sorted(positions):
        errors.append("rapid-review headings are not in required order")

    rapid_words = re.findall(r"\b[\w'-]+\b", rapid_prose)
    answer_words = re.findall(r"\b[\w'-]+\b", answer_prose)
    if not 2500 <= len(rapid_words) <= 5500:
        errors.append(f"rapid-review word count {len(rapid_words)} is outside 2500–5500")

    for number in range(1, 6):
        if not re.search(rf"(?m)^### Story {number} — .+$", rapid_prose):
            errors.append(f"missing Story {number} section")

    for question in QUESTIONS:
        body = section(rapid_prose, question)
        if body is None:
            errors.append(f"missing interview question: {question}")
            continue
        for field in QUESTION_FIELDS:
            if field not in body:
                errors.append(f"{question} is missing {field}")

    headings = list(re.finditer(r"(?m)^## ([0-9]+)\. .+$", answer_prose))
    if len(headings) != 10 or [int(match.group(1)) for match in headings] != list(range(1, 11)):
        errors.append("recall answer page must have exactly numbered answer headings 1–10")
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(answer_prose)
        body = answer_prose[match.end():end]
        for field in ANSWER_FIELDS:
            if field not in body:
                errors.append(f"recall answer {match.group(1)} is missing {field}")

    core_text = CORE.read_text(encoding="utf-8") if CORE.is_file() else ""
    recall = core_text.find("## Recall Exercise")
    link = core_text.find("recall-answers.md", recall + 1)
    if recall < 0 or link < 0:
        errors.append("Core Path does not link to recall-answers.md after Recall Exercise")

    for relative, target in INTEGRATIONS.items():
        path = ROOT / relative
        if not path.is_file() or target not in path.read_text(encoding="utf-8"):
            errors.append(f"rapid review is not linked from {relative}")

    for path, text in ((RAPID, rapid_text), (ANSWERS, answer_text)):
        validate_links(errors, path, text)
        for number, line in enumerate(text.splitlines(), 1):
            if re.match(r"^\s*(?:!!!|\?\?\?\+?|===)(?:\s|$)", line):
                errors.append(f"{path.relative_to(ROOT)}:{number}: MkDocs-only block syntax")
            if re.match(r"^\s*(?:<div|<details|<summary)(?:\s|>)", line, re.IGNORECASE):
                errors.append(f"{path.relative_to(ROOT)}:{number}: layout-only HTML")
            if re.match(r"^(?:<<<<<<<|=======|>>>>>>>)", line):
                errors.append(f"{path.relative_to(ROOT)}:{number}: conflict marker")

    if errors:
        print("Interview rapid-review validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(
        f"Interview rapid review valid: {len(rapid_words)} words, {len(QUESTIONS)} answers; "
        f"recall key {len(answer_words)} words, {len(headings)} answers."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
