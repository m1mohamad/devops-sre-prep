---
title: Core Path Recall — Ideal Answers
tags:
  - core-path
  - recall
  - interview
  - answers
aliases:
  - Core Path Answer Key
  - Core Path Ideal Answers
---

# Core Path Recall — Ideal Answers

Attempt all ten questions in the [Core Path](index.md#recall-exercise) before reviewing this page. These are reference answers, not scripts to memorize.

## 1. Four stores, four responsibilities

**Ideal answer**

Terraform state, GitOps intent, a registry, and PostgreSQL backups preserve different kinds of truth at different system boundaries. Terraform state maps declared infrastructure resource addresses to provider objects and records infrastructure metadata needed to calculate changes. It is Terraform's operational mapping; it is not a copy of every real resource or its application data.

GitOps stores desired deployment configuration and version intent: which artifact and configuration an environment should reconcile. A registry stores the immutable deployable artifact bytes plus associated metadata such as manifest, digest, SBOM, provenance, and signatures. PostgreSQL backups preserve restorable business data and transaction history at a defined recovery point.

None substitutes for another. Each has different ownership, consistency behavior, retention, security sensitivity, backup, and recovery procedures. Restoring Terraform state changes Terraform's knowledge and does not restore application data. Restoring a database does not restore a Deployment's intended image or cloud mapping. Reverting Git can select an older digest, but it cannot recreate missing artifact bytes. Recovery therefore restores each required store coherently and verifies the resulting user capability.

**Key distinctions**

- State maps infrastructure intent to provider objects; Git declares deployment intent; a registry preserves executable content; a database backup preserves business truth.
- Their recovery points may differ, so runbooks must consider ordering, compatibility, authorization, and verification rather than treating “backup” as one mechanism.
- A desired reference without its artifact bytes is not deployable, and infrastructure reconstruction without business data is not application recovery.

**Common weak answer**

“They are all backups of the platform, so restoring any one of them should recreate production.”

## 2. Evidence attached to one immutable image

**Ideal answer**

A promotable image begins with a reviewed source change and a controlled build. The pipeline records tests, linting, dependency checks, an image vulnerability scan, an SBOM describing contents, provenance describing source and build process, and a signature binding an authorized identity to the result. Policy approval evaluates that evidence, and environment validation may prove that the same candidate behaves correctly under relevant integration or progressive-delivery checks.

The unit promoted is the immutable digest. Build once and promote that exact digest between environments. Rebuilding for production can produce different bytes because dependencies, timestamps, base images, or tooling may change; earlier tests, scans, provenance, or approval then may no longer apply. Different bytes also make incident correlation and rollback ambiguous. A tag is a mutable human reference such as a release name, while the digest is the content identity. Environment-specific configuration may vary through reviewed intent, but the application artifact remains constant so evidence follows what actually runs.

**Key distinctions**

- Tests show behavior; scans and an SBOM describe known content risk; provenance and signature establish origin and authorization. No single item replaces the others.
- A digest identifies exact content; a tag points humans or automation to content and may be moved unless policy prevents it.
- Promotion authorizes existing bytes for another environment; rebuilding manufactures a new, not-yet-proven artifact.

**Common weak answer**

“Use the same image tag in production; rebuilding is harmless because the Dockerfile and source commit are unchanged.”

## 3. Argo CD health is deployment evidence

**Ideal answer**

Argo CD can provide evidence that live resources match the desired Git state, reconciliation completed, and supported Kubernetes resource health conditions satisfy its configured heuristics. For example, it can observe whether a Deployment reports available replicas. This is valuable control-plane and rollout evidence.

It cannot prove business correctness, correct fraud decisions, acceptable user latency, dependency health, peak-load behavior, model quality, absence of data corruption, or correct application semantics. A shallow readiness check and an Available Deployment may coexist with incorrect results, a slow downstream dependency, or a model that fails only under production batching.

> Synced and Healthy is deployment evidence, not complete production evidence.

Production judgment combines GitOps state with user SLIs, business checks, logs, traces, dependency telemetry, and revision-aware progressive delivery. When users report errors, investigate that evidence even if reconciliation is green; if the rollout is implicated and rollback is state-safe, pause or revert it and verify through the original user signal.

**Key distinctions**

- Sync compares desired and live resource intent; health evaluates known resource conditions. Neither executes the full business contract.
- Kubernetes readiness is itself only the configured probe at a moment, not proof of correctness, load tolerance, or dependency behavior.
- Deployment evidence answers “did the intended resources reconcile?”; production evidence answers “is the user capability correct and reliable?”

**Common weak answer**

“Healthy means the application and all its dependencies are working, so user errors must be unrelated.”

## 4. Discovery, readiness, and two scaling loops

**Ideal answer**

A Service provides stable discovery and virtual routing for a changing workload. EndpointSlices represent its current backend addresses and readiness conditions. A readiness probe informs whether a Pod should be treated as ready and included as a traffic endpoint; it does not create resources.

HPA changes the desired Pod replica count from configured workload metrics such as CPU, memory, or a suitable custom signal. The Deployment creates Pods and the scheduler tries to place them on nodes that satisfy resource requests and placement constraints. If new Pods are unschedulable for capacity reasons, node autoscaling can add suitable nodes, subject to node-group bounds, cloud capacity, and quota. After nodes register, the scheduler can place Pods; after startup and successful readiness, endpoints become eligible for Service traffic.

Readiness does not add capacity. HPA does not create nodes. Node autoscaling does not fix bad readiness. All loops depend on correct requests, metrics, selectors, affinity, taints, volumes, capacity types, and available provider quota. Their events and statuses must be correlated rather than treating “autoscaling” as one controller.

**Key distinctions**

- HPA responds at the workload replica layer; node autoscaling responds to capacity-related unschedulability at the infrastructure layer.
- Service and EndpointSlice route to backends; readiness controls eligibility, not the amount of compute behind them.
- More replicas cannot help if the metric is wrong, Pods cannot schedule, or the bottleneck is a shared dependency.

**Common weak answer**

“When readiness fails, HPA creates more nodes and the Service automatically adds capacity.”

## 5. Identity and permission along the payment path

**Ideal answer**

Authentication validates who the caller is, commonly at an edge, gateway, or dedicated authentication service by validating credentials or a token. A gateway may enforce coarse policy such as audience, route entitlement, or rate limits. The payment service must still enforce operation-level authorization using business context: for example, whether this identity may create this payment for this account and amount. A valid identity is not universal permission.

Service-to-service calls also require workload identity and scoped authorization rather than trusting network location alone. The payment, fraud, and model services should authenticate peers and allow only required operations. Separately, cloud APIs and secret stores authorize the workload identity—such as a role mapped from a Kubernetes service account—to particular secrets or resources. Kubernetes RBAC authorizes Kubernetes API operations and is not a substitute for business authorization.

> Authentication establishes who the caller is; authorization determines whether that identity may perform this specific operation.

The decision and relevant caller or workload identity should be auditable without leaking credentials or prohibited sensitive data.

**Key distinctions**

- Edge authentication and coarse gateway controls do not replace contextual authorization in the service that owns the business operation.
- User identity, workload identity, Kubernetes API authorization, and cloud IAM are related but distinct trust and policy boundaries.
- Network reachability establishes a possible path, not authority to use it.

**Common weak answer**

“The gateway validates the token, so every downstream service can trust and permit the request.”

## 6. Durable publication and bounded duplicate handling

**Ideal answer**

An outbox closes the dangerous gap between updating business state and publishing an event. The application writes the business update and an outbox record in the same durable database transaction. A separate publisher later reads committed outbox records and sends them to the broker. A crash can cause publication to be retried, so duplicate delivery remains possible.

An idempotency key lets a producer or consumer recognize the same logical operation and return or preserve the original business effect rather than charging or updating twice. Capped retries with appropriate backoff handle transient faults without infinite retry storms or permanent resource consumption. A repeatedly failing poison message moves to a dead-letter destination after the cap, where it is visible for diagnosis. Replay must be authorized, observable, and idempotent; otherwise replay can repeat harmful side effects.

Together these mechanisms support practical at-least-once processing and controlled recovery. They do not create magical exactly-once execution across a database, broker, network, and consumers. Business uniqueness constraints and handler design remain essential.

**Key distinctions**

- The outbox makes business state and publication intent atomic locally; it does not guarantee a single network delivery.
- Idempotency protects business effects from duplicates; retry caps protect the system from unbounded amplification.
- A dead-letter destination preserves failed work for governed investigation; it is not a bin to ignore or blindly replay.

**Common weak answer**

“The outbox guarantees exactly-once delivery, and the dead-letter queue can be replayed whenever convenient.”

## 7. Federated Pod identity for secret access

**Ideal answer**

The identity chain is:

```text
Kubernetes service account
→ projected service-account token
→ cloud workload-identity trust
→ scoped cloud IAM role or service account
→ External Secrets or application SDK
→ secret store
```

The Pod runs as a specific Kubernetes service account and receives a projected, bounded service-account token. Cloud workload-identity configuration validates that token and trusts the specific cluster, namespace, and service-account relationship, then issues short-lived cloud credentials for a scoped IAM role or service account. External Secrets can use that identity to fetch and materialize an allowed secret, or the application SDK can retrieve it directly when that contract is preferable.

AWS implementations include EKS Pod Identity or IRSA; GCP provides Workload Identity Federation for GKE. In every case, both sides of trust must be correct: the Kubernetes identity and cloud trust mapping. IAM permissions scope the exact secret or API actions required. No long-lived cloud access key is stored in an image, Git repository, or Kubernetes manifest, and access remains auditable and revocable.

**Key distinctions**

- The Kubernetes service-account token is exchanged or attested for short-lived cloud credentials; it is not itself a static cloud key.
- Trust answers which Kubernetes identity may assume the role; permissions answer what that resulting identity may do.
- External Secrets is a delivery mechanism, while the cloud secret store remains the controlled source and cloud IAM remains the authorization boundary.

**Common weak answer**

“Put an AWS access key in a Kubernetes Secret and mount it read-only into every Pod that needs secrets.”

## 8. Correlating a user SLI to model and infrastructure

**Ideal answer**

Useful release and topology attributes include commit SHA, image digest, GitOps commit or application revision, Deployment or ReplicaSet revision, model revision, namespace, Pod, node, cluster, region or zone, and service. Trace context connects a request across payment, fraud, and model spans. A trace ID and, where policy permits, a request or payment correlation ID allow deeper investigation in traces or logs.

The investigation path is:

```text
payment p95 alert
→ affected service and revision
→ trace
→ fraud/model span
→ model revision
→ Pod
→ node
→ GPU and node metrics
```

The p95 alert first establishes the affected service, cluster/region, and time. Exemplars or sampled traces locate where time accumulated. Resource attributes and application telemetry identify the model revision and Pod; Kubernetes metadata maps the Pod to a node; node and accelerator telemetry then shows GPU memory, utilization, restarts, or capacity pressure. Deployment annotations and GitOps metadata map runtime evidence back to immutable artifact and reviewed intent.

Prometheus metric labels must remain bounded. Unrestricted payment IDs, request IDs, and trace IDs are high cardinality and should generally live in appropriately protected logs or traces, with exemplars or controlled correlation—not become metric dimensions.

**Key distinctions**

- Release identity explains which bytes and configuration ran; topology identity explains where they ran; trace context explains where request time went.
- Model revision must be explicit because an application image or Pod name alone may not identify loaded model content.
- Correlation identifiers can be sensitive and high cardinality, requiring storage, retention, and access appropriate to logs or traces.

**Common weak answer**

“Add payment ID, user ID, trace ID, Pod, and every other field as Prometheus labels so dashboards can filter anything.”

## 9. CPU HPA observed the wrong constraint

**Ideal answer**

The `fraud-v12` release changed the accelerator and queue behavior rather than driving CPU saturation. The model used more GPU memory, batching efficiency fell, inference queue latency increased, and Pods restarted after GPU out-of-memory conditions. The configured HPA observed CPU, which stayed near its target, so it had no evidence to request the replica increase that the inference workload needed. Initial readiness also passed because the probe did not exercise sustained production-like batching or GPU memory pressure.

Even a better workload metric would not guarantee new capacity. The GPU node group had reached its configured maximum, and cloud quota blocked additional accelerator capacity. The chain therefore contained at least three limitations: an HPA signal that did not represent queue or accelerator saturation, a readiness check that admitted a revision before its load behavior was known, and infrastructure bounds that prevented capacity expansion. Evidence must connect the model revision, queue, GPU memory/OOM restarts, unschedulable Pods or autoscaler decisions, group maximum, and cloud quota.

> Autoscaling is only as useful as its signal and the capacity available behind it.

**Key distinctions**

- Normal CPU does not mean spare GPU memory, queue capacity, database capacity, or acceptable latency.
- HPA decides replica demand from configured signals; node autoscaling and cloud quota determine whether infrastructure can satisfy that demand.
- Readiness is admission to traffic under its configured check, not a production load test.

**Common weak answer**

“HPA failed because Kubernetes cannot autoscale GPU workloads, so the only fix is manual replicas.”

## 10. Capacity mitigates pressure but not design weakness

**Ideal answer**

More GPU capacity can be an appropriate immediate mitigation: it may reduce queueing and restart pressure and restore the user SLI. It is incomplete as a corrective action because it does not explain or correct why `fraud-v12` consumed excessive model memory, why batching became inefficient, or why queues could grow without a safe bound. It also leaves CPU-based autoscaling blind to the real saturation signal and leaves weak readiness or warm-up behavior able to expose an unproven revision.

A complete improvement set considers model-memory optimization, bounded queues and overload behavior, queue- or GPU-aware scaling, representative load and soak tests, warm-up-aware readiness, canary exposure with user SLO gates, and a safe rollback or model fallback. Capacity engineering must also cover cloud quota management, reserved headroom for failure and rollout, and tested behavior when requested accelerator capacity is unavailable. Model-revision labels and correlations must make a regression visible quickly.

Each failure mechanism needs an owned correction. Capacity can delay recurrence while leaving design weaknesses intact and increase spend without fixing correctness.

**Key distinctions**

- Mitigation reduces current impact; corrective action changes the conditions, detection, or controls that allowed the incident.
- More supply does not bound demand, improve model efficiency, select the right autoscaling signal, or validate a release.
- Headroom and quota are necessary platform responsibilities, but application/model efficiency and degradation behavior remain workload responsibilities.

**Common weak answer**

“Raise the GPU node-group maximum permanently; if latency recovers, the root cause is resolved.”
