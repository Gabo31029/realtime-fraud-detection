<p align="right">
  <a href="../es/0014-despliegue-local-y-aws.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0014: Docker Compose locally and managed services on AWS

| Status | Date |
|---|---|
| Accepted | 2026-10-05 |

## Context

The system must be startable with a single command for development and evaluation, and deployable to AWS as the
final target.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Docker Compose locally and AWS managed services (MSK, ECS Fargate, MemoryDB, RDS, MWAA) defined with Terraform | The same code in both environments, with managed equivalents in the cloud | Two configurations to maintain |
| Everything on a single EC2 instance with Docker Compose | Identical to the local environment | No high availability and no use of managed services |
| Amazon EKS (Kubernetes) | Standard for containers at scale | Excessive complexity and cost for the project |

## Decision

Locally, Docker Compose brings up the whole system. On AWS, each component runs on its equivalent managed service
and the infrastructure is defined as code with Terraform.

## Consequences

- Service configuration is injected through environment variables; on AWS it comes from Secrets Manager.
- The AWS environment is created and destroyed on demand to keep costs under control.
