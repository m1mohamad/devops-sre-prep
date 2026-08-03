---
title: Platform Interview Rapid Review
tags:
  - interview
  - platform-engineering
  - devops
  - sre
  - leadership
  - rapid-review
aliases:
  - Final Interview Review
  - Platform Interview Answers
  - Ninety-Minute Interview Review
---

# Platform Interview Rapid Review

## How to Use This Page

This page is for final interview rehearsal, not a replacement for the [Core Path](../core-path/index.md) or its deep dives. Say the answers aloud, adapt them to the job, and do not memorize them word-for-word. State assumptions when the question lacks context. Use only honest experience: invented metrics, impact, dates, or responsibilities are prohibited. A smaller truthful result followed by a thoughtful lesson is stronger than an impressive fiction.

Use one response model throughout:

```text
Principle
→ design or action
→ trade-off
→ evidence from experience
→ operational result
```

Weak answers often begin with a product list. Strong answers first name the system responsibility or engineering principle, then explain why a design meets it. Products are implementation evidence, not the argument. For every example, distinguish what the team did from what you personally designed, implemented, decided, or operated.

## Final 90-Minute Review Plan

|      Time | Activity                                  |
| --------: | ----------------------------------------- |
|  0–10 min | Rehearse introduction                     |
| 10–30 min | Review five experience stories            |
| 30–55 min | Practise platform and reliability answers |
| 55–70 min | Practise rapid troubleshooting            |
| 70–80 min | Review leadership and ambiguity           |
| 80–85 min | Select interviewer questions              |
| 85–90 min | Stop studying and prepare calmly          |

## The Answer Structure

Open with one sentence that answers the question. Explain the principle, design or action, most important trade-off, observable evidence, and real result. Ask a clarifying question when scale, regulation, failure tolerance, or ownership would change the answer.

For troubleshooting, lead with impact and evidence rather than commands. For design, establish requirements and failure modes before components. For experience, use “I” only for your own contribution and “we” for collective work. If the result is unknown, say what evidence you inspected or would inspect rather than inventing certainty.

## 30-Second Introduction

I have nearly twenty years in systems and infrastructure, with the last several focused on cloud, DevOps, and platform engineering, including more than six years working at AWS. I have built and operated automated cloud and Kubernetes platforms, using infrastructure as code, CI/CD, GitOps, and observability as connected capabilities rather than isolated tools. My current work also covers Python and Ansible automation, self-hosted CI, containers, virtualisation, and storage. My strengths are complex-system troubleshooting, infrastructure automation, Kubernetes, and cloud architecture, and I am seeking broader platform ownership across developer experience, reliability, security, standards, and operational maturity.

## 90-Second Introduction

My foundation is nearly twenty years in systems and infrastructure, so I approach platforms with an operator's understanding of networking, compute, storage, failure, and recovery. Over the last several years my focus has moved toward cloud, DevOps, and platform engineering, including more than six years working at AWS.

I have hands-on experience building the path from Terraform-managed cloud foundations and EKS through GitLab CI, registries, GitOps with Argo CD or Flux, Helm-based Kubernetes delivery, and Prometheus and Grafana observability. I think of those as one production system: identity, environment boundaries, immutable promotion, rollout, evidence, and recovery all need coherent ownership.

My current work includes Python automation, reusable Ansible, self-hosted CI, Podman services, Proxmox, storage, and private-cloud automation. The recurring theme is turning complex operational work into repeatable, supportable capabilities while retaining enough visibility to diagnose failures.

My strongest areas are troubleshooting across system boundaries, infrastructure automation, Kubernetes platforms, and cloud architecture. I am now looking for broader platform ownership: treating developers as platform users, improving secure self-service and standards, and connecting delivery speed to reliability, security, and operational maturity rather than optimizing one tool in isolation.

## Five Reusable Experience Stories

Prepare facts for these cards before the interview. Each should support several questions without pretending that one story proves everything.

### Story 1 — End-to-End Kubernetes Platform

