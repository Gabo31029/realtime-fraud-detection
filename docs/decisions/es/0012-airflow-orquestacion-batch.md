<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0012-airflow-orquestacion-batch.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0012: Airflow para la orquestación de procesos batch

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

La carga del histórico, la generación del dataset de entrenamiento, el reentrenamiento y la promoción de modelos son
procesos batch con dependencias entre sí. El streaming no necesita orquestador.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Apache Airflow (Amazon MWAA en AWS) | Estándar de la industria. Flujos definidos en Python e idénticos en local y en la nube | Amazon MWAA tiene un coste fijo alto |
| AWS Step Functions con EventBridge Scheduler | Nativo de AWS y con pago por uso | No se ejecuta en local y los flujos se definen en un lenguaje propio de AWS |
| Tareas programadas con cron | Lo más simple | Sin dependencias, reintentos ni visibilidad |

## Decisión

Airflow orquesta los procesos batch: en local con Docker Compose y en AWS con Amazon MWAA.

## Consecuencias

- Airflow solo coordina; el procesamiento pesado se ejecuta en otros servicios, como Glue o tareas de ECS.
- Por coste, MWAA solo se levantará para demostrar el despliegue. Step Functions queda como alternativa si el coste resulta un problema.
