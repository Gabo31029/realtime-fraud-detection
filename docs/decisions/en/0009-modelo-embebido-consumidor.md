<p align="right">
  <a href="../es/0009-modelo-embebido-consumidor.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0009: Model embedded in the consumer

| Status | Date |
|---|---|
| Accepted | 2026-10-05 |

## Context

The latency target is for 95% of decisions to take less than 200 ms. Every network call adds latency and a point of
failure.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Model loaded in memory in the consumer | No network call per event | Each consumer replica has to load and reload the model |
| Consumer calling the scoring API | A single scoring point | One network call per event. Consumer availability depends on the API |
| Managed endpoint (SageMaker) | Managed scaling and versioning | More latency and more cost |

## Decision

The consumer and the API load the model in memory and share the same scoring code. The API is used for on-demand
synchronous scoring requests.

## Consequences

- Both services detect when the active model version changes and load it without restarting.
- Only the consumer modifies window state; the API only reads it.
