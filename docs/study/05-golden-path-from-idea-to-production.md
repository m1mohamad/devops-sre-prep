---
title: "Golden Path: From Idea to Production"
tags: [platform-engineering, golden-path, developer-experience, interview]
aliases: [Golden Path from Idea to Production]
---

# Golden Path: From Idea to Production

> Reusable Helm charts and Terraform modules are building blocks.
>
> A Golden Path is the supported route that assembles those building blocks into a production-ready service.

Think of a highway: the cloud, cluster, modules, charts, and workflows are roads and infrastructure; the Golden Path is the signed, maintained route to a common destination. It gives a driver useful defaults, known junctions, support, and safe exits without claiming that every journey must use the same vehicle.

Without that route, a developer faces a decision tree:

```text
Developer wants a new API
        |
        +--> Which language/runtime?
        +--> Which Dockerfile?
        +--> Which Terraform module?
        +--> Which Kubernetes chart?
        +--> How do I get DNS?
        +--> How do I get TLS?
        +--> How do I configure CI?
        +--> Where do secrets go?
        +--> How do I add monitoring?
        +--> What labels are mandatory?
        +--> How do I deploy?
        +--> Who creates the AWS resources?
```

The organization may already publish `terraform-vpc-module`, `terraform-rds-module`, `helm-service-chart`, `github-actions-library`, and `prometheus-rules`. These are valuable reusable primitives, but the developer still has to select, connect, secure, and operate them correctly. The organization has supplied IKEA components; engineers still have to work out how to assemble the furniture.

The supported route changes the experience:

```text
              PLATFORM PORTAL

            "Create Backend API"
                    |
                    v
        Name: payments-api
        Owner: payments-team
        Runtime: Python
        Database: PostgreSQL? Yes
        Public API? Yes
        Environment: dev/stage/prod
                    |
               [ CREATE ]
                    |
    +---------------+----------------+
    |               |                |
    v               v                v
 Git repo       Infrastructure    Catalog
    |               |                |
    v               v                v
 CI/CD          Terraform          Owner
 Docker         RDS/EKS            Docs
 Tests          IAM                SLO
 Scan           DNS                Links
    |               |
    +-------+-------+
            |
            v
          ArgoCD
            |
            v
           EKS
            |
            v
      Service is running
            |
      +-----+------+------+
      |            |      |
      v            v      v
   Metrics       Logs   Alerts
```

**That complete supported journey is the Golden Path.** The design objective is:

```text
easy path
    =
secure path
    =
observable path
    =
supported path
    =
production-ready path
```

This is a direction, not a claim of instant perfection: Platform Engineering tries to make the organizationally preferred behavior the easiest behavior.

## The illustrative company

This case study follows **Atlas Commerce**, a fictional, medium-sized organization. It deliberately reuses the Atlas setting from the [Production Platform Interview Scenario](04-production-platform-scenario.md), but focuses on developer experience and lifecycle rather than repeating that page's Kubernetes runtime walkthrough.

| Dimension | Illustrative profile |
|---|---|
| Engineering | about 100 engineers; a Platform team of about 4 |
| Estate | 25–40 services; about 100,000 registered users |
| Traffic | roughly 20–200 requests/second, with occasional bursts |
| Foundation | AWS, EKS, GitHub, Terraform, Helm |
| Delivery | GitHub Actions, ECR, GitOps, ArgoCD |
| Operations | Prometheus, Grafana, Loki, and OpenTelemetry where useful |
| Front door | Backstage |

These figures are illustrative, not statistics attributed to Spotify, Backstage, or any real company. **Golden Paths primarily address organizational and developer complexity, not request volume.** Thirty inconsistent services and 50–100 engineers create meaningful ownership, security, upgrade, and operational coordination costs even without millions of requests per second.

