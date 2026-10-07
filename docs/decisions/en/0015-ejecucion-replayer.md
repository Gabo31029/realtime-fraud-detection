<p align="right">
  <a href="../es/0015-ejecucion-replayer.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0015: Running the replayer as an ECS Fargate task

| Status | Date |
|---|---|
| Accepted | 2026-10-06 |

## Context

The replayer is a long-running process: replaying the full history takes from minutes to several hours depending on
the chosen pace. It must emit events in a single ordered stream, set the pace with its own clock and connect to Kafka
inside the private network. Locally it runs as a process or a container; on AWS, a place to run it has to be chosen.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Amazon ECS task on Fargate | Uses the same container image as locally. Serverless. Billed only while running. Launched on demand inside the same network as MSK. Logs in CloudWatch | Takes about a minute to start and requires publishing the image to ECR |
| AWS Lambda | Serverless and pay-per-invocation | Each execution is capped at 15 minutes, which forces the replay to be split into chunks with the position saved between them. Order and pace no longer depend on a single process |
| Amazon EC2 | Full control of the environment | The server has to be maintained and is billed while running, even when idle |
| Amazon Managed Service for Apache Flink | Managed service | Oversized for a producer and requires rewriting the replayer |

## Decision

On AWS, the replayer runs as an ECS task on Fargate, with its image published to Amazon ECR. It reads the prepared
history from S3, publishes to Amazon MSK and finishes when the replay ends.

Dataset preparation is not part of that task: it runs once and its output is stored in S3.

## Consequences

- The same container is used locally and on AWS; only the configuration changes.
- The task needs read access to the data bucket and network access to MSK and the Schema Registry.
- If the task is interrupted, it is relaunched from the last processed date; repeated events are discarded by the consumer (ADR-0010).
