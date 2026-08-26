#!/usr/bin/env python3
"""Focused validation for the Platform / DevOps / SRE mental-model page."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs/study/04-platform-devops-sre-mental-models.md"

REQUIRED_HEADINGS = [
    "# Platform / DevOps / SRE Mental Models",
    "## The 20 Core Concepts",
    "# Troubleshooting Ladder",
    "# Networking Mental Model",
    "# Security Mental Model",
    "# Scheduling Mental Model",
    "# Health Mental Model",
    "# Scaling Mental Model",
    "# Reliability Mental Model",
    "# CI/CD Mental Model",
    "# Reconciliation Is Everywhere",
    "# State and Storage Mental Model",
    "# Observability Mental Model",
    "# Failure Domains and Blast Radius",
    "# Follow Boundaries, Not Products",
    "# Ultimate Memory Card",
]

NAVIGATION_LINKS = [
    ("START-HERE.md", "docs/study/04-platform-devops-sre-mental-models.md"),
    ("docs/study/00-interview-dashboard.md", "04-platform-devops-sre-mental-models.md"),
    ("docs/study/index.md", "04-platform-devops-sre-mental-models.md"),
    ("mkdocs.yml", "study/04-platform-devops-sre-mental-models.md"),
]


def main() -> int:
    errors: list[str] = []
    if not PAGE.is_file():
        print(f"Platform mental-model validation failed: missing {PAGE.relative_to(ROOT)}")
        return 1

    text = PAGE.read_text(encoding="utf-8")
    for heading in REQUIRED_HEADINGS:
        if not re.search(rf"(?m)^{re.escape(heading)}$", text):
            errors.append(f"required heading missing: {heading}")

    if re.search(r"\bHPA\s+(?:adds?|creates?|launches?)\s+Pods?\b", text, re.I):
        errors.append("HPA must not be described as directly creating Pods")

    scaling_match = re.search(
        r"(?ms)^# Scaling Mental Model\s*$\n(.*?)(?=^# )", text
    )
    if not scaling_match:
        errors.append("scaling section could not be located")
    else:
        scaling = scaling_match.group(1)
        scaling_concepts = [
            (r"\bHPA\b", "HPA"),
            (r"desired replicas?", "desired replica count"),
            (r"\b(?:Deployment|ReplicaSet|workload controller)\b", "workload controller"),
            (r"\bPending\b", "Pending Pods"),
            (r"\b(?:Karpenter|Cluster Autoscaler)\b", "node autoscaler"),
        ]
        for pattern, concept in scaling_concepts:
            if not re.search(pattern, scaling, re.I):
                errors.append(f"scaling section missing concept: {concept}")

    for anchor in ("scheduler", "kubelet", "readiness", "EndpointSlice"):
        if not re.search(rf"\b{re.escape(anchor)}\b", text, re.I):
            errors.append(f"Kubernetes ownership anchor missing: {anchor}")

    if re.search(r"(?m)^(?:<<<<<<<|=======|>>>>>>>)", text):
        errors.append("conflict marker found")
    prohibited = r"(?mi)^\s*(?:!!!|\?\?\?\+?|===)(?:\s|$)|^\s*<(?:div|details|summary)(?:\s|>)"
    if re.search(prohibited, text):
        errors.append("renderer-specific Markdown block found")
    for target in re.findall(r"!?\[[^]]*\]\(([^) ]+)", text):
        target = target.strip("<>")
        if re.match(r"^(?:/|~|[A-Za-z]:[\\/])", target):
            errors.append(f"non-relative internal link: {target}")

    for relative, target in NAVIGATION_LINKS:
        path = ROOT / relative
        if not path.is_file() or target not in path.read_text(encoding="utf-8"):
            errors.append(f"navigation integration missing from {relative}: {target}")

    if errors:
        print("Platform mental-model validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print("Platform mental-model page valid: headings, ownership, navigation, and compatibility.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
