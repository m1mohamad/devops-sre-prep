---
title: Golden Paths and Self-Service
tags: [platform-engineering, platform-engineering]
aliases: [Golden Paths and Self-Service study note]
---

# Golden Paths and Self-Service

## 30-Second Answer

Golden Paths and Self-Service is the path from **service catalog** to **scorecard and docs**. The essential handoffs are self-service template, repository creation, CI and IaC workflow, deployment environment. In production, I verify each handoff independently, keep its identity and state boundary visible, and operate it against availability, latency, security, and recovery objectives.

## Mental Model

```mermaid
flowchart LR
  N0[service catalog] --> N1[self-service template] --> N2[repository creation] --> N3[CI and IaC workflow] --> N4[deployment environment] --> N5[scorecard and docs]
```

Read this diagram as a concrete sequence, not a generic maturity loop: a failure after **deployment environment** has different evidence and ownership from a failure at **self-service template**.

## Why It Exists

Without golden paths and self-service, teams must manually coordinate service catalog, ci and iac workflow, and scorecard and docs. The technology standardizes those interfaces so changes are repeatable, reviewable, and diagnosable. It is justified when the repeated operational risk exceeds the cost of owning the abstraction.

## How It Works

**service catalog** owns stage 1; **self-service template** owns stage 2; **repository creation** owns stage 3; **CI and IaC workflow** owns stage 4; **deployment environment** owns stage 5; **scorecard and docs** owns stage 6. Follow resource IDs, revisions, events, and timestamps across these stages; an acknowledgement at one stage never proves completion at the next.

## Mechanisms

* **service catalog:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **self-service template:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **repository creation:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **CI and IaC workflow:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **deployment environment:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **scorecard and docs:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.

## Production Architecture

Deploy service catalog with least privilege and an auditable change path. Isolate ci and iac workflow by environment and failure domain, make scorecard and docs observable, and test loss of each dependency. Version the interface between stages so producers and consumers can roll independently.

## Failure Modes

| Failure | Evidence | Response |
|---|---|---|
| the abstraction hides a failure users must debug | Compare stage latency and revision at self-service template | Stop promotion and restore the last verified input |
| a mandatory path lacks an escape hatch or migration | Inspect saturation, quotas, events, and pending work at CI and IaC workflow | Add valid capacity or shed load; do not retry without a bound |
| adoption metrics count activity rather than developer outcomes | Compare the user result with scorecard and docs and upstream state | Mitigate first, preserve evidence, then repair the faulty contract |

## Trade-offs

More automation across service catalog and scorecard and docs improves consistency but can propagate an error faster. Strong isolation narrows blast radius but increases cost and upgrades. Managed implementations reduce component toil; self-managed implementations offer control but require availability, backup, security patching, and on-call expertise.

## Lead-Level Follow-ups

* Which team owns **CI and IaC workflow**, and what user-facing SLO proves it works?
* What remains available when **self-service template** is down?
* Where is state durable, and how are restore and upgrade tested?

## My Experience Prompt

Describe a change to ci and iac workflow: state the constraint, the exact signal that selected the design, the rollback boundary, and the durable guardrail you added.

## Recall Check

1. What does **service catalog** send to **self-service template**?
2. Which component stores or reports authoritative state?
3. How does **deployment environment** affect **scorecard and docs**?
4. Which capacity limit fails first at production scale?
5. When is a simpler managed alternative preferable?

## Related Notes

* [Category index](index.md)
* [Interview dashboard](../00-interview-dashboard.md)