**Best used for:** Platform design, Kubernetes, CI/CD, GitOps, and ownership.

**Situation:** Describe the real need behind this evidence path: Terraform → AWS networking and IAM → EKS → GitLab CI → registry → Argo CD or Flux → Helm/Kubernetes → Prometheus/Grafana → application teams.

**Risk or scale:** Give actual criticality, constraints, and scale, or `[replace with the real result]`.

**My ownership:** Separate what you designed, implemented, or operated from team work and application ownership.

**Decision:** Explain CI/CD separation, immutable artifact promotion, environment boundaries, identity and secrets, rollback, and the platform contract.

**Trade-off:** Standardisation reduced variation but required maintained templates and justified escape paths.

**Evidence:** Plans, pipeline records, digests, Git revisions, reconciliation, events, and user telemetry.

**Result:** `[replace with the real result]`

**What changed afterward:** Name the real default, runbook, ownership rule, or `[replace with the real result]`.

**Likely follow-up questions:**
- Which parts did you personally own?
- How did deployment authority, rollback, and application ownership work?

### Story 2 — Production Incident

**Best used for:** Incident leadership, diagnosis, communication, and learning.

**Situation:** Pick the incident you can explain most accurately, not the most impressive: CI/Jenkins storage exhaustion; Sentry, Kafka, Redis, or database degradation; Traefik or ingress 502/504 routing; Kubernetes scheduling; certificate renewal; or storage capacity.

**Risk or scale:** State confirmed impact and business risk using known facts.

**My ownership:** Say whether you led, diagnosed, mitigated, communicated, or delivered follow-up work.

**Decision:** Use impact → evidence → hypotheses → mitigation → recovery verification → permanent improvement.

**Trade-off:** Fast mitigation reduces harm but can destroy diagnostic evidence.

**Evidence:** Alerts, events, logs, traces, capacity signals, change history, and the original user SLI.

**Result:** `[replace with the real result]`

**What changed afterward:** Give the real alert, test, runbook, automation, or `[replace with the real result]`.

**Likely follow-up questions:**
- Which hypothesis did evidence reject?
- What was mitigation versus root-cause correction?

### Story 3 — Golden Path and Automation

**Best used for:** Developer experience, automation, standards, and toil.

**Situation:** Choose repeated work addressed by Python, reusable Ansible, self-hosted CI, Podman deployment, or repeatable infrastructure configuration.

**Risk or scale:** Describe real frequency, inconsistency, cognitive load, or risk.

**My ownership:** Explain discovery, contract design, implementation, documentation, and adoption support.

**Decision:** Encode stable knowledge with safe defaults, validation, idempotency, versioning, observable failures, and an escape route.

**Trade-off:** Automation creates maintenance and can fossilize a bad process.

**Evidence:** Repeatable runs, review, tests, support patterns, feedback, and telemetry.

**Result:** `[replace with the real result]`

**What changed afterward:**

> I converted repeated operational knowledge into a supported platform primitive.

**Likely follow-up questions:**
- How did you prove the abstraction was stable and reduced toil?

### Story 4 — Security and Identity

**Best used for:** Least privilege, compliance, secrets, and usability.

**Situation:** Select a real path involving AWS IAM, Kubernetes RBAC, SSO or Okta, workload identity, short-lived credentials, secrets, or auditability.

**Risk or scale:** Explain the trust boundary and consequence of excess access.

**My ownership:** Name the policy, role, integration, secret path, or review you owned.

**Decision:** Prefer federated identity, scoped short-lived credentials, protected secrets, and central audit evidence.

**Trade-off:** Strong controls reduce blast radius, but opaque denials and excessive approvals harm developer usability; give one real compromise.

**Evidence:** Identity-provider, cloud and Kubernetes audit evidence, access reviews, and rotation records.

**Result:** `[replace with the real result]`

**What changed afterward:** Name the real primitive or review improvement, or `[replace with the real result]`.

**Likely follow-up questions:**
- Where was each identity authenticated and authorized?
- What usability cost did the control impose?

