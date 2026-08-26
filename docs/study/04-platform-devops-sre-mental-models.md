---
title: Platform / DevOps / SRE Mental Models
tags: [study, interview, platform-engineering, devops, sre]
aliases: [Platform mental models]
---

# Platform / DevOps / SRE Mental Models

## How to Use This Page

This is a 10–15 minute recall sheet, not a replacement for the [Core Path](core-path/index.md), [interview week plan](03-senior-platform-interview-week.md), or topic deep dives. When a product detail disappears under interview pressure, reconstruct the answer from the system's boundaries and flows:

```text
What should exist?
What actually exists?
Who owns the next action?
What boundary is failing?
What evidence proves it?
What is the blast radius?
```

> Remember system boundaries, ownership, flows, and evidence. Product names are implementations of those deeper concepts.

---

## The 20 Core Concepts

| # | Mental model | Memory analogy | Reconstruct the answer |
|---:|---|---|---|
| 1 | **Desired vs actual state** | Thermostat: set temperature → measure reality → correct → repeat | Kubernetes controllers, Terraform, ArgoCD, and autoscaling compare intent with observation and act on a gap. Their reconciliation semantics are not identical. |
| 2 | **Control plane vs data plane** | Air traffic control vs airplanes | The control plane decides; the data plane executes or carries traffic. Ask whether the decision is wrong or execution is failing. |
| 3 | **Request → decision → execution** | Restaurant: order → assignment → cooking | Follow an API request through API server and scheduler/controllers to kubelet; use the same split for cloud APIs and CI/CD. |
| 4 | **Identity → permission → policy** | Passport → keycard → building rules | Trace IAM, RBAC, ServiceAccounts, OIDC/workload identity, and admission policy one authorization boundary at a time. |
| 5 | **Name → route → destination** | Contact name → GPS route → house | Trace DNS, load balancer, Ingress, Service, EndpointSlice, and routes rather than treating “networking” as one box. |
| 6 | **Labels describe; selectors choose** | Luggage tag → baggage search | A label records attributes; a selector finds matching objects. No match means no relationship or endpoint. |
| 7 | **Requests reserve; limits constrain** | Reservation vs boundary | Requests drive scheduler capacity accounting; limits are runtime enforcement boundaries. Limits do **not** reserve capacity. |
| 8 | **Taints repel; tolerations permit; affinity attracts** | Restricted room → access pass → preferred table | A toleration allows a Pod to remain eligible despite a taint; affinity influences selection. **A toleration does not force placement.** |
| 9 | **Startup → readiness → liveness** | Restaurant: opening → accepting customers → healthy enough to stay open | Startup protects initialization; readiness controls traffic eligibility; liveness controls restart. |
| 10 | **Horizontal vs vertical scaling** | More checkout lanes vs a faster checkout lane | HPA adds Pods; vertical scaling makes each unit bigger. Node autoscaling or Karpenter adds infrastructure capacity for Pods. |
| 11 | **Queue = shock absorber** | Waiting room between producer and worker | Kafka or SQS buffers bursts and enables backpressure, but queue depth and processing age expose overload. |
| 12 | **Cache trades freshness and complexity for speed** | Keep frequently used tools on your desk | Redis or a CDN reduces backend load and latency at the cost of invalidation, consistency, and failure-mode complexity. |
| 13 | **State changes architecture** | Replaceable cattle vs a diary containing unique information | Databases, PV/PVC, StatefulSets, and backups require explicit durability and recovery decisions; identity alone is not HA. |
| 14 | **Failure domain** | Do not put all eggs in one basket | Replicas help only when spread across the relevant Pod, node, AZ, or region failure boundary. |
| 15 | **Timeout → retry → backoff → jitter** | Knock → wait → retry later—not 10,000 people hammering the door | Bound waiting, retry only safe/transient failures, slow repeated attempts, and desynchronize clients. Otherwise retries amplify overload into a retry storm. |
| 16 | **Metrics = WHAT; logs = WHY; traces = WHERE** | Dashboard → diary → journey map | Use signals together: detect the symptom, explain an event, then locate delay or failure across boundaries. |
| 17 | **SLI measures; SLO targets; SLA promises** | Speedometer → target speed → contractual promise | Measure user-visible reliability, set an engineering objective, and distinguish it from an external commitment. |
| 18 | **Immutable artifact + declarative configuration** | Sealed box + instructions | Build a container image once; promote its identity while GitOps/CI/CD declares environment-specific desired state. |
| 19 | **Blast radius** | Electrical circuit breakers | Bound deployment, security, tenancy, and failure impact with isolation, staged rollout, and least privilege. |
| 20 | **Evidence before hypothesis** | Doctor diagnoses before prescribing | Senior troubleshooters establish scope and collect observations before changing the system; they verify both mitigation and cause. |

