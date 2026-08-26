#!/usr/bin/env python3
"""Focused structural and correctness checks for the Golden Path case study."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs/study/05-golden-path-from-idea-to-production.md"

REQUIRED_CONCEPTS = [
    (r"\bGolden Path\b", "Golden Path"),
    (r"\bplatform primitives?\b", "platform primitives"),
    (r"\bTerraform\b", "Terraform"),
    (r"\bHelm\b", "Helm"),
    (r"\bCI\b", "CI"),
    (r"\bGitOps\b", "GitOps"),
    (r"\bArgoCD\b", "ArgoCD"),
    (r"\bBackstage\b", "Backstage"),
    (r"\bSoftware Template\b", "Software Template"),
    (r"\bSoftware Catalog\b", "Software Catalog"),
    (r"\bobservability\b", "observability"),
    (r"\bescape hatch(?:es)?\b", "escape hatch"),
    (r"\bDay 2\b", "Day 2"),
    (r"\bGolden State\b", "Golden State"),
    (r"\bPlatform Lead\b", "Platform Lead"),
]

REQUIRED_HEADINGS = [
    "# Golden Path: From Idea to Production",
    "## What happens after CREATE?",
    "## What gets generated?",
    "## CI is part of the Golden Path",
    "## GitOps and the ArgoCD handoff",
    "## Observability is part of production readiness",
    "## Escape hatches: a path, not a prison",
    "## Complete Golden Path: redraw this on a whiteboard",
    "## Ownership split",
    "## Interview questions",
    "## Final memory anchors",
]

NAVIGATION_LINKS = [
    ("START-HERE.md", "docs/study/05-golden-path-from-idea-to-production.md"),
    ("docs/study/index.md", "05-golden-path-from-idea-to-production.md"),
    ("docs/study/00-interview-dashboard.md", "05-golden-path-from-idea-to-production.md"),
    ("mkdocs.yml", "study/05-golden-path-from-idea-to-production.md"),
]

PROHIBITED_CLAIMS = [
    (r"\bBackstage is the platform\b", "Backstage must not equal the platform"),
    (r"\b(?:a |the )?Terraform module is (?:a |the )?Golden Path\b", "Terraform module must remain a primitive"),
    (r"\b(?:a |the )?Helm chart is (?:a |the )?Golden Path\b", "Helm chart must remain a primitive"),
    (r"\bArgoCD builds?(?: and publishes?)? (?:the )?(?:container )?images?\b", "ArgoCD must not build images"),
    (r"\bGolden Path has no exceptions?\b", "Golden Path must allow justified exceptions"),
]


def main() -> int:
    errors: list[str] = []
    if not PAGE.is_file():
        print(f"Golden Path validation failed: missing {PAGE.relative_to(ROOT)}")
        return 1

    text = PAGE.read_text(encoding="utf-8")
    for pattern, label in REQUIRED_CONCEPTS:
        if not re.search(pattern, text, re.I):
            errors.append(f"required concept missing: {label}")
    for heading in REQUIRED_HEADINGS:
        if not re.search(rf"(?m)^{re.escape(heading)}$", text):
            errors.append(f"required heading missing: {heading}")
    for pattern, message in PROHIBITED_CLAIMS:
        if re.search(pattern, text, re.I):
            errors.append(f"prohibited claim: {message}")

    examples = [
        (r'```hcl\s+module\s+"database"', "Terraform module example"),
        (r"```yaml\s+service:\s+name: orders-api", "Helm values example"),
        (r"uses: company/platform-actions/.github/workflows/container\.yml@v4", "reusable CI example"),
        (r"orders-api/\s*\n├── src/", "service repository tree"),
        (r"(?m)^## Ownership split$", "ownership split"),
        (r"(?m)^## Complete Golden Path:", "end-to-end diagram"),
        (r"(?m)^## Interview questions$", "interview questions"),
    ]
    for pattern, label in examples:
        if not re.search(pattern, text, re.I):
            errors.append(f"required example missing: {label}")

    escape_section = re.search(
        r"(?ms)^## Escape hatches:.*?(?=^## )", text
    )
    if not escape_section or not re.search(r"exception|unusual", escape_section.group(), re.I):
        errors.append("escape-hatch section must describe exceptional workloads")

    if "ArgoCD does not build or publish the application image" not in text:
        errors.append("missing explicit ArgoCD/CI responsibility distinction")
    if not re.search(r"CI (?:builds|publishes).*artifact", text, re.I):
        errors.append("missing CI artifact ownership")

    for relative, target in NAVIGATION_LINKS:
        path = ROOT / relative
        if not path.is_file() or target not in path.read_text(encoding="utf-8"):
            errors.append(f"navigation integration missing from {relative}: {target}")

    if re.search(r"(?m)^(?:<<<<<<<|=======|>>>>>>>)", text):
        errors.append("conflict marker found")

    if errors:
        print("Golden Path validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print("Golden Path case study valid: concepts, distinctions, examples, and navigation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
