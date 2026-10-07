<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0015-ejecucion-replayer.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0015: Ejecución del replayer como tarea de ECS Fargate

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-06 |

## Contexto

El replayer es un proceso de larga duración: reproducir el histórico completo tarda de minutos a varias horas según el
ritmo elegido. Tiene que emitir los eventos en un único flujo ordenado, marcar el ritmo con su propio reloj y
conectarse a Kafka dentro de la red privada. En local se ejecuta como proceso o como contenedor; en AWS hay que decidir
dónde ejecutarlo.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Tarea de Amazon ECS en Fargate | Usa la misma imagen de contenedor que en local. Sin servidores. Se paga solo mientras se ejecuta. Se lanza bajo demanda dentro de la misma red que MSK. Registros en CloudWatch | Tarda alrededor de un minuto en arrancar y requiere publicar la imagen en ECR |
| AWS Lambda | Sin servidores y con pago por invocación | Cada ejecución tiene un máximo de 15 minutos, lo que obliga a partir la reproducción en tramos y guardar la posición entre ellos. El orden y el ritmo dejan de depender de un único proceso |
| Amazon EC2 | Control total del entorno | Hay que mantener el servidor y se paga mientras está encendido, aunque no se use |
| Amazon Managed Service for Apache Flink | Servicio gestionado | Sobredimensionado para un productor y obliga a reescribir el replayer |

## Decisión

En AWS, el replayer se ejecuta como una tarea de ECS en Fargate, con la imagen publicada en Amazon ECR. Lee el
histórico preparado desde S3, publica en Amazon MSK y termina al acabar la reproducción.

La preparación del dataset no forma parte de esa tarea: se ejecuta una sola vez y su resultado se guarda en S3.

## Consecuencias

- El mismo contenedor se usa en local y en AWS; solo cambia la configuración.
- La tarea necesita permiso de lectura sobre el bucket de datos y acceso de red a MSK y al Schema Registry.
- Si la tarea se interrumpe, se relanza desde la última fecha procesada; los eventos repetidos se descartan en el consumidor (ADR-0010).
