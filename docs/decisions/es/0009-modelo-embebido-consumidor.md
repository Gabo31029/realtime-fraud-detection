<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0009-modelo-embebido-consumidor.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0009: Modelo cargado dentro del consumidor

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

El objetivo de latencia es que el 95 % de las decisiones tarde menos de 200 ms. Cada llamada de red añade latencia y
un punto de fallo.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Modelo cargado en memoria en el consumidor | Ninguna llamada de red por evento | Cada réplica del consumidor tiene que cargar y recargar el modelo |
| Consumidor que llama a la API de scoring | Un único punto de scoring | Una llamada de red por evento. La disponibilidad del consumidor depende de la API |
| Endpoint gestionado (SageMaker) | Escalado y versionado gestionados | Más latencia y más coste |

## Decisión

El consumidor y la API cargan el modelo en memoria y comparten el mismo código de scoring. La API queda para las
consultas de scoring síncronas bajo demanda.

## Consecuencias

- Ambos servicios detectan cuándo cambia la versión activa del modelo y la cargan sin reiniciarse.
- Solo el consumidor modifica el estado de las ventanas; la API únicamente lo lee.
