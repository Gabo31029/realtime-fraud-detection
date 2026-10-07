<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0013-observabilidad.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0013: Métricas en formato Prometheus y CloudWatch en AWS

| Estado | Fecha |
|---|---|
| Propuesta | 2026-10-05 |

## Contexto

El proyecto exige medir latencia (percentiles 50, 95 y 99), throughput, retraso del consumidor y eventos rechazados.
Hace falta exponer esas métricas desde los servicios, almacenarlas y visualizarlas, tanto en local como en AWS.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Métricas en formato Prometheus. Prometheus y Grafana en local; CloudWatch en AWS | Los servicios se instrumentan una sola vez. En AWS, CloudWatch recoge esas mismas métricas de los contenedores, junto con las que ya publican MSK, RDS y MemoryDB | Dos herramientas de visualización distintas entre local y AWS |
| Prometheus y Grafana en todos los entornos (versiones gestionadas en AWS) | Los mismos paneles en local y en AWS | Dos servicios gestionados más, con su coste y su configuración de permisos |
| Solo CloudWatch, enviando las métricas desde el código | Un único sistema, nativo de AWS | Requiere una cuenta de AWS incluso en local y acopla los servicios a AWS |

## Decisión

Los servicios exponen sus métricas en formato Prometheus. En local, Prometheus y Grafana las recogen y visualizan. En
AWS, CloudWatch Container Insights las recoge de los contenedores en ECS, junto con las métricas de MSK, RDS y
MemoryDB.

## Consecuencias

- Los servicios no dependen de AWS para emitir métricas.
- Los paneles de Grafana no se reutilizan en AWS; hay que crear un panel equivalente en CloudWatch.