### Story 5 — Leadership and Ambiguity

**Best used for:** Influence, prioritisation, disagreement, mentoring, and uncertainty.

**Situation:** Choose unclear requirements, multiple teams, phased design, or a decision without perfect information.

**Risk or scale:** State uncertainty, failure impact, and reversibility.

**My ownership:** Explain how you clarified outcomes, communicated risk, prioritized pragmatically, and mentored or unblocked someone.

**Decision:** Declare assumptions, gather decisive evidence, phase the design, and set a feedback checkpoint.

**Trade-off:** A smaller reversible release learns sooner but may preserve temporary duplication.

**Evidence:** Reviews, operational data, user feedback, or decision records.

**Result:** `[replace with the real result]`

**What changed afterward:** Explain how feedback changed the design, contract, mentoring, or roadmap, or `[replace with the real result]`.

**Likely follow-up questions:**
- How did dissent alter the decision?
- How did you avoid becoming the bottleneck?

Leadership here means improving decisions, clarity, capability, and outcomes; it is not limited to people management.

## Platform Engineering Questions

### What is platform engineering?

**30-second ideal answer**

Platform engineering treats an internal platform as a product and developers as its users. The platform team provides supported, secure self-service capabilities and golden paths that reduce cognitive load for common delivery and operational work. Product thinking means discovering user pain, maintaining contracts, measuring adoption and outcomes, and evolving the platform rather than merely installing tools. The goal is not to hide every infrastructure detail: teams still need useful operational visibility and ownership. Safe defaults should cover frequent needs, while justified escape paths allow exceptional workloads without making uncontrolled variation the normal route.

**Strong answer includes**
- User research, owned capabilities, documentation, support, lifecycle, golden paths, and measurable outcomes.

**Trade-off or assumption**

Standardization creates leverage but can constrain exceptional workloads; the contract and exception process must be explicit.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Platform engineering is Kubernetes, Terraform, and CI/CD managed by a central team.”

### What is a golden path?

**30-second ideal answer**

A golden path is the supported default workflow for a common service type, expressed as a service template or reusable contract. It can provide CI, a secure build, deployment, identity, telemetry, probes, and policy defaults so teams do not repeatedly solve the same risks. It is maintained, documented, supported, and versioned like a product. It is not a mandatory paved prison: a team may deviate when requirements justify the added ownership and risk, using a documented escape path. The path earns adoption by being easier and safer than rebuilding the capability independently.

**Strong answer includes**
- A maintained, versioned default and clear responsibility for upgrades and support.

**Trade-off or assumption**

The path optimizes a frequent service shape; it should not pretend every workload has identical constraints.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“It is the one approved stack every team must use.”

### How do you decide what belongs on a golden path?

**30-second ideal answer**

I look for a repeated, high-frequency user need with meaningful operational risk or cognitive load. Before encoding it, the platform needs clear ownership, a maintainable contract, and an abstraction stable enough that users will not constantly bypass it. I validate demand through support patterns, workflow observation, and adoption evidence, release a small version, and keep an explicit escape hatch. I avoid automating rare or poorly understood workflows too early because automation can freeze the wrong process and create long-term maintenance without leverage. The decision is based on expected reuse and reduced risk, not technical novelty.

**Strong answer includes**
- Frequency, risk, stability, ownership, maintainability, adoption evidence, and an exception route.

**Trade-off or assumption**

Waiting improves understanding, but waiting too long leaves repeated manual risk; use the smallest useful contract.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“We standardize whatever technology the platform team prefers.”

### How do you measure platform success?

**30-second ideal answer**

I combine user, flow, reliability, and risk measures. I would track adoption and developer satisfaction; time to create a service; deployment lead time, change failure rate, and recovery time; support requests and repeated manual steps; platform and workload reliability; and security-policy compliance. I establish a baseline and segment results so forced adoption cannot masquerade as satisfaction. Measures should connect platform capabilities to outcomes and prompt product decisions. Cluster count or pipeline count are vanity metrics: they show inventory or activity, not that developers deliver safely, quickly, or reliably.

