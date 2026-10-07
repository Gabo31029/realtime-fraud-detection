<p align="right">
  <a href="../es/0005-consumidor-python.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0005: Stream processing with a Python consumer

| Status | Date |
|---|---|
| Accepted | 2026-10-05 |

## Context

The expected volume is hundreds of events per second and the per-card state is small. The feature logic must be
exactly the same in the batch path and in the streaming path.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Custom Python consumer | Simple. Shares code with batch and with the model. Easy to test | Manual scaling up to the number of partitions. No built-in state management |
| Apache Flink (Amazon Managed Service for Apache Flink) | Managed state, native windows and exactly-once delivery | Requires rewriting the features in another API. Learning curve and cost |
| Spark Structured Streaming | Unifies batch and streaming | Micro-batch processing with higher latency. Heavy infrastructure for this volume |

## Decision

Stream processing is done by a Python consumer. Flink will only be reconsidered if volume or state size require it.

## Consequences

- Window state is stored outside the consumer (ADR-0007).
- The delivery guarantee is handled with at-least-once delivery and idempotent writes (ADR-0010).
