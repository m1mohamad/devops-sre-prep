---
title: CI/CD and GitOps Questions
tags: [interview, study]
aliases: [CI/CD and GitOps Questions practice]
---

# CI/CD and GitOps Questions

Use these prompts for closed-book rehearsal. Answer in 30 seconds, expand mechanism and trade-offs for three minutes, then connect one honest experience. Full answer frameworks are in the [Interview Companion](../../interview/index.md).

* How do you promote one immutable artifact across environments?
* Argo CD is OutOfSync but the application works; what do you inspect?
* How would you prevent an untrusted pull request from stealing CI credentials?
* Design a pipeline that provides useful evidence in under ten minutes.
* How do you make container builds reproducible?
* What should an artifact provenance attestation prove?
* How do you roll back a GitOps deployment safely?
* Compare Argo CD and Flux for a multi-tenant platform.
* How do you separate deployment from release?
* When is blue-green safer than a canary?
* How would you detect and control configuration drift?
* How do you rotate a signing key without stopping delivery?

## Practice Loop

```mermaid
flowchart LR
  Prompt --> Short[30-second answer] --> Deep[Mechanics and trade-offs] --> Story[Experience evidence] --> Review
```

Avoid memorized scripts: state assumptions and test them.
