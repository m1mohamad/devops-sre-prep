---
title: Seven-Day Senior Platform Interview Plan
tags:
  - interview
  - platform-engineering
  - kubernetes
  - sre
  - study-plan
aliases:
  - Senior Platform Interview Week
  - Technical Interview Week
---

# Seven-Day Senior Platform Interview Plan

Use this focused path for approximately 2–2.5 hours per day. Retrieval beats endless reading: close the notes, draw the system, answer aloud, then reopen only to correct gaps. Keep personal examples truthful; use **[replace with a real example from your experience]** where evidence is missing.

## Daily Study Loop

* **45 minutes:** assigned reading, following links only for a weak concept.
* **15 minutes:** closed-book redraw and recall.
* **30 minutes:** interview questions answered aloud.
* **15 minutes:** break.
* **45 minutes:** weakest area, incident, or system-design practice.

End by writing three facts you retrieved, one misconception you corrected, and the first topic for tomorrow. The schedule totals 2.5 hours; shorten the weakest-area block to 15–30 minutes when only 2–2.25 hours are available.

## Day 1 — Kubernetes Architecture and Lifecycle

Read the [Kubernetes Interview Memory Refresh](kubernetes/00-kubernetes-interview-refresh.md) from its mental model through Deployment lifecycle. Deep dive into [Control Plane](kubernetes/02-control-plane.md) and [Reconciliation and Controllers](kubernetes/03-reconciliation-and-controllers.md).

Practice drawing the control plane, tracing Deployment → ReplicaSet → Pod → readiness → Service, and answering five Kubernetes questions aloud. Your answer must distinguish API acceptance, controller convergence, scheduler placement, and kubelet execution.

## Day 2 — Scheduling, Resources, Scaling, and Disruption

Refresh requests/limits, QoS, placement, taints/tolerations, affinity, topology spread, HPA, node autoscaling, Karpenter, PDBs, draining, and termination. Use [Scheduling and Capacity](kubernetes/04-scheduling-and-capacity.md) only to repair gaps.

Practice Pending Pod scenarios caused by resources, topology, PVCs, GPUs, node-group limits, and cloud quota. Explain why HPA and node provisioning are independent and why a PDB can stop a drain.

## Day 3 — Networking

Refresh CNI, Pod IPs, CoreDNS, Services, EndpointSlices, kube-proxy/eBPF, NetworkPolicy, Ingress, Gateway, LoadBalancer, and TLS. Deep dive with [Networking](kubernetes/05-networking-cni-services-ingress.md).

Diagnose four scenarios aloud: external 502, DNS failure, empty endpoints, and one-node-only failure. For each, state scope, path, first evidence, and a falsifiable hypothesis rather than proposing an immediate restart.

## Day 4 — Storage and Security

Refresh PVC/PV, StorageClass, CSI, topology, snapshots, RBAC, ServiceAccounts, workload identity, NetworkPolicy, Pod security, admission, and CRDs. Use [Storage and CSI](kubernetes/06-storage-and-csi.md) and [CRDs, Operators, and Admission](kubernetes/07-crds-operators-and-admission.md).

Practice explaining trust boundaries: Kubernetes RBAC versus cloud IAM versus application authorization versus network policy. Trace one zonal volume from claim to mount and explain why a snapshot is not automatically application-consistent.

## Day 5 — EKS, IaC, CI/CD, and GitOps

Connect Kubernetes to [Terraform](iac/index.md), [AWS networking](aws/02-vpc-networking-and-connectivity.md), [EKS](aws/04-eks-production-design.md), ECR, CI systems, immutable digests, SBOMs, provenance, signing, Argo CD/Flux, and rollback. Review [GitOps](kubernetes/08-gitops-argo-cd-and-flux.md) and the [Core Path](core-path/index.md).

Draw source → CI → registry → reviewed intent → GitOps → EKS. Explain shared responsibility and why Synced/Healthy does not prove business correctness.

## Day 6 — AI, Databases, Reliability

Focus on [GPU scheduling](ai-platform/02-gpu-nodes-and-scheduling.md), [model serving](ai-platform/04-model-serving-kserve-vllm-triton.md), queue saturation, [PostgreSQL and Redis](databases/index.md), SLI/SLOs, metrics/logs/traces, incident reasoning, capacity, and cost.

Practice an inference latency incident where CPU is normal. Correlate GPU memory/utilization, queue depth, model revision, dependency latency, and user SLOs. Adding GPUs is mitigation until evidence establishes the corrective action.

## Day 7 — Closed-Book Interview Day

Read no new material. Complete **10 Kubernetes questions, 5 platform questions, 3 incidents, 2 system designs, and 2 leadership stories**. Use the [closed-book Kubernetes questions](interview/02-kubernetes-questions.md), [system-design scenarios](interview/08-system-design-scenarios.md), and [production simulator](../simulator/index.md).

Structure every response as **Principle → design/action → trade-off → evidence → operational result**. For leadership and incident results, use only real experience; write **[replace with a real example from your experience]** rather than inventing an outcome. Finish with the [Platform Interview Rapid Review](interview/10-platform-interview-rapid-review.md), then stop studying and rest.

