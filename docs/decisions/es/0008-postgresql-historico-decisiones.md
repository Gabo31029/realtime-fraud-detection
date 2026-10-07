<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0008-postgresql-historico-decisiones.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0008: PostgreSQL para el histórico, las decisiones y el registro de modelos

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

Hace falta un almacén consultable para el histórico de transacciones, las decisiones con su trazabilidad, la cola del
panel de revisión y el registro de versiones de modelo.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| PostgreSQL | SQL completo. Índices adecuados para la cola de revisión. Soporte de datos semiestructurados. Disponible como Amazon RDS | No está pensado como almacén analítico de gran volumen |
| Amazon DynamoDB | Escala sin gestión | Las agregaciones y la cola de revisión son difíciles de modelar |
| S3 con Athena | Muy barato para el histórico | Latencia alta para el panel y no admite actualizar el estado de revisión de un caso |

## Decisión

Se usa PostgreSQL, como Amazon RDS en AWS. El histórico también se guarda en S3 en formato Parquet para consultas
analíticas con Athena.

## Consecuencias

- La cola de revisión se apoya en un índice limitado a los casos pendientes, para que el panel no recorra toda la tabla.
- Los cambios de esquema de la base de datos se gestionan como migraciones versionadas.
