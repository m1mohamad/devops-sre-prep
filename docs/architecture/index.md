---
title: Architecture Library
tags: [architecture, study]
aliases: [System designs]
---

# Architecture Library

Each page traces a concrete control or request path and names ownership, security, scale, and failure boundaries.

* [Code to Production](code-to-production.md) — Move one reviewed commit and one immutable artifact through verification and controlled exposure.
* [Kubernetes Control Plane](kubernetes-control-plane.md) — Accept declarative intent durably and converge it without coupling clients to node execution.
* [Kubernetes Request Lifecycle](kubernetes-request-lifecycle.md) — Trace a Deployment from API admission to a ready Service endpoint.
* [Kubernetes Networking](kubernetes-networking.md) — Give Pods routable identities and stable service discovery while enforcing explicit policy.
* [GitOps with Argo CD](gitops-argocd.md) — Continuously compare reviewed Git intent with live Kubernetes objects and expose drift.
* [Terraform AWS Platform](terraform-aws-platform.md) — Provision account and network foundations with isolated state, review, and recovery.
* [EKS Production Platform](eks-production-platform.md) — Operate multi-AZ workloads across controlled node, identity, traffic, and upgrade boundaries.
* [Observability Pipeline](observability-pipeline.md) — Collect, transform, store, and query telemetry without making applications depend on the backend.
* [Service Mesh](service-mesh.md) — Apply workload identity and selected traffic policy between services while pricing dataplane cost.
* [Custom Controller](custom-controller.md) — Turn a domain API into idempotently reconciled Kubernetes and external resources.
* [AI Inference Platform](ai-inference-platform.md) — Serve versioned models on scarce GPUs within token-latency and data-governance objectives.
* [Multi-Region Platform](multi-region-platform.md) — Survive a regional loss without unsafe writes, hidden data loss, or untested DNS behavior.
* [Incident Response Loop](incident-response-loop.md) — Convert detection into coordinated mitigation, learning, and verified prevention.
