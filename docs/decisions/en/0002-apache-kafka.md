<p align="right">
  <a href="../es/0002-apache-kafka.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0002: Apache Kafka as the event broker

| Status | Date |
|---|---|
| Accepted | 2026-10-05 |

## Context

The system needs a durable event log, ordered by key and replayable from any point. This decouples producer and
consumer and allows the state to be rebuilt from the broker's own history. The final deployment target is AWS.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Apache Kafka (KRaft mode) | Industry standard. Can be re-read from any position. Mature ecosystem. Migrates to Amazon MSK with no application changes | Heavier and more configuration locally |
| Redpanda | Single binary, fast startup and Kafka-compatible | Less common in the job market and no managed equivalent on AWS |
| Amazon Kinesis Data Streams | AWS-native service with no brokers to manage | Cannot run locally without emulators. Different client model and less flexible replay |

## Decision

Apache Kafka is used in KRaft mode, without ZooKeeper. Locally it runs as a single node; on AWS, Amazon MSK is used.

## Consequences

- Topics are created explicitly and under version control; the broker does not create them automatically.
- All components use the same Kafka client.
- Amazon MSK is billed while running, even with no traffic, so the AWS environment is only brought up for testing.
