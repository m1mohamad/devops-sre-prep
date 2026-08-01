---
title: VPC Networking and Connectivity
tags: [aws, platform-engineering]
aliases: [VPC Networking and Connectivity study note]
---

# VPC Networking and Connectivity

## 30-Second Answer

VPC Networking and Connectivity is the path from **VPC CIDR** to **DNS**. The essential handoffs are public and private subnets, route tables, internet or NAT gateway, Transit Gateway, security groups and NACLs. In production, I verify each handoff independently, keep its identity and state boundary visible, and operate it against availability, latency, security, and recovery objectives.

## Mental Model

```mermaid
flowchart LR
  N0[VPC CIDR] --> N1[public and private subnets] --> N2[route tables] --> N3[internet or NAT gateway] --> N4[Transit Gateway] --> N5[security groups and NACLs] --> N6[DNS]
```

Read this diagram as a concrete sequence, not a generic maturity loop: a failure after **security groups and NACLs** has different evidence and ownership from a failure at **public and private subnets**.

## Why It Exists

Without vpc networking and connectivity, teams must manually coordinate vpc cidr, internet or nat gateway, and dns. The technology standardizes those interfaces so changes are repeatable, reviewable, and diagnosable. It is justified when the repeated operational risk exceeds the cost of owning the abstraction.

## How It Works

**VPC CIDR** owns stage 1; **public and private subnets** owns stage 2; **route tables** owns stage 3; **internet or NAT gateway** owns stage 4; **Transit Gateway** owns stage 5; **security groups and NACLs** owns stage 6; **DNS** owns stage 7. Follow resource IDs, revisions, events, and timestamps across these stages; an acknowledgement at one stage never proves completion at the next.

## Mechanisms

* **VPC CIDR:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **public and private subnets:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **route tables:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **internet or NAT gateway:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **Transit Gateway:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **security groups and NACLs:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **DNS:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.

## Production Architecture

Deploy vpc cidr with least privilege and an auditable change path. Isolate internet or nat gateway by environment and failure domain, make dns observable, and test loss of each dependency. Version the interface between stages so producers and consumers can roll independently.

## Failure Modes

| Failure | Evidence | Response |
|---|---|---|
| quota, IP, or zonal exhaustion defeats nominal capacity | Compare stage latency and revision at public and private subnets | Stop promotion and restore the last verified input |
| an IAM trust policy grants a wider principal than intended | Inspect saturation, quotas, events, and pending work at internet or NAT gateway | Add valid capacity or shed load; do not retry without a bound |
| a shared account or network dependency widens blast radius | Compare the user result with DNS and upstream state | Mitigate first, preserve evidence, then repair the faulty contract |

## Trade-offs

More automation across vpc cidr and dns improves consistency but can propagate an error faster. Strong isolation narrows blast radius but increases cost and upgrades. Managed implementations reduce component toil; self-managed implementations offer control but require availability, backup, security patching, and on-call expertise.

## Lead-Level Follow-ups

* Which team owns **internet or NAT gateway**, and what user-facing SLO proves it works?
* What remains available when **public and private subnets** is down?
* Where is state durable, and how are restore and upgrade tested?

## My Experience Prompt

Describe a change to internet or nat gateway: state the constraint, the exact signal that selected the design, the rollback boundary, and the durable guardrail you added.

## Recall Check

1. What does **VPC CIDR** send to **public and private subnets**?
2. Which component stores or reports authoritative state?
3. How does **security groups and NACLs** affect **DNS**?
4. Which capacity limit fails first at production scale?
5. When is a simpler managed alternative preferable?

## Related Notes

* [Category index](index.md)
* [Interview dashboard](../00-interview-dashboard.md)
