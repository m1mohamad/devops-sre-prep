---
title: Observability and SRE Questions
tags: [interview, study]
aliases: [Observability and SRE Questions practice]
---

# Observability and SRE Questions

Use these prompts for closed-book rehearsal. Answer in 30 seconds, expand mechanism and trade-offs for three minutes, then connect one honest experience. Full answer frameworks are in the [Interview Companion](../../interview/index.md).

* A deployment increased latency but produced no errors; how do you investigate?
* How do you select an SLI for an asynchronous fraud decision?
* What makes an alert actionable rather than merely accurate?
* How do burn-rate alerts protect an error budget?
* When should a metric label be rejected as high cardinality?
* How do logs and traces complement RED metrics?
* How would you sample traces without losing rare failures?
* What should happen when the telemetry backend is unavailable?
* How do you distinguish saturation from a downstream slowdown?
* How should an error budget change release decisions?

## Practice Loop

```mermaid
flowchart LR
  Prompt --> Short[30-second answer] --> Deep[Mechanics and trade-offs] --> Story[Experience evidence] --> Review
```

Avoid memorized scripts: state assumptions and test them.