**Strong answer includes**
- Balanced quantitative and qualitative measures, baseline, trends, and decision use.

**Trade-off or assumption**

Attribution is imperfect because team and application changes also affect outcomes; triangulate rather than claim false causality.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Success is the number of clusters, pipelines, or services onboarded.”

### How do you prioritize platform roadmap work?

**30-second ideal answer**

I prioritize by combining user pain, operational risk, security or compliance deadlines, reliability and toil, expected adoption, and leverage across teams. I make sequencing dependencies visible—for example, identity may be required before safe self-service—and document explicit trade-offs between urgent risk and longer-term enablement. I communicate why work moved, what is deferred, and what evidence would change the order. Rather than funding a large platform rewrite on assumptions, I prefer small validated releases with clear owners and outcome measures, then expand capabilities that users adopt and that reduce material risk or effort.

**Strong answer includes**
- User and operational evidence, mandatory deadlines, leverage, dependencies, ownership, and communication.

**Trade-off or assumption**

Urgent reliability work can delay features, while perpetual firefighting can prevent structural improvement; reserve capacity deliberately.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“The loudest stakeholder or newest technology determines the roadmap.”

## Reliability and Operations Questions

### How do you define an SLO?

**30-second ideal answer**

I start with a user-visible capability, then define an SLI, objective, and measurement window. For a payment API, an SLI might be the proportion of valid payment attempts completed correctly under a latency threshold, with exclusions explicitly defined; the SLO might require a chosen percentage over 28 days. The allowed failure becomes an error budget that informs release and reliability decisions, while multi-window burn-rate alerts detect fast and slow budget consumption. CPU, Pod health, and database latency are valuable diagnostic signals, but they are not automatically SLOs because they do not directly state whether the user capability succeeded.

**Strong answer includes**
- User journey, precise good/valid events, target, window, error budget, and actionable burn-rate alerts.

**Trade-off or assumption**

The threshold reflects business expectations and cost; 100% is normally unrealistic and discourages honest risk decisions.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Our SLO is CPU below 80% and every Pod Running.”

### How do you lead a production incident?

**30-second ideal answer**

I confirm impact, establish severity, name an incident lead and technical owners, preserve relevant evidence, and create competing hypotheses. We choose the safest mitigation that reduces user harm, then verify recovery against the original user SLI rather than a single green component. Communication has a clear cadence and distinguishes facts, hypotheses, actions, and next update. After stabilization, root-cause analysis and a blameless postmortem produce prioritized improvements with owners. Mitigation restores service—such as rollback or shedding load—whereas root-cause correction changes the condition that allowed the incident; they are related but not the same.

**Strong answer includes**
- Confirm impact → severity → ownership → evidence → hypotheses → mitigation → SLI verification → communication.

**Trade-off or assumption**

Preserving evidence matters, but preventing ongoing harm takes priority when impact is severe.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“I restarted everything, watched the dashboard turn green, and later found the root cause.”

### Argo CD says Healthy, but users report errors. What now?

**30-second ideal answer**

Argo CD Healthy shows reconciliation and resource-level health heuristics; it does not prove business correctness. I would confirm the user SLI and affected scope, correlate errors with rollout timing and the deployed digest or Git revision, and inspect application errors, traces, dependencies, and business signals. I would compare old and new revisions and check whether readiness is too shallow. If evidence implicates the rollout, I would pause exposure or revert the GitOps change, then verify recovery through the original user SLI. GitOps status is deployment evidence, one input to diagnosis rather than the production verdict.

**Strong answer includes**
- User evidence, revision correlation, application telemetry, dependency health, and rollout timing.

**Trade-off or assumption**

A rapid revert reduces impact but may be unsafe after an incompatible state or schema change.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Healthy means Kubernetes is fine, so the report cannot be a deployment problem.”

### How do you design rollback?

**30-second ideal answer**

