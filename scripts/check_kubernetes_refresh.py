#!/usr/bin/env python3
"""Validate the Kubernetes memory refresh, study week, and navigation."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REFRESH = ROOT / "docs/study/kubernetes/00-kubernetes-interview-refresh.md"
WEEK = ROOT / "docs/study/03-senior-platform-interview-week.md"

HEADINGS = [
    "# Kubernetes Interview Memory Refresh", "## How to Use This Page",
    "## The Kubernetes Mental Model", "## Core Components",
    "## Kubernetes Workload Objects", "## What Happens When a Deployment Is Created?",
    "## Pod Lifecycle and Container States", "## Startup, Readiness, and Liveness",
    "## Requests, Limits, QoS, and Node Pressure", "## Scheduling and Placement",
    "## Services, EndpointSlices, and Cluster Networking",
    "## DNS, Ingress, Gateway, and External Traffic",
    "## Storage, PVCs, PVs, StorageClasses, and CSI",
    "## Horizontal Scaling and Node Scaling",
    "## Disruptions, PDBs, Draining, and Graceful Termination",
    "## Kubernetes Identity, RBAC, and Workload Security",
    "## NetworkPolicy and Runtime Security", "## Admission, Policy, and API Safety",
    "## Controllers, Reconciliation, CRDs, and Operators",
    "## GitOps and Kubernetes Delivery", "## Kubernetes Upgrades",
    "## EKS Mental Model", "## GPU and AI Workloads on Kubernetes",
    "## Production Troubleshooting Decision Tree", "## High-Value kubectl Commands",
    "## Interview Questions You Must Be Able to Answer", "## One-Page Recall Exercise",
    "## Related Deep Dives",
]


def prose(text: str) -> str:
    text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S)
    text = re.sub(r"(?ms)^```.*?^```\s*$", "", text)
    return text


def section(text: str, heading: str) -> str:
    match = re.search(rf"(?ms)^{re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", text)
    return match.group(1) if match else ""


def main() -> int:
    errors: list[str] = []
    for path in (REFRESH, WEEK):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        print("Kubernetes refresh validation failed:\n" + "\n".join(errors))
        return 1

    text = REFRESH.read_text(encoding="utf-8")
    visible = prose(text)
    positions: list[int] = []
    for heading in HEADINGS:
        matches = list(re.finditer(rf"(?m)^{re.escape(heading)}$", visible))
        if len(matches) != 1:
            errors.append(f"heading must appear exactly once: {heading}")
        else:
            positions.append(matches[0].start())
    if len(positions) == len(HEADINGS) and positions != sorted(positions):
        errors.append("required headings are out of order")

    words = re.findall(r"\b[\w'-]+\b", visible)
    if not 4000 <= len(words) <= 8000:
        errors.append(f"prose word count {len(words)} is outside 4000–8000")

    checks = {
        "## What Happens When a Deployment Is Created?": ["API server", "etcd", "Deployment", "ReplicaSet", "scheduler", "kubelet", "readiness", "EndpointSlice"],
        "## Startup, Readiness, and Liveness": ["startup", "readiness", "liveness"],
        "## Scheduling and Placement": ["nodeSelector", "affinity", "taint", "toleration", "topology spread"],
        "## Horizontal Scaling and Node Scaling": ["HPA", "Cluster Autoscaler", "Karpenter"],
        "## Disruptions, PDBs, Draining, and Graceful Termination": ["PDB", "SIGTERM", "terminationGracePeriodSeconds"],
        "## Kubernetes Identity, RBAC, and Workload Security": ["RBAC", "ServiceAccount", "workload identity"],
        "## NetworkPolicy and Runtime Security": ["NetworkPolicy", "securityContext"],
        "## Controllers, Reconciliation, CRDs, and Operators": ["informer", "work queue", "idempotent", "ownerReference", "finalizer", "CRD"],
        "## GPU and AI Workloads on Kubernetes": ["nvidia.com/gpu", "GPU memory", "queue", "model revision"],
    }
    for heading, terms in checks.items():
        body = section(text, heading)
        for term in terms:
            if term.lower() not in body.lower():
                errors.append(f"{heading} is missing {term}")

    yaml_count = len(re.findall(r"(?m)^```ya?ml\s*$", text))
    mermaid_count = len(re.findall(r"(?m)^```mermaid\s*$", text))
    interview = section(text, "## Interview Questions You Must Be Able to Answer")
    question_count = len(re.findall(r"(?m)^\d+\. \*\*.+\?\*\*", interview))
    if yaml_count < 8: errors.append(f"only {yaml_count} YAML examples; need 8")
    if mermaid_count < 4: errors.append(f"only {mermaid_count} Mermaid diagrams; need 4")
    if question_count < 20: errors.append(f"only {question_count} interview questions; need 20")

    for match in re.finditer(r"!?\[[^]]*\]\(([^) ]+)", text):
        target = match.group(1).strip("<>")
        if re.match(r"^(?:[a-z]+:|/|~|[A-Za-z]:[\\/])", target):
            errors.append(f"non-relative internal link: {target}")

    integrations = [
        ("docs/study/kubernetes/index.md", "00-kubernetes-interview-refresh.md"),
        ("docs/study/00-interview-dashboard.md", "kubernetes/00-kubernetes-interview-refresh.md"),
        ("START-HERE.md", "docs/study/kubernetes/00-kubernetes-interview-refresh.md"),
        ("mkdocs.yml", "study/kubernetes/00-kubernetes-interview-refresh.md"),
        ("docs/study/index.md", "03-senior-platform-interview-week.md"),
        ("docs/study/00-interview-dashboard.md", "03-senior-platform-interview-week.md"),
        ("mkdocs.yml", "study/03-senior-platform-interview-week.md"),
    ]
    for relative, target in integrations:
        content = (ROOT / relative).read_text(encoding="utf-8") if (ROOT / relative).is_file() else ""
        if target not in content:
            errors.append(f"{target} is not linked from {relative}")
    scheduling = section(text, "## Scheduling and Placement")
    admission = section(text, "## Admission, Policy, and API Safety")
    if "resourcequota" in scheduling.lower():
        errors.append("ResourceQuota must not be listed as a FailedScheduling cause")
    admission_normalized = re.sub(r"\s+", " ", admission.lower())
    quota_rejection = re.search(
        r"resourcequota.{0,160}(?:reject|deny|denied).{0,120}(?:request|creation|write)"
        r"|resourcequota.{0,160}(?:request|creation|write).{0,120}(?:reject|deny|denied)",
        admission_normalized,
    )
    if not quota_rejection:
        errors.append(
            "admission section must explicitly tie ResourceQuota to rejecting or denying object creation"
        )

    all_new = text + "\n" + WEEK.read_text(encoding="utf-8")
    prohibited = r"(?m)^\s*(?:!!!|\?\?\?\+?|===)(?:\s|$)|^\s*<(?:div|details|summary)(?:\s|>)"
    if re.search(prohibited, all_new, flags=re.I): errors.append("prohibited Markdown block found")
    if re.search(r"(?m)^(?:<<<<<<<|=======|>>>>>>>)", all_new): errors.append("conflict marker found")

    paragraphs = [re.sub(r"\s+", " ", p.strip()) for p in re.split(r"\n\s*\n", visible) if len(p.split()) >= 20]
    if len(paragraphs) != len(set(paragraphs)): errors.append("obviously repeated generic paragraph found")
    if "## Production Troubleshooting Decision Tree" not in text: errors.append("troubleshooting decision tree missing")

    if errors:
        print("Kubernetes refresh validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Kubernetes refresh valid: {len(words)} words, {yaml_count} YAML examples, {mermaid_count} Mermaid diagrams, {question_count} interview questions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
