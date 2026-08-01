---
title: Build Artifacts and Registries
tags: [cicd, platform-engineering]
aliases: [Build Artifacts and Registries study note]
---

# Build Artifacts and Registries

## 30-Second Answer

Build Artifacts and Registries is the path from **source tree** to **promotion**. The essential handoffs are reproducible build, container digest, SBOM, signature and provenance, registry retention. In production, I verify each handoff independently, keep its identity and state boundary visible, and operate it against availability, latency, security, and recovery objectives.

## Mental Model

```mermaid
flowchart LR
  N0[source tree] --> N1[reproducible build] --> N2[container digest] --> N3[SBOM] --> N4[signature and provenance] --> N5[registry retention] --> N6[promotion]
```

Read this diagram as a concrete sequence, not a generic maturity loop: a failure after **registry retention** has different evidence and ownership from a failure at **reproducible build**.

## Why It Exists

Without build artifacts and registries, teams must manually coordinate source tree, sbom, and promotion. The technology standardizes those interfaces so changes are repeatable, reviewable, and diagnosable. It is justified when the repeated operational risk exceeds the cost of owning the abstraction.

## How It Works

**source tree** owns stage 1; **reproducible build** owns stage 2; **container digest** owns stage 3; **SBOM** owns stage 4; **signature and provenance** owns stage 5; **registry retention** owns stage 6; **promotion** owns stage 7. Follow resource IDs, revisions, events, and timestamps across these stages; an acknowledgement at one stage never proves completion at the next.

## Mechanisms

* **source tree:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **reproducible build:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **container digest:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **SBOM:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **signature and provenance:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **registry retention:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **promotion:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.

## Production Architecture

Deploy source tree with least privilege and an auditable change path. Isolate sbom by environment and failure domain, make promotion observable, and test loss of each dependency. Version the interface between stages so producers and consumers can roll independently.

## Failure Modes

| Failure | Evidence | Response |
|---|---|---|
| a non-reproducible build changes bytes between environments | Compare stage latency and revision at reproducible build | Stop promotion and restore the last verified input |
| overprivileged pipeline credentials bypass review | Inspect saturation, quotas, events, and pending work at SBOM | Add valid capacity or shed load; do not retry without a bound |
| a green pipeline ignores rollout health | Compare the user result with promotion and upstream state | Mitigate first, preserve evidence, then repair the faulty contract |

## Trade-offs

More automation across source tree and promotion improves consistency but can propagate an error faster. Strong isolation narrows blast radius but increases cost and upgrades. Managed implementations reduce component toil; self-managed implementations offer control but require availability, backup, security patching, and on-call expertise.

## Lead-Level Follow-ups

* Which team owns **SBOM**, and what user-facing SLO proves it works?
* What remains available when **reproducible build** is down?
* Where is state durable, and how are restore and upgrade tested?

## My Experience Prompt

Describe a change to sbom: state the constraint, the exact signal that selected the design, the rollback boundary, and the durable guardrail you added.

## Recall Check

1. What does **source tree** send to **reproducible build**?
2. Which component stores or reports authoritative state?
3. How does **registry retention** affect **promotion**?
4. Which capacity limit fails first at production scale?
5. When is a simpler managed alternative preferable?

## Related Notes

* [Category index](index.md)
* [Interview dashboard](../00-interview-dashboard.md)
