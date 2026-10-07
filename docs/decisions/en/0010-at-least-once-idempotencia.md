<p align="right">
  <a href="../es/0010-at-least-once-idempotencia.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0010: At-least-once delivery with idempotent writes

| Status | Date |
|---|---|
| Accepted | 2026-10-05 |

## Context

If a consumer fails between processing an event and committing its position in Kafka, that event is processed
again. That reprocessing must not duplicate decisions or inflate window counters.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| At-least-once with idempotent writes | Simple and robust to restarts | Requires an identifier for deduplication |
| Kafka transactions (exactly-once) | Strong guarantee within Kafka | Does not cover writes to Redis or PostgreSQL |
| At-most-once | Simplest option | Events are lost on any failure |

## Decision

The consumer commits its position in Kafka only after persisting the result. Duplicates are discarded by transaction
identifier, both in the state store and in the database. The producer is idempotent and waits for acknowledgement from
all replicas.

## Consequences

- Reprocessing an event changes neither the state nor the tables.
- If the database is unavailable, the consumer stops instead of moving forward, and no events are lost.
