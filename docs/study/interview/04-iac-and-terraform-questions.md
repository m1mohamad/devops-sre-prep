---
title: IaC and Terraform Questions
tags: [interview, study]
aliases: [IaC and Terraform Questions practice]
---

# IaC and Terraform Questions

Use these prompts for closed-book rehearsal. Answer in 30 seconds, expand mechanism and trade-offs for three minutes, then connect one honest experience. Full answer frameworks are in the [Interview Companion](../../interview/index.md).

* How would you design Terraform state for multiple teams and AWS accounts?
* A Terraform state lock is stale during an incident; what do you do?
* How do plan, refresh, and apply relate to remote reality?
* How would you recover a resource accidentally removed from state?
* What belongs in a reusable Terraform module?
* How do provider aliases support multi-account deployments?
* How do you introduce moved blocks during a refactor?
* When is create_before_destroy unsafe?
* How do you detect drift without blindly applying it?
* Compare Terraform, CloudFormation, and Crossplane boundaries.
* When is Ansible preferable to image baking or cloud-init?
* How do you test a breaking provider upgrade?

## Practice Loop

```mermaid
flowchart LR
  Prompt --> Short[30-second answer] --> Deep[Mechanics and trade-offs] --> Story[Experience evidence] --> Review
```

Avoid memorized scripts: state assumptions and test them.
