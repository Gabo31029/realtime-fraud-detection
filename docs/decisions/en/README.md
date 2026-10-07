<p align="right">
  <a href="../es/README.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# Architecture Decision Records

Record of the project's architecture decisions (ADRs). Each decision has its own document describing the context that
motivated it, the options considered, the decision taken and its consequences.

## Decisions

| ADR | Decision | Description | Status |
|---|---|---|---|
| [ADR-0001](0001-dataset-sparkov.md) | Sparkov dataset as the data source | The simulated Sparkov dataset is used as the transaction history; IEEE-CIS remains an optional source. | Accepted |
| [ADR-0002](0002-apache-kafka.md) | Apache Kafka as the event broker | Kafka in KRaft mode carries events between components; on AWS its managed version, Amazon MSK, is used. | Accepted |
| [ADR-0003](0003-avro-schema-registry.md) | Avro and Schema Registry as the data contract | Events are serialized in Avro and validated against Confluent Schema Registry with backward compatibility. | Accepted |
| [ADR-0004](0004-clave-particion-cc-num.md) | Partition key by card number | Events are partitioned by card number to guarantee the order of each card's transactions. | Accepted |
| [ADR-0005](0005-consumidor-python.md) | Stream processing with a Python consumer | Streaming is processed by a custom Python consumer instead of Flink or Spark, due to volume and code reuse. | Accepted |
| [ADR-0006](0006-libreria-features-compartida.md) | A single feature implementation for batch and streaming | Features are implemented once and reused for training and inference to avoid training-serving skew. | Accepted |
| [ADR-0007](0007-redis-estado-ventanas.md) | Redis as the window state store | 1 h, 24 h and 7-day window counters per card and merchant are kept in Redis; on AWS, in MemoryDB. | Accepted |
| [ADR-0008](0008-postgresql-historico-decisiones.md) | PostgreSQL for history, decisions and model registry | PostgreSQL stores the history, every decision with its traceability, the review queue and model versions. | Accepted |
| [ADR-0009](0009-modelo-embebido-consumidor.md) | Model embedded in the consumer | The consumer runs the model in memory instead of calling the API per event, to meet the latency target. | Accepted |
| [ADR-0010](0010-at-least-once-idempotencia.md) | At-least-once delivery with idempotent writes | An event may be processed more than once, but writes are designed so that this never duplicates data or counters. | Accepted |
| [ADR-0011](0011-etiquetas-fuera-del-stream.md) | Fraud labels outside the stream and delayed | The fraud label never travels with events and is only used for training 30 days later, as with a real chargeback. | Accepted |
| [ADR-0012](0012-airflow-orquestacion-batch.md) | Airflow for batch orchestration | Airflow orchestrates history loading, dataset generation, retraining and model promotion. | Accepted |
| [ADR-0013](0013-observabilidad.md) | Prometheus-format metrics and CloudWatch on AWS | Services expose Prometheus-format metrics; locally they are viewed with Prometheus and Grafana, and on AWS with CloudWatch. | Proposed |
| [ADR-0014](0014-despliegue-local-y-aws.md) | Docker Compose locally and managed services on AWS | The full system runs locally with Docker Compose and is deployed on AWS managed services defined with Terraform. | Accepted |
| [ADR-0015](0015-ejecucion-replayer.md) | Running the replayer as an ECS Fargate task | On AWS the replayer runs as an on-demand ECS Fargate task, not on Lambda or EC2. | Accepted |

## Statuses

| Status | Meaning |
|---|---|
| Proposed | Under discussion, not yet in effect |
| Accepted | In effect |
| Superseded | Replaced by a later ADR, referenced in the document |
| Rejected | Evaluated and not adopted |

## How to record a decision

1. Copy the [template](template.md) using the next number and a short title, and create its Spanish version with the same name in the es folder, from its [template](../es/template.md).
2. Describe the context, options, decision and consequences in architectural terms, without code.
3. Set the status to Proposed and add the row to this index and to its Spanish version.
4. An accepted ADR is never edited: if the decision changes, a new one is created and the old one becomes Superseded.
