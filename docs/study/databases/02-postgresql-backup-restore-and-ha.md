---
title: PostgreSQL Backup, Restore, and HA
tags: [databases, interview-prep]
aliases: [PostgreSQL Backup, Restore, and HA]
---

# PostgreSQL Backup, Restore, and HA

## 30-Second Answer

A base backup plus continuous WAL archive enables PITR; replication and snapshots alone are not a tested application-consistent backup.

## Mental Model

Treat the observable boundary as part of the design. Set RPO from archive/replication lag and RTO from restore/failover rehearsal. Fence the former primary before promotion and test restore regularly.

## Architecture Diagram

```mermaid
flowchart LR
  Primary --> WALArchive --> ObjectStore; Primary --> Standby --> Promote
```

## Core Components

The named components in the diagram have different state, saturation signals and owners. Establish which component accepted work, which one made durable progress, and which one produced the user-visible result.

## How It Actually Works

A base backup plus continuous WAL archive enables PITR; replication and snapshots alone are not a tested application-consistent backup. Set RPO from archive/replication lag and RTO from restore/failover rehearsal. Fence the former primary before promotion and test restore regularly.

## Production Design

Define an availability objective, bounded resource consumption, an upgrade path and a reversible operational change. Keep authoritative state separate from caches and derived status.

## Failure Modes

| Failure | Discriminating evidence | Safe first action |
|---|---|---|
| Interface or configuration mismatch | rejection/error at the named boundary | stop the change and compare the last known-good contract |
| Resource saturation | queue or pressure rises before latency/errors | bound admission and relieve the specific bottleneck |
| Dependency unavailable | local health remains good while downstream calls fail | preserve evidence and enter the documented degraded mode |

## Troubleshooting Procedure

```bash
pg_basebackup; pg_verifybackup; pg_isready; select pg_wal_lsn_diff(pg_current_wal_lsn(),replay_lsn)
```

Capture a timestamp and failing example, compare it with a healthy peer, and change one hypothesis at a time.

## Security Considerations

Use least privilege, short-lived credentials, encrypted transport, safe secret handling and auditable changes. Validate untrusted inputs before they cross a privileged boundary.

## Scaling and Cost

Measure demand, concurrency, saturation and unit cost. Scale the constrained resource rather than copying every component; account for redundancy, data transfer and observability retention.

## Trade-offs

Set RPO from archive/replication lag and RTO from restore/failover rehearsal. Fence the former primary before promotion and test restore regularly.

## Lead-Level Follow-ups

* What is authoritative, and who owns recovery?
* Which signal triggers rollback rather than continued diagnosis?
* Which simplification would you choose at one tenth of the scale?

## My Experience Prompt

Describe one production decision involving **PostgreSQL Backup, Restore, and HA**: quantify impact, show the evidence that changed your mind, and name the durable guardrail.

## Recall Check

1. What is the first discriminating signal?
2. Which state survives restart?
3. What is the safest reversible mitigation?

## Related Notes

* [Study Vault](../index.md)
* [Interview dashboard](../00-interview-dashboard.md)

## Further Reading

* [CNCF documentation index](https://www.cncf.io/projects/)
* [Linux manual pages](https://man7.org/linux/man-pages/)
