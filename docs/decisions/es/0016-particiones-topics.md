<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0016-particiones-topics.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0016: Número de particiones de los topics

| Estado | Fecha |
|---|---|
| Aceptada | 2026-11-17 |

## Contexto

El número de particiones de un topic fija el paralelismo máximo del consumo: cada partición la lee un único consumidor
del grupo ([ADR-0004](0004-clave-particion-cc-num.md)). Además, la partición de cada mensaje se calcula como el hash
de su clave módulo el número de particiones, así que cambiar ese número después mueve tarjetas de una partición a
otra y rompe temporalmente el orden por tarjeta. Conviene elegirlo bien desde el principio.

### Datos medidos

Sobre el dataset completo de Sparkov (`fraudTrain.csv` y `fraudTest.csv`):

| Medida | Valor |
|---|---|
| Transacciones | 1.852.394, de enero de 2019 a diciembre de 2020 |
| Tarjetas distintas | 999 |
| Comercios distintos | 693 |
| Transacciones por hora de datos | Media 106, percentil 99 de 306, máximo 362 |
| Tarjeta más activa | 4.392 transacciones (0,24 % del total) |
| Tamaño de un mensaje en `transactions.raw` (valor Avro y clave) | Media 151 bytes, máximo 181 |

Con la velocidad por defecto del replayer (`--speedup 3600`, una hora de datos por segundo), el ritmo medio es de
106 eventos por segundo, con picos de 362. El requisito de throughput sostenido es de 500 eventos por segundo, que se
alcanza con `--max-rate 500`.

### Estimaciones

- **Carga de diseño:** 500 eventos por segundo con un margen de 2 veces para picos y reprocesos: 1.000 eventos por
  segundo.
- **Volumen en Kafka:** 1.000 eventos por segundo de 151 bytes son unos 150 KB/s. Una partición de Kafka admite varios
  MB/s, así que el broker no es el límite.
- **Capacidad de un consumidor:** se estima en unos 200 eventos por segundo por instancia. Es una cifra conservadora
  para un consumidor en Python ([ADR-0005](0005-consumidor-python.md)) que agrupa las lecturas de Redis por lote,
  ejecuta el modelo en memoria ([ADR-0009](0009-modelo-embebido-consumidor.md)) y escribe en PostgreSQL. **No está
  medida**: el consumidor todavía no existe.
- **Particiones necesarias:** 1.000 / 200 = 5 consumidores en paralelo, y por tanto al menos 5 particiones.

### Reparto de tarjetas

El productor de `confluent-kafka` (librdkafka) asigna la partición con CRC32 de la clave. Aplicado a las 999 tarjetas:

| Particiones | Tarjetas por partición | Eventos de la partición más cargada frente a la media |
|---|---|---|
| 3 | Entre 326 y 344 | 1,06 |
| 6 | Entre 149 y 185 | 1,10 |
| 12 | Entre 67 y 99 | 1,18 |

Ninguna tarjeta concentra tráfico suficiente para desequilibrar una partición.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| 3 particiones | Reparto más uniforme. Una partición por broker en MSK | Máximo de 3 consumidores: unos 600 eventos por segundo estimados, por debajo de la carga de diseño |
| 6 particiones | Cubre la carga de diseño con margen. Se reparte sin restos entre 1, 2, 3 y 6 consumidores. Dos particiones por broker en MSK | Algo más de desequilibrio que con 3 (10 %) |
| 12 particiones | Más margen de crecimiento | Desequilibrio del 18 %. Más archivos y conexiones en el broker sin que la carga lo necesite |
| Una partición por tarjeta | Aislamiento total por tarjeta | No escala: aparecen tarjetas nuevas cada día y miles de particiones degradan el broker. El paralelismo útil lo limita el número de consumidores, no el de tarjetas |

## Decisión

| Topic | Particiones | Motivo |
|---|---|---|
| `transactions.raw` | 6 | Cubre la carga de diseño (5 consumidores) con margen y se reparte de forma uniforme entre los 3 brokers de MSK |
| `transactions.scored` | 6 | Misma clave y mismo número que `transactions.raw`: la decisión de una tarjeta cae en la partición equivalente a la de su transacción (co-particionado), lo que permite combinar ambos topics por tarjeta sin redistribuir datos |
| `transactions.dlq` | 1 | Recibe una fracción mínima del tráfico, no necesita orden por tarjeta y no se consume en paralelo |

## Consecuencias

- Se pueden tener hasta 6 consumidores en paralelo sin tocar los topics. En local basta con uno, que lee las 6
  particiones.
- La estimación de 200 eventos por segundo por consumidor debe validarse cuando exista el consumidor, publicando con el
  replayer a `--max-rate` creciente. Si la capacidad real está por debajo de unos 170 eventos por segundo, 6
  consumidores no cubren la carga de diseño y hay que revisar esta decisión antes de que existan datos que dependan del
  reparto actual.
- Todos los productores deben usar el mismo particionador. El cliente Java de Kafka (y Kafka Connect) usa murmur2 en
  lugar de CRC32: un productor Java enviaría la misma tarjeta a otra partición. Si se añade uno, hay que configurar
  ambos con el mismo algoritmo.
- El almacenamiento no es una restricción: el dataset completo ocupa unos 280 MB por réplica en `transactions.raw`.
