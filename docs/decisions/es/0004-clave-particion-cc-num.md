<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0004-clave-particion-cc-num.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0004: Clave de partición por número de tarjeta

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

Las features en ventana dependen del orden en que llegan las transacciones de cada tarjeta. Kafka solo garantiza el
orden dentro de una misma partición.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Número de tarjeta | Orden garantizado por tarjeta. Cada tarjeta la procesa un único consumidor | Puede desbalancear particiones si una tarjeta concentra mucho tráfico |
| Identificador de transacción | Reparto uniforme entre particiones | Se pierde el orden por tarjeta y las ventanas se calcularían con eventos desordenados |
| Comercio | Orden por comercio | Rompe el orden por tarjeta, que es el que usan la mayoría de las features |

## Decisión

Tanto los eventos de entrada como las decisiones publicadas usan el número de tarjeta como clave de partición.

## Consecuencias

- Las features por tarjeta no necesitan coordinación entre consumidores.
- Las features por comercio sí se comparten entre consumidores, así que sus actualizaciones en el almacén de estado deben ser atómicas.
- El paralelismo máximo del consumo es igual al número de particiones.
