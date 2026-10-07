<p align="right">
  <a href="../es/0004-clave-particion-cc-num.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0004: Partition key by card number

| Status | Date |
|---|---|
| Accepted | 2026-10-05 |

## Context

Window features depend on the order in which each card's transactions arrive. Kafka only guarantees order within a
single partition.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Card number | Order guaranteed per card. Each card is processed by a single consumer | Partitions may become unbalanced if one card concentrates a lot of traffic |
| Transaction identifier | Even distribution across partitions | Per-card order is lost and windows would be computed over out-of-order events |
| Merchant | Order per merchant | Breaks per-card order, which is what most features rely on |

## Decision

Both incoming events and published decisions use the card number as the partition key.

## Consequences

- Per-card features need no coordination between consumers.
- Per-merchant features are shared between consumers, so their updates in the state store must be atomic.
- Maximum consumer parallelism equals the number of partitions.
