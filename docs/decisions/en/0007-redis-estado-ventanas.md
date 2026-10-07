<p align="right">
  <a href="../es/0007-redis-estado-ventanas.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0007: Redis as the window state store

| Status | Date |
|---|---|
| Accepted | 2026-10-05 |

## Context

Each event needs to read and update counters over one-hour, one-day and seven-day windows within a few milliseconds.
That state must survive a consumer restart and be readable by the scoring API.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Redis | Sub-millisecond latency. Data structures suited to time windows. Shared between services | One more service and risk of losing state |
| Local state in the consumer | No network calls | Lost or redistributed when consumers restart or scale. The API cannot read it |
| PostgreSQL | Already part of the system | Computing windows on every event is too slow for the latency target |

## Decision

Window state is stored in Redis, with atomic updates per event. On AWS, Amazon MemoryDB for Redis is used.

## Consequences

- Locally, Redis persists its content to disk to survive restarts; on AWS, MemoryDB provides durability across availability zones.
- If the state is lost, it is rebuilt by re-reading the last seven days of the input topic, so its retention must exceed that window.
