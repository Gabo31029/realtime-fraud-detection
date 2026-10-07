<p align="right">
  <a href="../es/0012-airflow-orquestacion-batch.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0012: Airflow for batch orchestration

| Status | Date |
|---|---|
| Accepted | 2026-10-05 |

## Context

Loading history, generating the training dataset, retraining and promoting models are batch processes with
dependencies between them. Streaming does not need an orchestrator.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Apache Airflow (Amazon MWAA on AWS) | Industry standard. Workflows defined in Python and identical locally and in the cloud | Amazon MWAA has a high fixed cost |
| AWS Step Functions with EventBridge Scheduler | AWS-native and pay-per-use | Does not run locally and workflows are defined in an AWS-specific language |
| Scheduled jobs with cron | Simplest option | No dependencies, retries or visibility |

## Decision

Airflow orchestrates the batch processes: locally with Docker Compose and on AWS with Amazon MWAA.

## Consequences

- Airflow only coordinates; heavy processing runs on other services, such as Glue or ECS tasks.
- For cost reasons, MWAA will only be brought up to demonstrate the deployment. Step Functions remains the alternative if cost becomes a problem.
