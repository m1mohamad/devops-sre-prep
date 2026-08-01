---
title: Kubernetes Questions
tags: [interview, study]
aliases: [Kubernetes Questions practice]
---

# Kubernetes Questions

Use these prompts for closed-book rehearsal. Answer in 30 seconds, expand mechanism and trade-offs for three minutes, then connect one honest experience. Full answer frameworks are in the [Interview Companion](../../interview/index.md).

* Walk me through what happens after a Deployment is submitted.
* How would you troubleshoot Pods stuck in Pending?
* Why can a Pod be Running but absent from Service endpoints?
* How do informers and work queues make controllers scalable?
* How would you design a safe EKS control-plane and node upgrade?
* When do taints, affinity, and topology spread solve different problems?
* How do requests, limits, HPA, and node autoscaling interact?
* What happens from a Service virtual IP to a Pod?
* How would you diagnose intermittent cluster DNS failures?
* How do CSI provisioning and volume attachment fail?
* How do finalizers and owner references affect deletion?
* When should you build a CRD and controller instead of a service?
* How would you secure admission webhooks against an outage?
* Compare Helm packaging with Kustomize overlays.
* When would you avoid a service mesh?

## Practice Loop

```mermaid
flowchart LR
  Prompt --> Short[30-second answer] --> Deep[Mechanics and trade-offs] --> Story[Experience evidence] --> Review
```

Avoid memorized scripts: state assumptions and test them.
