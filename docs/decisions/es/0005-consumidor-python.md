<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0005-consumidor-python.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0005: Procesamiento de streaming con un consumidor en Python

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

El volumen esperado es de cientos de eventos por segundo y el estado por tarjeta es pequeño. La lógica de features
tiene que ser exactamente la misma en el camino batch y en el de streaming.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Consumidor propio en Python | Simple. Comparte código con el batch y con el modelo. Fácil de probar | Escalado manual hasta el número de particiones. No trae gestión de estado incorporada |
| Apache Flink (Amazon Managed Service for Apache Flink) | Estado gestionado, ventanas nativas y entrega exactamente una vez | Obliga a reescribir las features en otra API. Curva de aprendizaje y coste |
| Spark Structured Streaming | Unifica batch y streaming | Procesa en microlotes, con más latencia. Infraestructura pesada para este volumen |

## Decisión

El procesamiento en streaming lo hace un consumidor en Python. Flink se reconsiderará solo si el volumen o el tamaño
del estado lo exigen.

## Consecuencias

- El estado de las ventanas se guarda fuera del consumidor (ADR-0007).
- La garantía de entrega se resuelve con entrega al menos una vez y escrituras idempotentes (ADR-0010).
