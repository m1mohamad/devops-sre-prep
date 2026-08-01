---
title: Platform System Map
tags: [architecture, study]
aliases: [System map]
---

# Platform System Map

## 30-Second Answer
A production platform is a chain of independently observable contracts, not one deployment tool.

```mermaid
flowchart LR
 Code --> CI --> Registry --> GitOps --> K8s[Kubernetes]
 K8s --> Edge --> Users
 K8s --> Telemetry --> Oncall
 IaC --> AWS --> K8s
```

Follow each edge by asking who authenticates, where state persists, how retries work, and what proves user impact. See the [architecture library](../architecture/index.md) and [dashboard](00-interview-dashboard.md).
