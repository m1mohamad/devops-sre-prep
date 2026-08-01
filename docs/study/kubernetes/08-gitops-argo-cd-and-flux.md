---
title: GitOps: Argo CD and Flux
tags: [kubernetes, platform-engineering]
aliases: [GitOps: Argo CD and Flux study note]
---

# GitOps: Argo CD and Flux

## 30-Second Answer

GitOps: Argo CD and Flux is the path from **application Git repository** to **drift reconciliation**. The essential handoffs are immutable image, environment Git repository, Argo CD or Flux, Kubernetes API. In production, I verify each handoff independently, keep its identity and state boundary visible, and operate it against availability, latency, security, and recovery objectives.

## Mental Model

```mermaid
flowchart LR
  N0[application Git repository] --> N1[immutable image] --> N2[environment Git repository] --> N3[Argo CD or Flux] --> N4[Kubernetes API] --> N5[drift reconciliation]
```

Read this diagram as a concrete sequence, not a generic maturity loop: a failure after **Kubernetes API** has different evidence and ownership from a failure at **immutable image**.

## Why It Exists

Without gitops: argo cd and flux, teams must manually coordinate application git repository, argo cd or flux, and drift reconciliation. The technology standardizes those interfaces so changes are repeatable, reviewable, and diagnosable. It is justified when the repeated operational risk exceeds the cost of owning the abstraction.

## How It Works

**application Git repository** owns stage 1; **immutable image** owns stage 2; **environment Git repository** owns stage 3; **Argo CD or Flux** owns stage 4; **Kubernetes API** owns stage 5; **drift reconciliation** owns stage 6. Follow resource IDs, revisions, events, and timestamps across these stages; an acknowledgement at one stage never proves completion at the next.

## Mechanisms

* **application Git repository:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **immutable image:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **environment Git repository:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **Argo CD or Flux:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **Kubernetes API:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **drift reconciliation:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.

## Production Architecture

Deploy application git repository with least privilege and an auditable change path. Isolate argo cd or flux by environment and failure domain, make drift reconciliation observable, and test loss of each dependency. Version the interface between stages so producers and consumers can roll independently.

## Failure Modes

| Failure | Evidence | Response |
|---|---|---|
| API or watch lag hides progress | Compare stage latency and revision at immutable image | Stop promotion and restore the last verified input |
| resource, IP, or storage capacity blocks convergence | Inspect saturation, quotas, events, and pending work at Argo CD or Flux | Add valid capacity or shed load; do not retry without a bound |
| a probe or policy reports a misleading serving state | Compare the user result with drift reconciliation and upstream state | Mitigate first, preserve evidence, then repair the faulty contract |

## Trade-offs

More automation across application git repository and drift reconciliation improves consistency but can propagate an error faster. Strong isolation narrows blast radius but increases cost and upgrades. Managed implementations reduce component toil; self-managed implementations offer control but require availability, backup, security patching, and on-call expertise.

## Lead-Level Follow-ups

* Which team owns **Argo CD or Flux**, and what user-facing SLO proves it works?
* What remains available when **immutable image** is down?
* Where is state durable, and how are restore and upgrade tested?

## My Experience Prompt

Describe a change to argo cd or flux: state the constraint, the exact signal that selected the design, the rollback boundary, and the durable guardrail you added.

## Recall Check

1. What does **application Git repository** send to **immutable image**?
2. Which component stores or reports authoritative state?
3. How does **Kubernetes API** affect **drift reconciliation**?
4. Which capacity limit fails first at production scale?
5. When is a simpler managed alternative preferable?

## Related Notes

* [Category index](index.md)
* [Interview dashboard](../00-interview-dashboard.md)