I design rollback before release. CI builds one immutable artifact digest; GitOps records the digest and previous known-good configuration, so a reviewed Git revert can reconcile the earlier version. Progressive rollout and feature flags can limit exposure, and recovery is verified through user SLIs. The application and migration design must maintain schema and data compatibility because rollback is not always safe once state changes. For expand-and-contract migrations, old and new code can coexist. If a destructive or irreversible change has occurred, a tested roll-forward may be safer than restoring old code against incompatible state.

**Strong answer includes**
- Immutable identity, known-good configuration, GitOps revert, compatibility, flags, and user verification.

**Trade-off or assumption**

Compatibility periods cost engineering effort and temporary complexity but buy recovery options.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Run `kubectl rollout undo` and assume the previous image restores the system.”

## Data, Security, and Cost Questions

### How do you operate PostgreSQL reliably?

**30-second ideal answer**

I start with business RPO and RTO, automated backups, and regularly tested restoration—not merely successful backup jobs. I monitor query latency and plans, indexes, locks, transaction age, storage growth, replication lag, and failover readiness. Connection pooling and deliberately sized `max_connections` protect finite database resources. Schema migrations use backward-compatible phases and bounded locks. Access is least privilege and auditable. During an incident I preserve evidence, distinguish database saturation from application pool or query behavior, and verify recovery with both database signals and the user SLI. A managed service can reduce operational work, but “use RDS” is not a reliability design.

**Strong answer includes**
- Restore tests, objectives, pools, queries, transactions, locks, storage, replication, migrations, and access.

**Trade-off or assumption**

Higher availability and lower RPO cost more and add operational complexity; requirements determine the design.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Use RDS with backups and a large instance.”

### How do you operate Redis reliably?

**30-second ideal answer**

First I determine whether losing Redis is a performance problem or a correctness problem. For a cache, durable truth stays elsewhere and cache loss has a documented fallback. I bound memory with intentional limits, eviction policy, TTLs, and controls for hot keys or unbounded key growth. I monitor memory, evictions, hit ratio, latency, and replication; provide replication and failover where required; and enable persistence only when the state contract requires it. If Redis holds correctness-critical state, I design and test it as a data system rather than casually calling it a cache.

**Strong answer includes**
- Explicit cache versus durable-state contract, bounded growth, failure behavior, and monitoring.

**Trade-off or assumption**

Persistence and replicas improve recovery but add latency, cost, and operational behavior that must be tested.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Redis is in memory, so add replicas and more RAM.”

### How do you approach platform cost?

**30-second ideal answer**

I begin with allocation and visibility by environment, service, owner, and major cost driver. Then I examine accurate Kubernetes requests, bin-packing, autoscaling, idle non-production capacity, storage lifecycle, data transfer, build efficiency, instance families, and managed-service sizing. I change one bounded area and evaluate savings against SLOs, resilience, and developer productivity. Commitments or architectural changes follow stable demand evidence. Blindly reducing resources is not cost engineering: it can convert cloud spend into incidents, queues, slow builds, or engineering toil. The objective is efficient delivery of required outcomes, not the smallest infrastructure bill in isolation.

**Strong answer includes**
- Ownership and allocation, workload efficiency, lifecycle and transfer costs, then measured optimization.

**Trade-off or assumption**

Reserved headroom looks idle but may be required for failure, rollout, or demand; quantify its purpose.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Lower every request and buy the cheapest instance.”

### How do you implement compliance without blocking delivery?

**30-second ideal answer**

I translate ISO27001-style control intent into repeatable technical and procedural evidence rather than claiming that a tool creates compliance. Protected changes, least privilege, centralized audit logs, access reviews, secret rotation, vulnerability scanning, artifact provenance, backup restore tests, and incident/change procedures become platform defaults. Policy as code gives early pull-request feedback and creates consistent records. Where a control cannot fit, an exception has an owner, rationale, compensating control, approval, and expiry. This makes the normal delivery path continuously produce evidence while retaining accountable handling for genuine exceptions.

**Strong answer includes**
- Control intent, automated evidence, human procedures, named ownership, and expiring exceptions.

