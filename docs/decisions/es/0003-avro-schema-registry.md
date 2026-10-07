<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0003-avro-schema-registry.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0003: Avro y Schema Registry como contrato de datos

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

El productor y los consumidores evolucionan por separado. Hace falta un contrato de datos que se valide antes de
publicar y que permita añadir campos nuevos sin romper a quienes ya consumen los eventos.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Avro con Confluent Schema Registry | Valida el evento antes de publicarlo. Controla la compatibilidad entre versiones. Mensajes binarios compactos. Soporte nativo en el cliente de Python | Un servicio más que operar |
| JSON Schema con Schema Registry | Mensajes legibles | Mensajes más grandes y validación más costosa |
| JSON sin esquema | Lo más simple | No hay contrato; los errores aparecen tarde, en el consumidor |
| AWS Glue Schema Registry | Gestionado por AWS | No tiene serializador oficial para Python |

## Decisión

Los eventos se serializan en Avro y se validan contra Confluent Schema Registry con compatibilidad hacia atrás
(BACKWARD). En AWS el registry se ejecuta como servicio en ECS Fargate.

## Consecuencias

- Los esquemas se versionan junto al código y se registran al desplegar.
- Cualquier campo nuevo debe ser opcional y tener un valor por defecto, para que los consumidores existentes sigan funcionando.
