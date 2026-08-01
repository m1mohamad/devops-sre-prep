---
title: Prometheus and Grafana
tags: [observability, platform-engineering]
aliases: [Prometheus and Grafana study note]
---

# Prometheus and Grafana

## 30-Second Answer

Prometheus and Grafana is the path from **Prometheus scrape** to **Grafana**. The essential handoffs are service discovery, time-series database, recording and alert rules, Alertmanager. In production, I verify each handoff independently, keep its identity and state boundary visible, and operate it against availability, latency, security, and recovery objectives.

## Mental Model

```mermaid
flowchart LR
  N0[Prometheus scrape] --> N1[service discovery] --> N2[time-series database] --> N3[recording and alert rules] --> N4[Alertmanager] --> N5[Grafana]
```

Read this diagram as a concrete sequence, not a generic maturity loop: a failure after **Alertmanager** has different evidence and ownership from a failure at **service discovery**.

## Why It Exists

Without prometheus and grafana, teams must manually coordinate prometheus scrape, recording and alert rules, and grafana. The technology standardizes those interfaces so changes are repeatable, reviewable, and diagnosable. It is justified when the repeated operational risk exceeds the cost of owning the abstraction.

## How It Works

**Prometheus scrape** owns stage 1; **service discovery** owns stage 2; **time-series database** owns stage 3; **recording and alert rules** owns stage 4; **Alertmanager** owns stage 5; **Grafana** owns stage 6. Follow resource IDs, revisions, events, and timestamps across these stages; an acknowledgement at one stage never proves completion at the next.

## Mechanisms

* **Prometheus scrape:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **service discovery:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **time-series database:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **recording and alert rules:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **Alertmanager:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **Grafana:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.

## Production Architecture

Deploy prometheus scrape with least privilege and an auditable change path. Isolate recording and alert rules by environment and failure domain, make grafana observable, and test loss of each dependency. Version the interface between stages so producers and consumers can roll independently.

## Failure Modes

| Failure | Evidence | Response |
|---|---|---|
| cardinality or volume overloads ingestion | Compare stage latency and revision at service discovery | Stop promotion and restore the last verified input |
| sampling removes the only evidence for a rare failure | Inspect saturation, quotas, events, and pending work at recording and alert rules | Add valid capacity or shed load; do not retry without a bound |
| an unactionable alert pages without user impact | Compare the user result with Grafana and upstream state | Mitigate first, preserve evidence, then repair the faulty contract |

## Trade-offs

More automation across prometheus scrape and grafana improves consistency but can propagate an error faster. Strong isolation narrows blast radius but increases cost and upgrades. Managed implementations reduce component toil; self-managed implementations offer control but require availability, backup, security patching, and on-call expertise.

## Lead-Level Follow-ups

* Which team owns **recording and alert rules**, and what user-facing SLO proves it works?
* What remains available when **service discovery** is down?
* Where is state durable, and how are restore and upgrade tested?

## My Experience Prompt

Describe a change to recording and alert rules: state the constraint, the exact signal that selected the design, the rollback boundary, and the durable guardrail you added.

## Recall Check

1. What does **Prometheus scrape** send to **service discovery**?
2. Which component stores or reports authoritative state?
3. How does **Alertmanager** affect **Grafana**?
4. Which capacity limit fails first at production scale?
5. When is a simpler managed alternative preferable?

## Related Notes

* [Category index](index.md)
* [Interview dashboard](../00-interview-dashboard.md)