**Trade-off or assumption**

Not every control can be fully automated; automate stable checks while preserving accountable review for context.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Install scanners and policy tools, and the platform is ISO27001 compliant.”

### How do you balance security with developer experience?

**30-second ideal answer**

I make the secure path the easiest path through pre-approved platform primitives, short-lived workload and human identity, and self-service workflows. Policies should return useful failure messages and appear in pull requests, where fixes are cheap, rather than surprise teams at production deployment. The platform absorbs repeated low-level security mechanics while preserving visibility into the contract. Exceptional needs use documented, owned, time-bound escape paths. This improves both security and adoption: developers do not need to become specialists in every IAM or supply-chain detail, but they retain responsibility for application-specific threats and data decisions.

**Strong answer includes**
- Secure defaults, federated identity, self-service, early actionable feedback, and governed exceptions.

**Trade-off or assumption**

More abstraction reduces cognitive load but can obscure denial causes; expose identity, policy, and remediation evidence.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Security sets the rules; developers must work around them.”

## Rapid Technical Troubleshooting

### A Pod is Pending

**30-second ideal answer**

“Pending” is a symptom, not a root cause. I first read Pod and scheduler events, then follow the placement chain: resource requests; node selectors and affinity; taints and tolerations; volume binding; namespace quota; node autoscaler decisions; node-group limits; and cloud capacity or quota. I compare the Pod specification with available node capacity and constraints rather than immediately adding nodes. If capacity is the cause, I verify that the autoscaler can provision the required node type and that quotas allow it; if not, I mitigate safely and correct the request, constraint, storage, or capacity boundary.

**Strong answer includes**
- `describe`/events first, followed by resources, placement, storage, quota, autoscaler, group, and cloud evidence.

**Trade-off or assumption**

Relaxing placement may restore scheduling but violate isolation or availability requirements.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Restart the Pod or scale the node group.”

### Users see 502 responses although readiness is green

**30-second ideal answer**

Readiness proves only the configured probe, not the complete request path. I trace evidence hop by hop: load balancer or gateway, route, Service, EndpointSlice and readiness membership, target port, Pod listening address and port, protocol or TLS, then application logs and traces. I check whether errors affect all targets or one revision and whether they correlate with a rollout. A green probe can hit a different path, port, protocol, or shallow local check. I mitigate by removing the bad revision or route only when evidence identifies it, then verify using the original external request signal.

**Strong answer includes**
- End-to-end routing inspection and revision-aware application evidence.

**Trade-off or assumption**

A deep dependency probe may remove all endpoints during a shared outage; probe design must avoid amplifying failure.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Readiness is green, so restart the ingress controller.”

### Terraform plans to replace a critical resource

**30-second ideal answer**

I do not blindly apply. I determine exactly why replacement is planned by inspecting the provider diff and any force-new field, the state binding, refreshed remote attributes and drift, configuration history, and provider-version changes. I estimate dependencies and blast radius, confirm backup and recovery requirements, and reproduce or test the migration in a safer environment. Depending on evidence, the correct path may be an import, a reviewed state move, restoring the intended configuration, or a phased parallel migration. State operations change Terraform's mapping, not the real resource, so each step needs a backup, peer review, and post-change validation.

**Strong answer includes**
- Diff reason, state, drift, provider changes, blast radius, testing, and recovery.

**Trade-off or assumption**

Preserving a critical resource may retain drift temporarily; document and converge deliberately rather than hiding it.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Terraform knows best, so approve the plan.”

### Design a secure CI/CD flow

**30-second ideal answer**

My default path is pull request → tests → lint → dependency and security checks → build once → image scan → SBOM → provenance → signing → immutable digest. CI uses short-lived, scoped identity to publish the artifact and propose a reviewed GitOps update; it does not hold unrestricted production-cluster credentials. CD promotes the same digest through progressive rollout, evaluates an SLO gate, and reverts to a known-good digest when safe. Protected reviews, policy evidence, environment boundaries, and audit logs establish who authorized what. Building once keeps test and supply-chain evidence attached to the exact production bytes.

