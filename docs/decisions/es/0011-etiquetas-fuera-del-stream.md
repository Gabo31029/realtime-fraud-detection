<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0011-etiquetas-fuera-del-stream.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0011: Etiquetas de fraude fuera del stream y con retraso

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

En la realidad el fraude se confirma semanas después de la transacción, cuando llega el contracargo. Si la etiqueta
viaja en el evento, o se usa antes de estar disponible, el entrenamiento aprende con información del futuro.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Etiquetas en un almacén aparte, con fecha de disponibilidad | Reproduce el retraso real y evita fugas de información | Más lógica al generar el dataset de entrenamiento |
| Etiqueta dentro del evento | Simple | Fuga directa de información y no refleja la realidad |

## Decisión

El replayer elimina la etiqueta antes de publicar. Las etiquetas se guardan aparte con una fecha de disponibilidad de
30 días después de la transacción, y el dataset de entrenamiento solo usa las que ya están disponibles en la fecha de
corte.

## Consecuencias

- El reentrenamiento trabaja siempre con un desfase de 30 días respecto a los datos más recientes.
- La división temporal entre entrenamiento y validación se define por fecha de corte y se acuerda con el equipo de ciencia de datos.
