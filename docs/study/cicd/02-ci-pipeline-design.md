---
title: CI Pipeline Design
tags: [cicd, platform-engineering]
aliases: [CI Pipeline Design study note]
---

# CI Pipeline Design

## 30-Second Answer

CI Pipeline Design is the path from **source checkout** to **pipeline evidence**. The essential handoffs are unit tests, integration tests, security gates, build cache, artifact publication. In production, I verify each handoff independently, keep its identity and state boundary visible, and operate it against availability, latency, security, and recovery objectives.

## Mental Model

```mermaid
flowchart LR
  N0[source checkout] --> N1[unit tests] --> N2[integration tests] --> N3[security gates] --> N4[build cache] --> N5[artifact publication] --> N6[pipeline evidence]
```

Read this diagram as a concrete sequence, not a generic maturity loop: a failure after **artifact publication** has different evidence and ownership from a failure at **unit tests**.

## Why It Exists

Without ci pipeline design, teams must manually coordinate source checkout, security gates, and pipeline evidence. The technology standardizes those interfaces so changes are repeatable, reviewable, and diagnosable. It is justified when the repeated operational risk exceeds the cost of owning the abstraction.

## How It Works

**source checkout** owns stage 1; **unit tests** owns stage 2; **integration tests** owns stage 3; **security gates** owns stage 4; **build cache** owns stage 5; **artifact publication** owns stage 6; **pipeline evidence** owns stage 7. Follow resource IDs, revisions, events, and timestamps across these stages; an acknowledgement at one stage never proves completion at the next.

## Mechanisms

* **source checkout:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **unit tests:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **integration tests:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **security gates:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **build cache:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **artifact publication:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **pipeline evidence:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.

## Production Architecture

Deploy source checkout with least privilege and an auditable change path. Isolate security gates by environment and failure domain, make pipeline evidence observable, and test loss of each dependency. Version the interface between stages so producers and consumers can roll independently.

## Failure Modes

| Failure | Evidence | Response |
|---|---|---|
| a non-reproducible build changes bytes between environments | Compare stage latency and revision at unit tests | Stop promotion and restore the last verified input |
| overprivileged pipeline credentials bypass review | Inspect saturation, quotas, events, and pending work at security gates | Add valid capacity or shed load; do not retry without a bound |
| a green pipeline ignores rollout health | Compare the user result with pipeline evidence and upstream state | Mitigate first, preserve evidence, then repair the faulty contract |

## Trade-offs

More automation across source checkout and pipeline evidence improves consistency but can propagate an error faster. Strong isolation narrows blast radius but increases cost and upgrades. Managed implementations reduce component toil; self-managed implementations offer control but require availability, backup, security patching, and on-call expertise.

## Lead-Level Follow-ups

* Which team owns **security gates**, and what user-facing SLO proves it works?
* What remains available when **unit tests** is down?
* Where is state durable, and how are restore and upgrade tested?

## My Experience Prompt

Describe a change to security gates: state the constraint, the exact signal that selected the design, the rollback boundary, and the durable guardrail you added.

## Recall Check

1. What does **source checkout** send to **unit tests**?
2. Which component stores or reports authoritative state?
3. How does **artifact publication** affect **pipeline evidence**?
4. Which capacity limit fails first at production scale?
5. When is a simpler managed alternative preferable?

## Related Notes

* [Category index](index.md)
* [Interview dashboard](../00-interview-dashboard.md)