Use the [Kubernetes refresh](kubernetes/00-kubernetes-interview-refresh.md), [AWS foundation](aws/01-aws-platform-foundation.md), [IaC mental model](iac/01-iac-mental-model.md), and [observability notes](observability/index.md) when an interviewer asks for implementation depth.

---

# The Five Questions Behind Almost Every Problem

The opening six prompts collapse into five investigations: **intent and reality**, **owner**, **boundary**, **evidence**, and **blast radius**.

## What should exist?

```text
desired state
→ actual state
→ difference

Kubernetes:
Deployment wants 3
actual Pods = 2

Terraform:
3 subnets desired
2 exist

ArgoCD:
Git says v2
cluster runs v1

SRE:
SLO says 99.9%
observed is lower
```

The difference identifies the next question; it does not yet prove the cause.

## Who owns the next action?

```text
API server  = receptionist
etcd        = records
controller  = manager
scheduler   = placement planner
kubelet     = node worker
CRI         = container machinery
CNI         = network/roads
CSI         = storage integration
```

```text
Deployment wants 3 but only 2 Pods exist
→ controller / ReplicaSet path

Pod exists but Pending
→ scheduling / placement / capacity

Pod scheduled but cannot start
→ kubelet / runtime / image / CNI / CSI

Pod Running but NotReady
→ readiness / application / dependency

Pod Ready but users cannot reach it
→ Service / EndpointSlice / dataplane / Ingress / LB
```

> Do not memorize every failure mode. Find the component that owns the next state transition.

For the other questions, name the interface where expected behavior diverges, gather direct evidence at both sides, and ask how much shares that dependency or privilege.

---

# Troubleshooting Ladder

```text
INTENT
  ↓
OBJECT
  ↓
PLACEMENT
  ↓
EXECUTION
  ↓
HEALTH
  ↓
DISCOVERY
  ↓
NETWORK
  ↓
APPLICATION
  ↓
DEPENDENCY
```

In Kubernetes, walk the concrete chain and stop at the first failed transition:

```text
Deployment
→ ReplicaSet
→ Pod
→ Scheduler
→ Node
→ Kubelet
→ Container
→ Readiness
→ EndpointSlice
→ Service
→ Ingress/LB
→ User
```

Communicate the investigation like a senior engineer:

```text
Symptom
→ Scope
→ Recent change
→ Boundary
→ Evidence
→ Cause
→ Mitigation
→ Verification
→ Prevention
```

The [production troubleshooting note](kubernetes/10-production-troubleshooting.md) supplies commands; this ladder supplies their order.

---

# Networking Mental Model

```text
NAME
→ DESTINATION
→ PATH
→ POLICY
→ PROCESS
```

```text
api.company.com
→ DNS
→ Load Balancer
→ Ingress
→ Service
→ EndpointSlice
→ Pod IP
→ application port
```

```text
Does the name resolve?
Does it resolve correctly?
Can I reach the destination?
Is routing correct?
Does policy allow it?
Is something listening?
Is the application healthy?
```

This sequence works for Kubernetes, AWS, Linux, and traditional infrastructure because it tests interfaces, not brands. Go deeper with [Kubernetes networking](kubernetes/05-networking-cni-services-ingress.md) or [TCP, DNS, routing, and firewalls](linux-networking/04-tcp-dns-routing-and-firewalls.md).

---

# Security Mental Model

```text
WHO
→ CAN DO WHAT
→ TO WHAT
→ UNDER WHICH CONDITIONS
```

```text
AWS:
Pod / IAM role
→ s3:GetObject
→ bucket/object
→ account / tags / resource policy / network conditions

Kubernetes:
ServiceAccount
→ get/list
→ Secrets
→ namespace
```

For an EKS Pod receiving S3 `AccessDenied`, trace the whole identity and policy chain:

```text
Pod
→ ServiceAccount
→ workload identity
→ IAM role
→ IAM policy
→ resource policy
→ S3
```

> Find the first broken authorization boundary rather than saying “check IAM”.

See [IAM and workload identity](aws/03-iam-and-workload-identity.md) for trust and policy details.

---

# Scheduling Mental Model

```text
Labels describe.
Selectors choose.

Taints repel.
Tolerations permit.
Affinity attracts.

Requests schedule.
Limits constrain.
```

Requests are inputs to placement and reserved-capacity accounting; runtime limits constrain resource use. A toleration makes placement possible but does not select a node. See [scheduling and capacity](kubernetes/04-scheduling-and-capacity.md).

---

# Health Mental Model

```text
Startup:
Have I completed initialization?

Readiness:
Should I receive traffic?

Liveness:
Should kubelet restart me?
```

```text
Running != Ready
```

Process existence, traffic eligibility, and recoverability are different facts. A poor liveness probe can turn dependency trouble into a restart loop.

---

# Scaling Mental Model

```text
Horizontal
= more

Vertical
= bigger
```

```text
traffic rises
→ HPA wants more Pods
→ some Pods Pending
→ insufficient node capacity
→ Karpenter / Cluster Autoscaler adds capacity
→ Pods schedule
```

