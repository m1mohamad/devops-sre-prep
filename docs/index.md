# Platform Engineer Handbook

## Mission

> Build a permanent mental model for shipping, operating, securing, and scaling modern platforms.

```mermaid
---
title: Handbook Map
---
flowchart LR
  Code[Developer Code] --> CI[CI Pipeline]
  CI --> Image[Container Image]
  Image --> GitOps[GitOps Desired State]
  GitOps --> K8s[Kubernetes Runtime]
  K8s --> Obs[Observability]
  Obs --> Improve[Staff Engineering Improvements]
  Improve --> Code
```

## How to use this site

### Read

Follow the Handbook and Engineering Journey from first principles to multi-region operations.

### Practice

Use the Interview Companion and Production Simulator to rehearse realistic staff-level decisions.

### Design

Reuse the Architecture Library diagrams when explaining tradeoffs, failure domains, and scaling paths.
