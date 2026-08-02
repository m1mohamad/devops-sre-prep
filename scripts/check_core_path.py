#!/usr/bin/env python3
"""Validate the canonical end-to-end Core Path and its repository integration."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = ROOT / "docs/study/core-path/index.md"
REQUIRED_HEADINGS = [
    "# Core Path — End-to-End Platform Scenario",
    "## Why This Page Exists",
    "## What You Will Understand",
    "## The FinAI Scenario",
    "## Two-to-Three-Hour Study Plan",
    "## The Complete Platform in One Diagram",
    "## The Six Platform Layers",
    "## AWS and GCP Component Mapping",
    "## Flow 1 — Building the Cloud Foundation",
    "## Flow 2 — Delivering a Change to Production",
    "## Flow 3 — Serving a Payment Request",
    "## Flow 4 — Processing Asynchronous Events",
    "## Flow 5 — Identity, Secrets, and Certificates",
    "## Flow 6 — Observability and Incident Response",
    "## Control Plane Versus Data Plane",
    "## Component Ownership",
    "## Security Across the Whole System",
    "## What the AI Component Changes",
    "## What the AI Component Does Not Change",
    "## One End-to-End Production Incident",
    "## Investigation and Recovery Walkthrough",
    "## Core Commands and Evidence",
    "## Platform Trade-offs",
    "## 60-Second Interview Answer",
    "## Five-Minute Architecture Walkthrough",
    "## Ten Memory Anchors",
    "## Recall Exercise",
    "## Existing Deep Dives",
    "## Further Reading",
]
CONCEPTS = {
    "Terraform or OpenTofu": r"terraform|opentofu",
    "CI": r"\bci\b",
    "registry": r"registry",
    "GitOps": r"gitops",
    "Argo CD or Flux": r"argo|flux",
    "Kubernetes": r"kubernetes",
    "gateway or ingress": r"gateway|ingress",
    "microservices": r"microservices",
    "PostgreSQL": r"postgresql",
    "Redis": r"redis",
    "messaging": r"kafka|sqs|pub/sub|queue|messag",
    "model service": r"model.service",
    "secrets": r"secret",
    "observability": r"opentelemetry|prometheus|metrics.*logs.*traces|telemetry",
    "on-call": r"on-call|oncall",
}
INTEGRATIONS = {
    "mkdocs.yml": "study/core-path/index.md",
    "START-HERE.md": "docs/study/core-path/index.md",
    "README.md": "docs/study/core-path/index.md",
    "docs/study/index.md": "core-path/index.md",
    "docs/study/00-interview-dashboard.md": "core-path/index.md",
}


def outside_fences(text: str) -> str:
    """Return prose outside backtick or tilde fenced code blocks."""
    visible: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)[0]
            fence = None if fence == token else token if fence is None else fence
        elif fence is None:
            visible.append(line)
    return "\n".join(visible)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    if not CORE_PATH.is_file():
        print(f"Missing {CORE_PATH.relative_to(ROOT)}")
        return 1

    text = CORE_PATH.read_text(encoding="utf-8")
    prose = outside_fences(text)
    positions: list[int] = []
    for heading in REQUIRED_HEADINGS:
        matches = list(re.finditer(rf"(?m)^{re.escape(heading)}$", prose))
        if len(matches) != 1:
            fail(errors, f"required heading must occur once: {heading}")
        else:
            positions.append(matches[0].start())
    if len(positions) == len(REQUIRED_HEADINGS) and positions != sorted(positions):
        fail(errors, "required headings are not in the required order")

    words = re.findall(r"\b[\w'-]+\b", prose)
    if not 3000 <= len(words) <= 6500:
        fail(errors, f"word count {len(words)} is outside 3000–6500")

    diagrams = re.findall(r"```mermaid\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if not 1 <= len(diagrams) <= 4:
        fail(errors, f"Mermaid diagram count {len(diagrams)} is outside 1–4")
    elif diagrams:
        first = diagrams[0].lower()
        for concept, pattern in CONCEPTS.items():
            if not re.search(pattern, first, re.IGNORECASE):
                fail(errors, f"first Mermaid diagram is missing {concept}")

    mapping = re.search(
        r"## AWS and GCP Component Mapping\n(.*?)(?=\n## )", prose, re.DOTALL
    )
    if not mapping or not all(term in mapping.group(1) for term in ("| AWS", "| GCP", "EKS", "GKE")):
        fail(errors, "AWS and GCP component mapping table is missing")

    incident = re.search(
        r"## One End-to-End Production Incident\n(.*?)(?=\n## )", prose, re.DOTALL
    )
    if not incident or "fraud-v12" not in incident.group(1):
        fail(errors, "fraud-v12 production incident is missing")

    for number, line in enumerate(prose.splitlines(), 1):
        if re.match(r"^\s*(?:!!!|\?\?\?\+?|===)(?:\s|$)", line):
            fail(errors, f"line {number}: MkDocs-only block syntax")
    for match in re.finditer(r"!?\[[^]]*]\(\s*<?([^) >]+)", prose):
        target = match.group(1)
        if re.match(r"^(?:[A-Za-z][A-Za-z0-9+.-]*:|/|~|[A-Za-z]:[\\/])", target):
            fail(errors, f"repository link must be relative: {target}")

    for relative, expected in INTEGRATIONS.items():
        integration_text = (ROOT / relative).read_text(encoding="utf-8")
        if expected not in integration_text:
            fail(errors, f"Core Path is not linked from {relative}")

    if errors:
        print("Core Path validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(
        f"Core Path valid: {len(words)} words, {len(diagrams)} Mermaid diagram(s), "
        f"{len(REQUIRED_HEADINGS)} required headings."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