**Strong answer includes**
- Isolated build evidence, immutable promotion, narrow identities, reviewed GitOps, progressive rollout, and rollback.

**Trade-off or assumption**

More gates improve assurance but can slow feedback; run cheap checks early and reserve approvals for meaningful risk.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Give the CI runner cluster-admin so it can deploy after building each environment.”

### How do you upgrade Kubernetes safely?

**30-second ideal answer**

I inventory deprecated APIs and version skew, verify controller, CNI, CSI, ingress, observability, and other add-on compatibility, then rehearse in non-production with representative workloads. I establish capacity headroom and a recovery path before upgrading the control plane in supported steps. Node pools are replaced progressively; drain behavior, PodDisruptionBudgets, topology, local storage, and termination handling are tested rather than assumed. At each phase I validate cluster functions, workload behavior, and user SLOs. I pause when evidence degrades. An available control plane alone does not prove workloads or critical add-ons survived the change.

**Strong answer includes**
- API/add-on compatibility, rehearsal, control plane, replaceable nodes, disruption, topology, headroom, and validation.

**Trade-off or assumption**

Parallel node pools cost temporary capacity but make progressive migration and reversal safer.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Upgrade the control plane, then run the managed node upgrade.”

### CPU is normal, but latency is rising

**30-second ideal answer**

CPU may be the wrong saturation signal. I first confirm the affected user SLI and use traces to locate where request time accumulates. Then I inspect queueing, memory and garbage collection, database waits and locks, network and downstream latency, thread and connection pools, disk, GPU, and rate limits. I correlate the onset with demand, configuration, dependency behavior, and application or model revision. Scaling blindly can add load to the true bottleneck or leave it unchanged. I form competing hypotheses, use evidence to discriminate them, mitigate the constrained boundary, and verify recovery at the user level.

**Strong answer includes**
- Trace-based localization, non-CPU saturation signals, change and demand correlation, and SLI verification.

**Trade-off or assumption**

Temporary load shedding may protect recovery but reduces accepted work; align it with business priorities.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Add Pods because latency always means insufficient compute.”

## Leadership and Ambiguity Questions

### Tell me about a decision you made with incomplete information

**30-second ideal answer**

I make the uncertainty visible: desired outcome, evidence available, assumptions, and consequences if an assumption is wrong. I distinguish reversible decisions from hard-to-reverse ones; for a reversible choice I time-box analysis and use a small phased rollout, while an irreversible choice earns deeper review. I contain risk with limited scope, monitoring, a stop condition, and a recovery path. Then I create a feedback checkpoint and record how new evidence revised the decision. In the interview I would attach this structure to Story 5 and be precise about my decision, dissent, result, and lesson.

**Strong answer includes**
- Assumptions, evidence, reversibility, risk containment, staged action, feedback, and revision.

**Trade-off or assumption**

More analysis reduces some uncertainty but delays learning and value; match rigor to reversibility and blast radius.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“I trusted my intuition and it worked.”

### How do you handle disagreement with application teams?

**30-second ideal answer**

I first understand the underlying application need and distinguish preference from material reliability, security, cost, or ownership risk. We make evidence and constraints explicit, clarify which team owns each operational consequence, and agree a service contract rather than arguing about product loyalty. I prefer a supported default with a justified escape path whose additional responsibilities are documented. I record the decision, unresolved risks, and review trigger. If later production or user evidence changes the premise, I revisit it openly; consistency matters, but defending an outdated decision does not.

**Strong answer includes**
- Listening, evidence, risk, ownership, contract, exception, decision record, and review.

**Trade-off or assumption**

An escape path supports genuine needs but increases variation and support cost; make that cost owned and visible.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“The platform standard wins because central consistency is always more important.”

### How do you mentor engineers?

**30-second ideal answer**

