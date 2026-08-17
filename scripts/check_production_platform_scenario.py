#!/usr/bin/env python3
"""Focused, prose-tolerant validation for the Atlas production scenario."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "docs/study/04-production-platform-scenario.md"
DAYS = [
    "# Day 1 — Kubernetes: Deploy Atlas",
    "# Day 2 — Networking, Traffic and AWS/EKS",
    "# Day 3 — Rollouts, CI/CD, Helm and GitOps",
    "# Day 4 — Scaling, Resilience and Storage",
    "# Day 5 — Terraform, AWS Infrastructure and Security",
    "# Day 6 — Observability, SRE and Production Incident",
    "# Day 7 — System Design, Failure Domains and Senior-Level Reasoning",
]
CONCEPTS = [
    "Namespace", "Deployment", "ReplicaSet", "ConfigMap", "ServiceAccount",
    "EndpointSlice", "startupProbe", "readinessProbe", "livenessProbe",
    "nodeSelector", "affinity", "taint", "toleration", "ResourceQuota",
    "NetworkPolicy", "Argo CD", "HorizontalPodAutoscaler", "PodDisruptionBudget",
    "StorageClass", "VolumeAttachment", "Terraform", "workload identity",
    "error budget", "RTO", "RPO", "nvidia.com/gpu",
]
INTEGRATIONS = {
    "docs/study/index.md": "04-production-platform-scenario.md",
    "docs/study/00-interview-dashboard.md": "04-production-platform-scenario.md",
    "START-HERE.md": "docs/study/04-production-platform-scenario.md",
    "mkdocs.yml": "study/04-production-platform-scenario.md",
    ".github/workflows/pages.yml": "check_production_platform_scenario.py",
}


def strip_code(text: str) -> str:
    """Remove front matter and fenced examples for prose-level checks."""
    text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S)
    return re.sub(r"(?ms)^```.*?^```\s*$", "", text)


def main() -> int:
    errors: list[str] = []
    if not SCENARIO.is_file():
        print(f"Production scenario validation failed: missing {SCENARIO.relative_to(ROOT)}")
        return 1

    text = SCENARIO.read_text(encoding="utf-8")
    prose = strip_code(text)
    for heading in ["# Production Platform Interview Scenario", *DAYS,
                    "# End-to-end manifest reconstruction exercise", "# Failure map",
                    "# Senior interview questions"]:
        if len(re.findall(rf"(?m)^{re.escape(heading)}$", prose)) != 1:
            errors.append(f"heading must occur exactly once: {heading}")

    for term in CONCEPTS:
        if term.lower() not in text.lower():
            errors.append(f"required concept missing: {term}")

    yaml_count = len(re.findall(r"(?m)^```ya?ml\s*$", text))
    if yaml_count < 8:
        errors.append(f"need at least 8 concrete YAML examples; found {yaml_count}")
    questions = re.findall(r"(?m)^\d+\. [^\n]*\?[^\n]*$", prose)
    if len(questions) < 25:
        errors.append(f"need at least 25 interview questions; found {len(questions)}")
    if len(re.findall(r"(?m)^```mermaid\s*$", text)) < 4:
        errors.append("need at least 4 meaningful Mermaid diagrams")

    if re.search(r"(?m)^(?:<<<<<<<|=======|>>>>>>>)", text):
        errors.append("conflict marker found")
    prohibited = r"(?mi)^\s*(?:!!!|\?\?\?\+?|===)(?:\s|$)|^\s*<(?:div|details|summary)(?:\s|>)"
    if re.search(prohibited, text):
        errors.append("renderer-specific block found")
    for target in re.findall(r"!?\[[^]]*\]\(([^) ]+)", text):
        target = target.strip("<>")
        if re.match(r"^(?:/|~|[A-Za-z]:[\\/])", target):
            errors.append(f"non-relative internal link: {target}")

    paragraphs = [re.sub(r"\s+", " ", p.strip()) for p in re.split(r"\n\s*\n", prose)
                  if len(p.split()) >= 35]
    repeated = [p for p, count in Counter(paragraphs).items() if count > 1]
    if repeated:
        errors.append("obvious duplicate long paragraph found")

    # Catch accidental fallback to common disconnected toy workloads.
    for name in ("example-app", "my-pod"):
        if re.search(rf"\b{re.escape(name)}\b", text, flags=re.I):
            errors.append(f"inconsistent toy workload name found: {name}")
    if text.lower().count("atlas-api") < 30 or "atlas-prod" not in text:
        errors.append("Atlas naming is not used consistently enough")

    for relative, needle in INTEGRATIONS.items():
        path = ROOT / relative
        if not path.is_file() or needle not in path.read_text(encoding="utf-8"):
            errors.append(f"navigation/build integration missing from {relative}: {needle}")

    if errors:
        print("Production scenario validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    words = len(re.findall(r"\b[\w'-]+\b", prose))
    print(f"Production scenario valid: {words} prose words, {yaml_count} YAML examples, "
          f"{len(questions)} interview questions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
