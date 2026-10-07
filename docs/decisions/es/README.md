<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/README.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# Registro de decisiones de arquitectura

Registro de las decisiones de arquitectura del proyecto (ADR). Cada decisión tiene su propio documento con el
contexto que la motivó, las opciones evaluadas, la decisión tomada y sus consecuencias.

## Decisiones

| ADR | Decisión | Descripción | Estado |
|---|---|---|---|
| [ADR-0001](0001-dataset-sparkov.md) | Dataset Sparkov como fuente de datos | Se usa el dataset simulado Sparkov como histórico de transacciones; IEEE-CIS queda como fuente opcional. | Aceptada |
| [ADR-0002](0002-apache-kafka.md) | Apache Kafka como broker de eventos | Kafka en modo KRaft transporta los eventos entre componentes; en AWS se usa su versión gestionada, Amazon MSK. | Aceptada |
| [ADR-0003](0003-avro-schema-registry.md) | Avro y Schema Registry como contrato de datos | Los eventos se serializan en Avro y su esquema se valida contra Confluent Schema Registry con compatibilidad hacia atrás. | Aceptada |
| [ADR-0004](0004-clave-particion-cc-num.md) | Clave de partición por número de tarjeta | Los eventos se particionan por número de tarjeta para garantizar el orden de las transacciones de cada tarjeta. | Aceptada |
| [ADR-0005](0005-consumidor-python.md) | Procesamiento de streaming con un consumidor en Python | El streaming se procesa con un consumidor propio en Python en lugar de Flink o Spark, por volumen y por reutilización de código. | Aceptada |
| [ADR-0006](0006-libreria-features-compartida.md) | Una única implementación de las features para batch y streaming | Las features se implementan una sola vez y se reutilizan en entrenamiento y en inferencia para evitar el training-serving skew. | Aceptada |
| [ADR-0007](0007-redis-estado-ventanas.md) | Redis como almacén del estado de las ventanas | Los contadores en ventana de 1 h, 24 h y 7 días por tarjeta y comercio se mantienen en Redis; en AWS, en MemoryDB. | Aceptada |
| [ADR-0008](0008-postgresql-historico-decisiones.md) | PostgreSQL para el histórico, las decisiones y el registro de modelos | PostgreSQL guarda el histórico, cada decisión con su trazabilidad, la cola de revisión y las versiones de modelo. | Aceptada |
| [ADR-0009](0009-modelo-embebido-consumidor.md) | Modelo cargado dentro del consumidor | El consumidor ejecuta el modelo en memoria en lugar de llamar a la API por cada evento, para cumplir el objetivo de latencia. | Aceptada |
| [ADR-0010](0010-at-least-once-idempotencia.md) | Entrega al menos una vez con escrituras idempotentes | Un evento puede procesarse más de una vez, pero las escrituras están diseñadas para que eso no duplique datos ni contadores. | Aceptada |
| [ADR-0011](0011-etiquetas-fuera-del-stream.md) | Etiquetas de fraude fuera del stream y con retraso | La etiqueta de fraude no viaja en los eventos y solo se usa para entrenar 30 días después, como ocurre con un chargeback real. | Aceptada |
| [ADR-0012](0012-airflow-orquestacion-batch.md) | Airflow para la orquestación de procesos batch | Airflow orquesta la carga del histórico, la generación del dataset, el reentrenamiento y la promoción de modelos. | Aceptada |
| [ADR-0013](0013-observabilidad.md) | Métricas en formato Prometheus y CloudWatch en AWS | Los servicios exponen métricas en formato Prometheus; en local se ven con Prometheus y Grafana, y en AWS con CloudWatch. | Propuesta |
| [ADR-0014](0014-despliegue-local-y-aws.md) | Docker Compose en local y servicios gestionados en AWS | El sistema completo se levanta en local con Docker Compose y se despliega en AWS sobre servicios gestionados definidos con Terraform. | Aceptada |
| [ADR-0015](0015-ejecucion-replayer.md) | Ejecución del replayer como tarea de ECS Fargate | El replayer se ejecuta en AWS como tarea de ECS Fargate bajo demanda, y no en Lambda ni en EC2. | Aceptada |

## Estados

| Estado | Significado |
|---|---|
| Propuesta | En discusión, todavía no vigente |
| Aceptada | Vigente |
| Reemplazada | Sustituida por un ADR posterior, que se indica en el documento |
| Descartada | Evaluada y no adoptada |

## Cómo registrar una decisión

1. Copiar la [plantilla](template.md) con el siguiente número y un título corto, y crear su versión en inglés con el mismo nombre en la carpeta en, a partir de su [plantilla](../en/template.md).
2. Describir el contexto, las opciones, la decisión y sus consecuencias, en lenguaje de arquitectura y sin código.
3. Dejar el estado en Propuesta y añadir la fila a este índice y a su versión en inglés.
4. Un ADR aceptado no se modifica: si la decisión cambia, se crea uno nuevo y el anterior pasa a Reemplazada.