This page explains one journey through the capabilities in [The Complete Platform in One Diagram](core-path/index.md#the-complete-platform-in-one-diagram). Use that diagram to answer “what capabilities exist?”, this page to answer “how does a developer use them?”, the [mental models](04-platform-devops-sre-mental-models.md) to reason about boundaries, and the [Atlas scenario](04-production-platform-scenario.md) for deeper runtime behavior.

## The problem before the Golden Path

Atlas accumulated valid local choices but no ordinary-service contract:

```text
payments-api
├── Terraform copied from another repository
├── custom Helm chart
├── GitHub Actions
└── Prometheus annotations

orders-api
├── shared Terraform modules
├── different Helm chart
├── Jenkins
└── manually created Grafana dashboard

accounts-api
├── raw Kubernetes YAML
├── old copied pipeline
└── no consistent resource limits

catalog-api
├── shared chart pinned to an old version
├── manually created IAM role
└── undocumented alerts
```

Each service can run, yet every upgrade and incident requires archaeology. The Platform team's first product decision is narrow: **for an ordinary HTTP backend service, there should be one supported way.** It starts with that frequent workflow rather than attempting to standardize every workload.

## Step 1 — Build reusable platform primitives

Atlas first makes repeated implementation safe and reusable:

```text
platform/
├── terraform-modules/
│   ├── eks-service-iam/
│   ├── rds-postgres/
│   ├── redis/
│   ├── s3-bucket/
│   └── route53-record/
│
├── helm-charts/
│   └── service/
│
├── github-actions/
│   ├── build-container.yml
│   ├── test.yml
│   ├── security-scan.yml
│   └── promote.yml
│
└── policies/
    ├── kubernetes/
    └── terraform/
```

These are **platform primitives**, not a Golden Path by themselves. This is the familiar starting point for teams that already maintain Terraform modules, reusable Helm charts, Jenkins libraries, GitHub Actions workflows, or shared functions.

## Step 2 — Define the standardized service contract

The Platform and application teams agree what “ordinary backend service” means:

```text
Application
    ↓
Container
    ↓
Deployment
    ↓
Service
    ↓
Ingress / Load Balancer (when externally reachable)
```

The contract supplies appropriate defaults for resource requests/limits, startup/readiness/liveness probes, disruption protection and topology spread, ServiceAccount and workload identity, labels, metrics scraping, structured logging, ownership, runbook, and SLO metadata. A public service may receive ingress and DNS; an internal worker should not.

Developers should understand these mechanisms, but they should not manually recreate organizational boilerplate for every service. The Platform team converts standards into defaults and guardrails, while preserving visible controls for application-specific capacity and health semantics.

## Step 3 — Helm encodes the Kubernetes contract

The Platform-owned `platform-charts/service` chart accepts a small application-owned values file:

```yaml
service:
  name: orders-api

image:
  repository: company/orders-api
  tag: "1.4.7"

resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    memory: 512Mi

health:
  readiness:
    path: /ready
  liveness:
    path: /health
```

Depending on declared intent, the chart may render a Deployment, Service, ServiceAccount, PodDisruptionBudget, Ingress, NetworkPolicy, or PodMonitor. Not every service needs every object. It also applies standard labels:

```yaml
company.io/team: orders
company.io/service: orders-api
company.io/environment: production
```

Consistent labels support ownership, cost attribution, discovery, policy selection, monitoring, and incident response. Helm is still a packaging primitive: the chart does not create the repository, provision RDS, build an image, register ownership, or operate the full lifecycle.

## Step 4 — Terraform encodes infrastructure standards

`orders-api` needs PostgreSQL. The application team should not reproduce RDS resource configuration, subnet groups, security groups, KMS integration, backups, monitoring, tags, parameter defaults, and relevant DNS/integration wiring in every repository. It expresses intent:

```hcl
module "database" {
  source = "git::ssh://platform/terraform-rds"

  service               = "orders-api"
  engine_version        = "16"
  size                  = "small"
  backup_retention_days = 7
  owner                 = "orders-team"
}
```

The versioned module can encode private-subnet placement, encryption, least-privilege security groups, backup policy, monitoring, tags, KMS, and reviewed parameter defaults. It should expose additional controls when teams genuinely need them rather than hiding every infrastructure detail forever.

> **Platform team owns repeated infrastructure complexity. Application team expresses application intent.**

Terraform manages infrastructure desired state; providers drive AWS API changes. Separately, Kubernetes controllers reconcile workload desired state. This follows the [desired state → actual state → reconcile](04-platform-devops-sre-mental-models.md#reconciliation-is-everywhere) and [identity → permission → resource](04-platform-devops-sre-mental-models.md#security-mental-model) models.

### The primitives are still not the journey

Atlas now has Terraform modules, Helm charts, CI libraries, and policies—but developers can still ask which module, chart, repository, workflow, naming convention, documentation, and ownership metadata to use. Standardized parts become a Golden Path only when Atlas composes them into an owned, documented route. Orchestration and self-service are next.

## Step 5 — Backstage is one possible front door

Atlas uses Backstage as a concrete interface; Backstage is **not required** for Platform Engineering or a Golden Path. A CLI, API, GitHub repository template, a form backed by automation, or even a well-designed pull-request workflow can expose the same supported route.

```text
Backstage
    ↓
Create
    ↓
Backend Service
```

```text
Create Backend Service

Service Name:  [ orders-api ]
Owner:         [ Team Orders ]
Language:      [ Python ▼ ]
Database:      [ PostgreSQL ▼ ]
External API:  [ Yes ]
Environments:  [x] dev  [x] staging  [x] production
SLO:           [ 99.9% ]

[ CREATE SERVICE ]
```

[Backstage Software Templates](https://backstage.io/docs/features/software-templates/) can collect parameters, render skeleton files, execute Scaffolder actions, publish repositories, register catalog components, and invoke organizational automation. Spotify's public [Software Templates guidance](https://backstage.spotify.com/learn/onboarding-software-to-backstage/setting-up-software-templates/11-spotify-templates/) describes templates as a way to encode Golden Path setup. Atlas is an illustrative architecture, not a claim about Spotify's implementation.

**A Software Template is an automation/scaffolding mechanism; the Golden Path is the supported end-to-end experience.** Backstage is a useful front door here, not the platform itself.

## What happens after CREATE?

```text
                 DEVELOPER

        Create "orders-api"
                 |
                 v
             Backstage
                 |
        +--------+---------+
        |                  |
        v                  v
 Application Repo    Infrastructure Repo
        |                  |
        v                  v
    Python API          Terraform
    Dockerfile          RDS module
    unit tests          IAM
    catalog-info        secret references
        |                  |
        +---------+--------+
                  |
                  v
                GitHub
                  |
                  v
             GitHub Actions
                  |
         +--------+-------+
         |        |       |
        test    build    scan
                  |
                  v
                 ECR
                  |
                  v
          GitOps repo update
                  |
                  v
                ArgoCD
                  |
                  v
                 EKS
                  |
        +---------+---------+
        |         |         |
       Pods    Service   Ingress
        |
        v
 Prometheus / Logs / Traces
```

1. Backstage validates the requested name, owner, workload shape, dependencies, environments, and SLO intent.
2. Scaffolder actions create an application repository and an infrastructure declaration or pull request; they register `catalog-info.yaml` rather than pretending that a catalog deploys software.
3. Human review remains at policy-sensitive boundaries. Terraform provisions approved AWS resources such as RDS, an IAM role, and DNS when requested.
4. GitHub Actions tests the source, scans it, builds the container, and publishes an immutable artifact to ECR.
5. CI or a promotion workflow proposes the image digest in the GitOps repository. The repository records desired deployment state and approval history.
6. ArgoCD observes Git and reconciles the declared Kubernetes resources into EKS. **ArgoCD does not build or publish the application image.**
7. Kubernetes controllers converge Deployments, ReplicaSets, Pods, Services, and—where declared—Ingress. Readiness controls whether ready Pod endpoints receive traffic.
8. Platform integrations expose metrics, logs, traces where appropriate, dashboards/alerts, ownership, SLO, and runbook links. “Accepted” at one step never proves the next step is ready.

## What gets generated?

```text
orders-api/
├── src/
│   └── app.py
├── tests/
│   └── test_health.py
├── Dockerfile
├── pyproject.toml
├── .github/
│   └── workflows/
│       └── pipeline.yml
├── deploy/
│   └── values.yaml
├── catalog-info.yaml
├── docs/
│   ├── README.md
│   └── runbook.md
└── README.md
```

The developer receives a working skeleton, health endpoints, container build, test structure, CI integration, Helm values, ownership metadata, documentation, and runbook skeleton. The path makes questions such as “should it have health checks, an owner, image scanning, a runbook, and production resource declarations?” defaults rather than repeated tickets. The developer still owns meaningful health behavior, tests, sizing, business code, and keeping generated material useful.

## CI is part of the Golden Path

The generated repository consumes a versioned reusable workflow:

```yaml
jobs:
  build:
    uses: company/platform-actions/.github/workflows/container.yml@v4
    with:
      app-name: orders-api
      dockerfile: Dockerfile
```

The supported baseline can progressively provide:

```text
checkout
 ↓
unit tests
 ↓
lint
 ↓
SAST
 ↓
container build
 ↓
image scan
 ↓
SBOM
 ↓
push ECR
 ↓
sign image
```

Not every organization implements every stage on day one. The value is an owned delivery contract that Platform and Security can improve centrally. When version/update policy permits, improving `container.yml@v4` improves many consumers; pinned major versions still require a deliberate migration strategy.

## GitOps and the ArgoCD handoff

The environment repository separates build from deployment intent:

```text
environments/
├── dev/
│   └── orders-api.yaml
├── staging/
│   └── orders-api.yaml
└── production/
    └── orders-api.yaml
```

CI publishes `orders-api@sha256:abc123`; approved desired state references that immutable artifact:

```yaml
image:
  digest: sha256:abc123
```

```text
source
  → CI build/test/scan
  → immutable artifact in ECR
  → desired deployment state in Git
  → ArgoCD reconciliation
  → Kubernetes runtime

Git desired state
        ↓
ArgoCD
        ↓
cluster actual state
```

CI builds, tests, scans, and publishes artifacts. ArgoCD reconciles desired Kubernetes deployment state; it does not build images. Promotion can be a reviewed PR, automation with environment controls, or another explicit policy—the important properties are immutable identity, traceability, and clear ownership.

## Observability is part of production readiness

A weak path ends at `Pod Running`. A production-ready Golden Path considers the operating chain:

```text
Service deployed
       ↓
metrics available
       ↓
logs searchable
       ↓
traces available where appropriate
       ↓
dashboard available
       ↓
alerts configured
       ↓
owner recorded
       ↓
runbook linked
       ↓
SLO registered
```

Not every service needs automatic custom dashboards, traces, or identical alerts. These are capabilities and progressively standardized defaults. A deployed Service does not automatically become observable or production-ready: operators must be able to connect [metrics → logs → traces](04-platform-devops-sre-mental-models.md#observability-mental-model), identify an owner, judge user impact, and act.

## The Software Catalog is the discovery surface

```text
orders-api

Owner         Orders Team
Lifecycle     Production
System        Commerce
Repository    github/company/orders-api
Deployment    EKS / production
ArgoCD         Healthy / Synced
SLO            99.9%
Dashboard      Grafana
Logs           Loki
Runbook        orders-api/runbook
Dependencies   postgres-orders, redis-orders, payments-api
```

The Software Catalog answers: What is this service? Who owns it? Where is its code and deployment? Is delivery healthy? Where are its logs, dashboard, and runbook? What does it depend on? The catalog is an inventory and integration surface; it links to or queries GitHub, ArgoCD, Grafana, Loki, and SLO systems rather than necessarily storing or implementing them.

## Golden Technologies, Path, Template, Catalog, and State

These labels are useful distinctions, not a claim that every company uses identical terminology:

| Term | Meaning in this case study |
|---|---|
| Golden Technologies | Technologies Atlas chooses to support, such as EKS, Terraform, Helm, and GitHub Actions |
| Golden Path | The recommended and supported way to combine capabilities for a workload type |
| Software Template | A scaffolding/orchestration mechanism that helps instantiate the path |
| Software Catalog | Inventory, ownership, and discovery with links/integrations to operational systems |
| Golden State | Evidence that deployed software continues to meet current organizational standards |

## Escape hatches: a path, not a prison

```text
                 GOLDEN PATH
                     |
         +-----------+-----------+
         |                       |
  common cases (~90%*)       unusual cases
         |                       |
     standard path             escape hatch
         |                       |
     automated              engineering review

* Illustrative model, not a measured universal statistic.
```

HTTP APIs, PostgreSQL, Redis, and background workers may fit a small set of paths. GPU inference, Kafka Streams, extreme-low-latency systems, special networking, specialized stateful systems, or unusual compliance may require deviation.

> A Golden Path is the easiest supported path, not necessarily the only permitted path.

```text
BAD:
"Every team must use exactly this architecture."

GOOD:
"This is the supported production path.
If your workload fits it, everything is easy.
If it does not, there is an explicit exception path."
```

The exception should record why the standard is insufficient, reviewers and risk owners, compensating controls, support expectations, and whether the exception expires or becomes a supported capability. Overly rigid platforms encourage teams to bypass the platform entirely.

## From shared libraries to an internal developer platform

### Level 1 — Reusable components

```text
Terraform modules
Helm charts
pipeline functions
shared libraries
```

Teams reuse implementation pieces.

### Level 2 — Standardized patterns

```text
backend-service pattern
frontend pattern
worker pattern
database pattern
```

The organization standardizes how primitives should be assembled and which team supports the result.

### Level 3 — Golden Path automation

```text
Create Backend Service
        ↓
Terraform + Helm + CI + GitOps + observability + ownership
```

Teams express intent and automation composes the supported path.

### Level 4 — Internal Developer Platform

```text
self-service
catalog
ownership
scorecards
documentation
cost visibility
security posture
lifecycle management
```

The platform exposes and operates multiple journeys as products. Atlas gains value at Levels 1–3 without completing every Level 4 capability.

## Critical interview distinctions

| Concept | What it is | What it is not |
|---|---|---|
| Terraform module | Reusable infrastructure primitive | A complete Golden Path |
| Helm chart | Reusable Kubernetes packaging primitive | The entire service lifecycle |
| Reusable CI workflow | Reusable delivery primitive | Infrastructure, runtime, catalog, and ownership |
| Backstage Software Template | Scaffolding/orchestration mechanism | The Golden Path itself |
| Golden Path | Supported end-to-end engineering journey | A mandatory architecture for every workload |
| Internal Developer Platform | Capabilities/products that expose and operate journeys | Merely a portal UI |

> A template is an implementation mechanism. A Golden Path is the supported end-to-end engineering experience.

### Platform versus Golden Path

```text
PLATFORM = capabilities
GOLDEN PATH = recommended journey through those capabilities

Airport = platform
signs + security flow + gates + baggage process = Golden Path
```

An airport can contain excellent infrastructure without giving a traveler an obvious journey. Likewise, a platform can contain EKS, IAM, modules, charts, and telemetry without connecting developer intent to a supported outcome.

### LEGO memory model

```text
Platform
= LEGO pieces

Golden Path
= LEGO kit + instructions for the supported model

Developer Portal
= storefront where engineers select the kit
```

The analogy is intentionally simple. The real platform still needs APIs, automation, policies, infrastructure, support, and ownership behind its interface.

## Platform Lead perspective: problem before portal

A Platform Lead should not begin with `Let's install Backstage.` Start with:

```text
discover repeated developer pain
        ↓
identify common workflows
        ↓
standardize the pattern
        ↓
build reusable primitives
        ↓
compose a supported Golden Path
        ↓
automate self-service
        ↓
measure adoption and friction
        ↓
improve the path
```

Only then choose an interface such as Backstage, Port, Humanitec, a custom portal, CLI, GitHub template, or API. This is not a product comparison. **The portal is not the platform. Installing Backstage does not automatically create Platform Engineering or a useful Golden Path.** A medium organization can begin with versioned modules, one service contract, reusable CI, documented pull-request workflows, and a CLI or repository template.

### Product mindset and evidence

Treat developers as internal customers. Ask how long production-ready service creation takes; how many tickets it needs; where and why teams leave the path; which defaults confuse or block them; how long onboarding takes; whether capabilities are adopted; and whether responders can discover ownership during an incident.

Useful outcome signals include time to first deployment, service-creation lead time, Golden Path adoption, deployment success/failure, developer satisfaction, support-ticket volume, and time spent on common infrastructure work. There are no universal target numbers. Segment the evidence by workload and team, and pair adoption with outcomes: high usage of a frustrating or unreliable path is not success.

## Lifecycle and Day 2

The template is not the finish line:

```text
DISCOVER
   ↓
CREATE
   ↓
BUILD
   ↓
DEPLOY
   ↓
OPERATE
   ↓
OBSERVE
   ↓
MAINTAIN
   ↓
UPGRADE
   ↓
DEPRECATE
```

### What happens after the service has existed for six months?

Scaffolding primarily solves **Day 0/Day 1**. A mature platform must help with **Day 2**: runtime and base-image updates, security fixes, Helm chart and Terraform module evolution, Kubernetes version changes, dependency updates, owner and SLO changes, and eventual deprecation.

A two-year-old template may have generated an old base image, Helm conventions, CI version, and runtime. Atlas therefore versions contracts, publishes compatibility/deprecation policy, inventories consumers, tests upgrades, creates automated update pull requests where safe, provides migration guides, and assigns completion ownership. A template without an upgrade strategy produces standardized legacy services faster.

### Golden State and scorecards

```text
Created correctly
        ↓
six months pass
        ↓
runtime outdated
missing owner
old CI workflow
no SLO
deprecated API
        ↓
no longer in desired Golden State
```

Golden Path describes the supported journey; Golden State asks whether the running service still meets current standards. Scorecards or health checks can surface owner presence, supported runtime, current CI baseline, resource declarations, SLO metadata, runbook, security scanning, and supported deployment pattern.

Treat checks according to risk: **visibility → guidance → warning → policy enforcement**. Not every scorecard item should block a deployment. Explain the reason, remediation, exception, and enforcement owner before turning guidance into policy.

## Complete Golden Path: redraw this on a whiteboard

```text
                         DEVELOPER
                            |
                            v
                    Developer Portal
                    "Create Service"
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
         App Template   Infrastructure   Catalog
              |             Intent          |
              |               |             |
              v               v             v
           GitHub         Terraform       Owner
              |           Modules          Docs
              |             |              SLO
              |             v              Links
              |            AWS
              |      VPC / RDS / IAM / DNS
              |
              v
        Reusable CI Workflow
              |
       +------+------+------+
       |      |      |      |
      Test   Scan   Build   SBOM
                     |
                     v
                    ECR
                     |
                     v
                GitOps Repo
                     |
                     v
                   ArgoCD
                     |
                     v
                    EKS
                     |
             +-------+-------+
             |       |       |
           Pods   Service  Ingress
             |
             v
      Runtime / Application
             |
     +-------+-------+-------+
     |               |       |
     v               v       v
  Metrics           Logs   Traces
     |
     v
 Dashboards / Alerts / SLO

              PLATFORM TEAM OWNS
                        |
      +-----------------+----------------+
      |                 |                |
 Terraform Modules   Helm Charts    CI Workflows
 Policies            Templates      Observability
 Documentation       Guardrails     Upgrade Paths
```

Read it top to bottom: developer intent enters an interface; a template creates code, infrastructure intent, and catalog metadata; Terraform converges AWS infrastructure; CI turns source into an immutable ECR artifact; the GitOps repository records approved deployment intent; ArgoCD reconciles EKS; Kubernetes runs and routes the workload; telemetry and metadata make it operable. The Platform team owns the repeatable paved surface, while application teams own their application within it.

## One service-creation walkthrough

The times below illustrate sequence only; they are not a universal delivery promise.

### 09:00 — Request

The developer selects `Create Backend Service` and supplies `orders-api`, Orders Team, Python, PostgreSQL, external API, environments, and SLO intent.

### 09:02 — Scaffolding

Automation proposes the `orders-api` repository, catalog registration, CI workflow, Helm values, docs/runbook skeleton, and infrastructure declaration.

### 09:05 — Review boundary

An initial pull request is ready for ownership, security-sensitive intent, capacity, and service-specific behavior to be reviewed. These timestamps do not imply RDS or production is ready in five minutes.

### After review and merge — Artifact

```text
test → scan → build → publish immutable image
```

### Infrastructure and deployment

Terraform provisions approved supporting resources. Desired deployment state references the digest; ArgoCD reconciles it into EKS.

### Runtime and operations

```text
Deployment → ReplicaSet → Pods → readiness → EndpointSlice → Service → Ingress/LB
```

The service then appears through the catalog, Grafana, searchable logs, relevant alerts, and the SLO view. Each surface must be verified; generation alone is not evidence that it works.

## Ownership split

Exact boundaries vary between organizations; this is Atlas's explicit starting contract.

| Application team owns | Platform team owns | Shared responsibility |
|---|---|---|
| Application code and business logic | Supported service patterns | Capacity |
| Tests and application health semantics | Terraform modules and Helm/service abstractions | Security |
| Resource requirements | CI baseline and GitOps tooling | Reliability |
| SLO requirements with stakeholders | Cluster platform and identity integration | Cost |
| Dependency choices within supported boundaries | Observability capabilities and policy/guardrails | Incident response |
| Application incidents | Documentation and Golden Path lifecycle | Upgrades |

“Shared” still needs a named decision owner for each change or incident. Platform owns the reusable capability; the application team remains accountable for business behavior and operating its service.

## Failure scenarios improve the product

### Missing IAM capability

`orders-api` works in development but production fails because it needs an IAM permission absent from the standard path. The bad response is `developer manually edits IAM`: it creates unaudited drift and teaches the team to bypass the platform.

```text
Is this requirement common?
        |
        +--> No
        |     ↓
        |  explicit escape hatch with risk owner
        |
        +--> Yes
              ↓
        improve supported IAM module/path
              ↓
        test, document, and migrate consumers
              ↓
        future teams self-service it
```

The Platform Lead distinguishes solving one ticket from improving the platform product. First verify the workload identity and exact denied AWS action/resource; then decide whether the capability belongs in the contract.

### A team bypasses slow database provisioning

A team bypasses the path because the standard database module is slow or lacks required configuration. Do not begin with “developer noncompliance.” Ask: Why did the path fail the team? Is the use case legitimate? Is provisioning unreliable or approval-bound? Is the abstraction too restrictive? Should the option become supported, or remain a time-bounded exception?

Adoption is earned. Repeated escape reasons are product research; one-off requirements may remain explicitly owned exceptions.

## Interview questions

1. What is a Golden Path?
2. How is a Golden Path different from a Terraform module?
3. How is a Backstage Software Template different from a Golden Path?
4. Do you need Backstage to implement Platform Engineering?
5. What happens after a developer clicks Create Service?
6. What should the Platform team own?
7. What should application teams own?
8. Why should observability be part of the Golden Path?
9. Why is `Pod Running` not sufficient production readiness?
10. How would you design a Golden Path for an organization with 100 engineers?
11. Where does Terraform fit?
12. Where does Helm fit?
13. Where does ArgoCD fit, and what does it not do?
14. Where does the Software Catalog fit?
15. How would you handle a workload outside the Golden Path?
16. How would you measure whether the path succeeds?
17. What is the difference between Golden Path and Golden State?
18. How do you prevent generated services becoming outdated?
19. How would you evolve shared modules into an internal developer platform?
20. What should you build first: Backstage or reusable platform capabilities?
21. How would you convince developers to adopt the path?
22. What happens when the path becomes too restrictive?
23. How does a Golden Path improve security?
24. How does it improve incident response?
25. How would you design separate paths for APIs, workers, frontends, and data workloads?

## High-value interview answers

### 1. What is a Golden Path?

**30-second answer:** A Golden Path is the supported, opinionated, end-to-end way to deliver a common workload. It composes Terraform modules, Helm charts, CI workflows, GitOps, identity, observability, and organizational standards into an easy self-service journey. Its goal is to make the secure, observable, production-ready route the easiest route while retaining explicit escape hatches for justified exceptions.

**2-minute expansion:** I would define the workload and boundary first—for example an HTTP API on EKS—not promise one architecture for everything. Then I would trace developer intent through repository creation, infrastructure, immutable artifact, desired deployment state, reconciliation, operations, ownership, and upgrades. A team owns that contract, measures adoption and outcomes, and improves repeated exceptions. The template or portal is only one implementation surface.

### 2. How is it different from Terraform or Helm?

**30-second answer:** A Terraform module standardizes infrastructure and a Helm chart packages Kubernetes resources. Both are primitives. The Golden Path decides when and how they combine with source control, CI, identity, GitOps, observability, ownership, support, and lifecycle to produce an operable service.

### 3. Is a Backstage template the Golden Path?

**30-second answer:** No. A Backstage Software Template collects intent and invokes scaffolding or organizational automation. The Golden Path includes everything before and after that action: the supported contract, review, infrastructure, build, deployment, operation, upgrades, and escape process. Backstage can expose the path, but a CLI or Git workflow can too.

### 4. What happens after Create Service?

**30-second answer:** Automation creates application and infrastructure intent plus ownership metadata. Terraform provisions approved dependencies. CI tests, scans, builds, and publishes an immutable image. A GitOps change references its digest; ArgoCD reconciles that desired state to EKS. Kubernetes runs it, and catalog and observability integrations make ownership, health, logs, metrics, traces, runbook, and SLO discoverable.

### 5. Why is `Pod Running` insufficient?

**30-second answer:** Running describes a Pod phase, not a correct user result. I still need readiness, routing, dependency health, useful metrics/logs/traces, alerts tied to user impact, an owner, SLO, and runbook. Production readiness includes the ability to detect, understand, and respond to failure.

### 6. How do you handle exceptions?

**30-second answer:** Make the common path easiest, then provide a documented review route with risk ownership and support boundaries. If an exception repeats and is broadly useful, productize it. If it is genuinely unusual, permit it with compensating controls rather than either forcing a bad abstraction or allowing invisible drift.

### 7. What should a Platform Lead build first?

**30-second answer:** Discover repeated pain, select one common workflow, define its production contract, and build the minimum reliable primitives and documentation. Automate that route through the simplest suitable interface. Installing a portal before understanding the workflow produces a polished front door to unresolved complexity.

### 8. How do you measure success?

**30-second answer:** Combine adoption with outcomes: service-creation lead time, time to first deployment, deployment reliability, ticket volume, developer satisfaction, and infrastructure effort. Examine where teams leave the path and why. I avoid a vanity adoption target because forced usage can hide friction without improving delivery.

### 9. Golden Path versus Golden State?

**30-second answer:** Golden Path is how a service starts and moves through the supported lifecycle. Golden State is whether it still meets current standards later. Scorecards can reveal outdated runtimes, CI, owners, runbooks, scanning, or SLO metadata; migrations and ownership are needed to restore state.

### 10. Why does a medium organization need this?

**30-second answer:** The driver is repeated organizational complexity, not internet-scale traffic. With roughly 30 services and 100 engineers, inconsistent identity, delivery, ownership, telemetry, and upgrades already impose tickets and incident risk. A thin path for the common workload can reduce that coordination cost without building a Spotify-scale portal.

## Final memory anchors

```text
PRIMITIVES
Terraform / Helm / CI libraries
        ↓
PATTERN
How they should be assembled
        ↓
GOLDEN PATH
Supported end-to-end journey
        ↓
SELF-SERVICE
Portal / CLI / API / template
        ↓
PLATFORM PRODUCT
Operate, measure, improve
        ↓
GOLDEN STATE
Keep services healthy over time
```

```text
Platform
= capabilities

Golden Path
= supported journey

Template
= automation mechanism

Portal
= interface

Catalog
= discovery + ownership

Golden State
= ongoing standards/health
```

```text
Platform
= LEGO pieces

Golden Path
= LEGO kit + instructions

Developer Portal
= storefront
```

```text
easy
=
secure
=
observable
=
supported
=
production-ready
```

The shortest reconstruction is: **intent → template → repositories → Terraform/CI → artifact → GitOps → ArgoCD → EKS → observability/ownership → Day 2 Golden State**.
