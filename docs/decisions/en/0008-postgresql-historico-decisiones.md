<p align="right">
  <a href="../es/0008-postgresql-historico-decisiones.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0008: PostgreSQL for history, decisions and model registry

| Status | Date |
|---|---|
| Accepted | 2026-10-05 |

## Context

A queryable store is needed for the transaction history, the decisions with their traceability, the review panel
queue and the model version registry.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| PostgreSQL | Full SQL. Indexes suited to the review queue. Support for semi-structured data. Available as Amazon RDS | Not designed as a large-scale analytical store |
| Amazon DynamoDB | Scales without management | Aggregations and the review queue are hard to model |
| S3 with Athena | Very cheap for history | High latency for the panel and cannot update a case's review status |

## Decision

PostgreSQL is used, as Amazon RDS on AWS. History is also stored in S3 in Parquet format for analytical queries with
Athena.

## Consequences

- The review queue relies on an index limited to pending cases, so the panel does not scan the whole table.
- Database schema changes are managed as versioned migrations.
