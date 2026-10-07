<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0002-apache-kafka.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0002: Apache Kafka como broker de eventos

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

El sistema necesita un registro de eventos duradero, ordenado por clave y que se pueda volver a leer desde cualquier
punto. Así el productor y el consumidor quedan desacoplados y el estado se puede reconstruir a partir del histórico
del propio broker. El despliegue final es en AWS.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Apache Kafka (modo KRaft) | Estándar de la industria. Permite releer desde cualquier posición. Ecosistema maduro. Migra a Amazon MSK sin cambios en las aplicaciones | Más pesado y con más configuración en local |
| Redpanda | Un solo binario, arranque rápido y compatible con Kafka | Menos presente en el mercado laboral y sin equivalente gestionado en AWS |
| Amazon Kinesis Data Streams | Servicio nativo de AWS, sin brokers que gestionar | No se puede ejecutar en local sin emuladores. Su modelo de clientes es distinto y la relectura es menos flexible |

## Decisión

Se usa Apache Kafka en modo KRaft, sin ZooKeeper. En local corre un único nodo; en AWS se usa Amazon MSK.

## Consecuencias

- Los topics se crean de forma explícita y versionada; el broker no los crea automáticamente.
- Todos los componentes usan el mismo cliente de Kafka.
- Amazon MSK tiene coste mientras está encendido, aunque no haya tráfico, así que el entorno de AWS se levanta solo para pruebas.
