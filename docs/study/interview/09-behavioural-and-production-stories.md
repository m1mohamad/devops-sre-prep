---
title: Behavioural and Production Stories
tags: [interview, study]
aliases: [Behavioural and Production Stories practice]
---

# Behavioural and Production Stories

Use these prompts for closed-book rehearsal. Answer in 30 seconds, expand mechanism and trade-offs for three minutes, then connect one honest experience. Full answer frameworks are in the [Interview Companion](../../interview/index.md).

* Pods are Pending only in one Availability Zone; lead the incident.
* Argo CD repeatedly reverts a field mutated by another controller.
* A signed but incompatible container image reached production.
* Terraform reports a lock while no pipeline appears active.
* Certificates stopped renewing before a holiday freeze.
* DNS resolution works from laptops but fails from Pods.
* Database connections are exhausted after a harmless-looking rollout.
* LLM p99 latency doubled while request volume stayed flat.
* An EKS node replacement evicts too many replicas at once.
* Users see 502 responses although every readiness probe is green.

## Practice Loop

```mermaid
flowchart LR
  Prompt --> Short[30-second answer] --> Deep[Mechanics and trade-offs] --> Story[Experience evidence] --> Review
```

Avoid memorized scripts: state assumptions and test them.
