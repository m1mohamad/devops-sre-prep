# GitOps

## Executive Summary

GitOps is a core platform engineering capability because it turns individual engineering work into repeatable, observable, and secure production outcomes. Staff engineers treat it as a system of feedback loops rather than a checklist.

!!! tip "Mental model"
    Ask what state exists, who owns it, how it changes, and how operators know when reality diverges from intent.

```mermaid
---
title: GitOps Mental Model
---
flowchart LR
  Intent[GitOps Intent] --> Control[Control Plane]
  Control --> Runtime[Runtime State]
  Runtime --> Signals[Metrics Logs Traces]
  Signals --> Decision[Engineering Decision]
  Decision --> Intent
```

## Why this exists

Teams need a shared abstraction that reduces cognitive load while preserving escape hatches for production incidents. Without gitops, organizations rely on tribal knowledge, manual runbooks, and heroics.

## Historical evolution

| Era | Practice | Limitation | Modern replacement |
|---|---|---|---|
| Manual | Tickets and shell access | Slow and inconsistent | Self-service workflows |
| Scripted | Bash automation | Hidden state | Declarative APIs |
| Platform | Productized capability | Requires governance | Golden paths |

## Deep technical explanation

The implementation combines APIs, controllers, policy, telemetry, and documentation. The goal is not to hide complexity; it is to put complexity behind stable contracts that can be tested, reviewed, and evolved.

```mermaid
---
title: GitOps Internal Architecture
---
flowchart TB
  Users[Engineers] --> Portal[Developer Portal]
  Portal --> API[Platform API]
  API --> Policy[Policy Engine]
  API --> Controller[Controller/Reconciler]
  Controller --> Infra[Cloud and Cluster Resources]
  Infra --> Telemetry[Telemetry Backend]
  Telemetry --> Portal
```

## Internal architecture

??? note "Collapsible operator detail"
    Controllers should be idempotent, observable, and safe to retry. Every mutation should have an owner, audit trail, and rollback plan.

## Production example

A product team ships a customer-facing change through a golden path. The platform validates policy, builds artifacts, deploys with progressive delivery, and exposes dashboards before broad rollout.

## Failure scenarios

| Failure | Symptom | First check | Mitigation |
|---|---|---|---|
| Drift | Desired and live state differ | Reconciler status | Pause, diff, reconcile |
| Capacity | Queues grow | Saturation metrics | Scale or shed load |
| Policy | Deployment blocked | Admission logs | Fix ownership metadata |

## Troubleshooting

1. Confirm user impact and blast radius.
2. Compare desired state, control-plane state, and runtime state.
3. Read recent changes before restarting components.
4. Prefer rollback over speculative fixes.

## Platform Engineer perspective

Design the paved road, defaults, documentation, and telemetry so product teams can move quickly without bypassing controls.

## Staff Engineer perspective

Focus on boundaries, failure domains, organizational ownership, migration paths, and long-term operability.

## Common interview questions

- How do you detect drift?
- Which SLO proves this capability is healthy?
- What should be centralized versus delegated?

## Key takeaways

!!! success "Remember"
    Mature platforms convert repeated operational judgment into productized, observable workflows.

## References

- Kubernetes documentation
- CNCF landscape
- AWS Well-Architected Framework


---

## Knowledge graph

### Prerequisites

- Software Delivery, Git, and Kubernetes reconciliation
- [Handbook dependency map](../knowledge-graph/index.md#capability-dependency-graph)

### Related chapters

[Software Delivery](software-delivery.md) · [Kubernetes](kubernetes.md) · [Security](security.md) · [Reliability](reliability.md)

### Next topics

Argo CD and Flux · Progressive delivery · Infrastructure reconciliation

### Common confusions

!!! warning "Do not conflate these concepts"
    GitOps is not merely YAML in Git: an automated agent must continuously reconcile and report drift.

### Industry example

A pull request changes desired state; a controller applies it and an SLO-driven rollout gates promotion.

### Interview questions

- How is an emergency change handled without permanent drift?
- What belongs outside a Git repository?

### Further reading

- [opengitops.dev](https://opengitops.dev/)
- [argo-cd.readthedocs.io](https://argo-cd.readthedocs.io/)
- [Technology relationships and comparisons](../knowledge-graph/index.md#technology-relationships)
