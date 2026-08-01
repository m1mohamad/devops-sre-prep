---
title: GitOps Continuous Delivery
tags: [cicd, platform-engineering]
aliases: [GitOps Continuous Delivery study note]
---

# GitOps Continuous Delivery

## 30-Second Answer

GitOps Continuous Delivery is the path from **application repository** to **sync and health**. The essential handoffs are CI and registry, environment repository, Argo CD, live-state diff. In production, I verify each handoff independently, keep its identity and state boundary visible, and operate it against availability, latency, security, and recovery objectives.

## Mental Model

```mermaid
flowchart LR
  N0[application repository] --> N1[CI and registry] --> N2[environment repository] --> N3[Argo CD] --> N4[live-state diff] --> N5[sync and health]
```

Read this diagram as a concrete sequence, not a generic maturity loop: a failure after **live-state diff** has different evidence and ownership from a failure at **CI and registry**.

## Why It Exists

Without gitops continuous delivery, teams must manually coordinate application repository, argo cd, and sync and health. The technology standardizes those interfaces so changes are repeatable, reviewable, and diagnosable. It is justified when the repeated operational risk exceeds the cost of owning the abstraction.

## How It Works

**application repository** owns stage 1; **CI and registry** owns stage 2; **environment repository** owns stage 3; **Argo CD** owns stage 4; **live-state diff** owns stage 5; **sync and health** owns stage 6. Follow resource IDs, revisions, events, and timestamps across these stages; an acknowledgement at one stage never proves completion at the next.

## Mechanisms

* **application repository:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **CI and registry:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **environment repository:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **Argo CD:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **live-state diff:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **sync and health:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.

## Production Architecture

Deploy application repository with least privilege and an auditable change path. Isolate argo cd by environment and failure domain, make sync and health observable, and test loss of each dependency. Version the interface between stages so producers and consumers can roll independently.

## Failure Modes

| Failure | Evidence | Response |
|---|---|---|
| a non-reproducible build changes bytes between environments | Compare stage latency and revision at CI and registry | Stop promotion and restore the last verified input |
| overprivileged pipeline credentials bypass review | Inspect saturation, quotas, events, and pending work at Argo CD | Add valid capacity or shed load; do not retry without a bound |
| a green pipeline ignores rollout health | Compare the user result with sync and health and upstream state | Mitigate first, preserve evidence, then repair the faulty contract |

## Trade-offs

More automation across application repository and sync and health improves consistency but can propagate an error faster. Strong isolation narrows blast radius but increases cost and upgrades. Managed implementations reduce component toil; self-managed implementations offer control but require availability, backup, security patching, and on-call expertise.

## Lead-Level Follow-ups

* Which team owns **Argo CD**, and what user-facing SLO proves it works?
* What remains available when **CI and registry** is down?
* Where is state durable, and how are restore and upgrade tested?

## My Experience Prompt

Describe a change to argo cd: state the constraint, the exact signal that selected the design, the rollback boundary, and the durable guardrail you added.

## Recall Check

1. What does **application repository** send to **CI and registry**?
2. Which component stores or reports authoritative state?
3. How does **live-state diff** affect **sync and health**?
4. Which capacity limit fails first at production scale?
5. When is a simpler managed alternative preferable?

## Related Notes

* [Category index](index.md)
* [Interview dashboard](../00-interview-dashboard.md)
