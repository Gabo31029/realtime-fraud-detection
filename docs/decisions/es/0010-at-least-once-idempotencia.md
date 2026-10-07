<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0010-at-least-once-idempotencia.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0010: Entrega al menos una vez con escrituras idempotentes

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

Si un consumidor falla entre procesar un evento y confirmar su posición en Kafka, ese evento se vuelve a procesar.
Ese reprocesamiento no puede duplicar decisiones ni inflar los contadores de las ventanas.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Al menos una vez con escrituras idempotentes | Simple y robusto ante reinicios | Requiere un identificador para deduplicar |
| Transacciones de Kafka (exactamente una vez) | Garantía fuerte dentro de Kafka | No cubre las escrituras en Redis ni en PostgreSQL |
| Como máximo una vez | Lo más simple | Se pierden eventos ante cualquier fallo |

## Decisión

El consumidor confirma su posición en Kafka solo después de persistir el resultado. Los duplicados se descartan por
identificador de transacción, tanto en el almacén de estado como en la base de datos. El productor es idempotente y
espera la confirmación de todas las réplicas.

## Consecuencias

- Reprocesar un evento no altera ni el estado ni las tablas.
- Si la base de datos no está disponible, el consumidor se detiene en lugar de avanzar, y no se pierden eventos.