I teach the decision process, not only the command that fixed today's issue. During diagnosis I pair, ask the engineer to form hypotheses and choose discriminating evidence, then explain the relevant system model. I delegate meaningful ownership with a clear outcome and safety boundary, review designs and decisions, and give timely, specific feedback. Repeated lessons become documentation, tests, or automation that help the wider team. The goal is increasing independent judgment and confidence; if every difficult issue still requires me, I have made myself a permanent bottleneck rather than building capability.

**Strong answer includes**
- Pairing, hypotheses, context, meaningful delegation, design review, specific feedback, and reusable learning.

**Trade-off or assumption**

Pairing can take longer during one incident, so match coaching to severity and debrief after urgent mitigation.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“I mentor by answering questions and reviewing every important change myself.”

### How do you reduce operational toil?

**30-second ideal answer**

I use a deliberate loop: measure repeated work → classify its source → remove unnecessary work → automate stable work → improve observability → assign ownership → verify reduction. Classification matters because recurring work may come from a defective system, unclear contract, missing product capability, or a legitimate repeatable procedure. I eliminate or simplify before automating. Automation then needs idempotency, safe failure, tests, telemetry, documentation, and an owner. I compare frequency, time, errors, or support demand afterward. Automating a broken process can preserve the wrong process more efficiently, so “we scripted it” is not sufficient evidence.

**Strong answer includes**
- Baseline, root classification, elimination before automation, product-quality automation, ownership, and verification.

**Trade-off or assumption**

Low-frequency automation may cost more to maintain than it saves; prioritize repeated high-risk or high-volume work.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“I automate every manual task.”

### What would you do in your first 90 days?

**30-second ideal answer**

My sequence is listen and map → understand users and ownership → inspect reliability and delivery evidence → identify high-leverage pain → agree priorities → ship one small useful improvement → establish roadmap and measures. I would meet platform and application teams, follow a change and an incident end to end, examine SLOs, support demand, security obligations, cost, and decision boundaries, and test assumptions with users. The first delivery should solve a visible, bounded problem and teach us how the organization works. Then I would agree an evidence-based roadmap. I would not promise an immediate platform rewrite before understanding constraints and trust.

**Strong answer includes**
- Users, system and ownership map, operational evidence, one bounded delivery, relationships, measures, and roadmap.

**Trade-off or assumption**

An urgent risk may require earlier intervention; explain why while continuing discovery.

**Experience prompt**

Use one truthful experience and name the evidence.


**Common weak answer**

“Replace the existing platform with my preferred stack in the first quarter.”

## Questions to Ask the Interviewer

Choose two or three that fit the conversation; do not ask all six mechanically.

1. What are the largest platform constraints today: reliability, delivery speed, security, cost, or developer experience?
2. Which workflows are standardized, and where are teams still building their own infrastructure or delivery patterns?
3. How are production ownership, on-call, and SLOs divided between platform and application teams?
4. What would a successful first six months look like?
5. Which platform decisions are already settled, and which are still open?
6. How does the team measure whether platform work improves developer outcomes?

Listen and ask one relevant follow-up. Understand the real problem, decision scope, and success criteria.

## Final Interview Checklist

- [ ] CV open.
- [ ] Job description open.
- [ ] Five story headings visible.
- [ ] Three interviewer questions selected.
- [ ] Camera and audio checked.
- [ ] Water ready.
- [ ] Stop learning new material.
- [ ] Slow down answers.
- [ ] Ask clarifying questions.
- [ ] State assumptions.
- [ ] Use real evidence.
- [ ] Do not bluff.
- [ ] Pause before answering.

## Related Deep Dives

- [Core Path — End-to-End Platform](../core-path/index.md) and its separate [ideal recall answers](../core-path/recall-answers.md)
- [Platform Engineering](../platform-engineering/index.md)
- [CI/CD and GitOps](../cicd/index.md)
- [Kubernetes](../kubernetes/index.md)
- [Observability and SRE](../observability/index.md)
- [Databases](../databases/index.md)
- [Leadership](../leadership/index.md)
- [Behavioural and Production Stories](09-behavioural-and-production-stories.md)