Workload scaling changes application replicas or size; infrastructure scaling supplies nodes. Neither fixes a saturated downstream dependency by itself.

---

# Reliability Mental Model

```text
Avoid
→ Absorb
→ Recover
→ Learn
```

| Stage | Examples |
|---|---|
| **Avoid** | Tests, validation, capacity planning, safe rollout |
| **Absorb** | Replicas, multiple AZs, queues, caches, rate limits, circuit breakers |
| **Recover** | Rollback, restart, failover, backup/restore, DR |
| **Learn** | Metrics, logs, traces, postmortems, automation |

A complete design addresses all four stages instead of claiming failures can be prevented. Use the [SRE notes](observability/04-alerting-slos-and-error-budgets.md) to connect reliability to user outcomes.

---

# CI/CD Mental Model

```text
CODE
→ VALIDATE
→ BUILD
→ TEST
→ SCAN
→ PACKAGE
→ PUBLISH
→ DECLARE DESIRED VERSION
→ DEPLOY / RECONCILE
→ VERIFY
→ OBSERVE
→ ROLLBACK
```

Jenkins, GitHub Actions, GitLab CI, Helm, registries, ArgoCD, and Flux occupy one or more positions in this chain. Separate artifact creation from promotion and delivery.

> Where in the delivery chain does this tool operate?

See [code to production](cicd/01-code-to-production.md) and [GitOps continuous delivery](cicd/05-gitops-continuous-delivery.md).

---

# Reconciliation Is Everywhere

```text
Terraform
desired infrastructure
→ actual infrastructure

ArgoCD
desired Git state
→ actual Kubernetes state

Kubernetes
desired workload state
→ actual workload state
```

Terraform plans and applies infrastructure changes, ArgoCD compares and syncs Git state, and Kubernetes controllers continuously act on resource state. The shared comparison question is useful; the tools do not have identical reconciliation semantics.

> What should reality look like, what does reality look like now, and who closes the gap?

---

# State and Storage Mental Model

```text
Persist
→ Replicate
→ Backup
→ Restore
```

```text
persistent volume != replication
replication != backup
backup != tested recovery
StatefulSet != database HA
```

```text
Where does state live?
What if the process dies?
What if the node dies?
What if the AZ dies?
What if data is corrupted?
How is it restored?
```

Durability, availability, point-in-time protection, and proven recovery are separate requirements. See [Kubernetes storage](kubernetes/06-storage-and-csi.md) and [database backup, restore, and HA](databases/02-postgresql-backup-restore-and-ha.md).

---

# Observability Mental Model

```text
Metrics = WHAT
Logs    = WHY
Traces  = WHERE
```

```text
RED:
Rate
Errors
Duration
```

Use RED for request-driven services.

```text
USE:
Utilization
Saturation
Errors
```

Use USE for resources and capacity.

```text
SLI = measure
SLO = target
SLA = promise
```

Start with the user-visible symptom, then choose the signal that can confirm or reject a boundary hypothesis. See [metrics, logs, and traces](observability/01-metrics-logs-and-traces.md).

---

# Failure Domains and Blast Radius

```text
What if:

process fails?
Pod fails?
node fails?
AZ fails?
region fails?
dependency fails?
deployment is bad?
credentials are compromised?
```

> How much of the system fails with it?

Resilience spreads replicas across independent failure domains; security and deployment design restrict privilege and rollout scope. Both are blast-radius engineering.

---

# Follow Boundaries, Not Products

```text
USER
→ DNS
→ LOAD BALANCER
→ INGRESS
→ SERVICE
→ POD
→ APPLICATION
→ CACHE
→ DATABASE
→ EXTERNAL DEPENDENCY
```

```text
What changed?
Where does latency begin?
What is the first failing boundary?
What evidence proves it?
```

> Follow boundaries and evidence rather than randomly naming products.

The [production platform scenario](04-production-platform-scenario.md) is the next step for applying this method to one connected system.

---

# Ultimate Memory Card

```text
1. Desired state → Actual state → Reconcile

2. Control plane decides → Data plane executes

3. Identity → Permission → Resource

4. Name → Route → Destination

5. Requests schedule → Limits constrain

6. Taints repel → Tolerations permit → Affinity attracts

7. Startup initializes → Readiness serves → Liveness restarts

8. Metrics = WHAT → Logs = WHY → Traces = WHERE

9. Replicate != Backup → Backup != Recovery

10. Symptom → Scope → Boundary → Evidence → Cause → Fix → Verify → Prevent
```

Leadership anchor:

```text
People
→ Process
→ Platform
```

```text
Engineer
→ solves the problem

Senior Engineer
→ solves the class of problems

Platform / DevOps Lead
→ builds the system, guardrails, and team capability
  that make that class of problems safe and repeatable
```

> Product names change. The mental models, system boundaries, ownership, and evidence remain transferable.
