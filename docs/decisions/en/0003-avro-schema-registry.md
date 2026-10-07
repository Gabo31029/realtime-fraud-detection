<p align="right">
  <a href="../es/0003-avro-schema-registry.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0003: Avro and Schema Registry as the data contract

| Status | Date |
|---|---|
| Accepted | 2026-10-05 |

## Context

The producer and the consumers evolve independently. A data contract is needed that is validated before publishing
and that allows new fields to be added without breaking existing consumers.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Avro with Confluent Schema Registry | Validates the event before publishing. Enforces compatibility between versions. Compact binary messages. Native support in the Python client | One more service to operate |
| JSON Schema with Schema Registry | Human-readable messages | Larger messages and more expensive validation |
| Schemaless JSON | Simplest option | No contract; errors surface late, in the consumer |
| AWS Glue Schema Registry | Managed by AWS | No official serializer for Python |

## Decision

Events are serialized in Avro and validated against Confluent Schema Registry with backward compatibility (BACKWARD).
On AWS the registry runs as a service on ECS Fargate.

## Consequences

- Schemas are versioned alongside the code and registered on deployment.
- Any new field must be optional and have a default value, so existing consumers keep working.
