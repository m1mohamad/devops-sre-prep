---
title: Storage and CSI
tags: [kubernetes, platform-engineering]
aliases: [Storage and CSI study note]
---

# Storage and CSI

## 30-Second Answer

Storage and CSI is the path from **PersistentVolumeClaim** to **VolumeSnapshot**. The essential handoffs are StorageClass, CSI provisioner, PersistentVolume, attach and mount. In production, I verify each handoff independently, keep its identity and state boundary visible, and operate it against availability, latency, security, and recovery objectives.

## Mental Model

```mermaid
flowchart LR
  N0[PersistentVolumeClaim] --> N1[StorageClass] --> N2[CSI provisioner] --> N3[PersistentVolume] --> N4[attach and mount] --> N5[VolumeSnapshot]
```

Read this diagram as a concrete sequence, not a generic maturity loop: a failure after **attach and mount** has different evidence and ownership from a failure at **StorageClass**.

## Why It Exists

Without storage and csi, teams must manually coordinate persistentvolumeclaim, persistentvolume, and volumesnapshot. The technology standardizes those interfaces so changes are repeatable, reviewable, and diagnosable. It is justified when the repeated operational risk exceeds the cost of owning the abstraction.

## How It Works

**PersistentVolumeClaim** owns stage 1; **StorageClass** owns stage 2; **CSI provisioner** owns stage 3; **PersistentVolume** owns stage 4; **attach and mount** owns stage 5; **VolumeSnapshot** owns stage 6. Follow resource IDs, revisions, events, and timestamps across these stages; an acknowledgement at one stage never proves completion at the next.

## Mechanisms

* **PersistentVolumeClaim:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **StorageClass:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **CSI provisioner:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **PersistentVolume:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **attach and mount:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.
* **VolumeSnapshot:** Inspect its native state, events, latency, permissions, and capacity before moving to the next component.

## Production Architecture

Deploy persistentvolumeclaim with least privilege and an auditable change path. Isolate persistentvolume by environment and failure domain, make volumesnapshot observable, and test loss of each dependency. Version the interface between stages so producers and consumers can roll independently.

## Failure Modes

| Failure | Evidence | Response |
|---|---|---|
| API or watch lag hides progress | Compare stage latency and revision at StorageClass | Stop promotion and restore the last verified input |
| resource, IP, or storage capacity blocks convergence | Inspect saturation, quotas, events, and pending work at PersistentVolume | Add valid capacity or shed load; do not retry without a bound |
| a probe or policy reports a misleading serving state | Compare the user result with VolumeSnapshot and upstream state | Mitigate first, preserve evidence, then repair the faulty contract |

## Trade-offs

More automation across persistentvolumeclaim and volumesnapshot improves consistency but can propagate an error faster. Strong isolation narrows blast radius but increases cost and upgrades. Managed implementations reduce component toil; self-managed implementations offer control but require availability, backup, security patching, and on-call expertise.

## Lead-Level Follow-ups

* Which team owns **PersistentVolume**, and what user-facing SLO proves it works?
* What remains available when **StorageClass** is down?
* Where is state durable, and how are restore and upgrade tested?

## My Experience Prompt

Describe a change to persistentvolume: state the constraint, the exact signal that selected the design, the rollback boundary, and the durable guardrail you added.

## Recall Check

1. What does **PersistentVolumeClaim** send to **StorageClass**?
2. Which component stores or reports authoritative state?
3. How does **attach and mount** affect **VolumeSnapshot**?
4. Which capacity limit fails first at production scale?
5. When is a simpler managed alternative preferable?

## Related Notes

* [Category index](index.md)
* [Interview dashboard](../00-interview-dashboard.md)
