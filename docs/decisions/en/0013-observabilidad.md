<p align="right">
  <a href="../es/0013-observabilidad.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0013: Prometheus-format metrics and CloudWatch on AWS

| Status | Date |
|---|---|
| Proposed | 2026-10-05 |

## Context

The project requires measuring latency (50th, 95th and 99th percentiles), throughput, consumer lag and rejected
events. Those metrics must be exposed by the services, stored and visualized, both locally and on AWS.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Prometheus-format metrics. Prometheus and Grafana locally; CloudWatch on AWS | Services are instrumented once. On AWS, CloudWatch collects those same metrics from the containers, along with the ones MSK, RDS and MemoryDB already publish | Two different visualization tools between local and AWS |
| Prometheus and Grafana in every environment (managed versions on AWS) | The same dashboards locally and on AWS | Two more managed services, with their cost and permission setup |
| CloudWatch only, sending metrics from the code | A single AWS-native system | Requires an AWS account even locally and couples the services to AWS |

## Decision

Services expose their metrics in Prometheus format. Locally, Prometheus and Grafana collect and visualize them. On
AWS, CloudWatch Container Insights collects them from the ECS containers, together with the MSK, RDS and MemoryDB
metrics.

## Consequences

- Services do not depend on AWS to emit metrics.
- Grafana dashboards are not reused on AWS; an equivalent CloudWatch dashboard has to be built.
