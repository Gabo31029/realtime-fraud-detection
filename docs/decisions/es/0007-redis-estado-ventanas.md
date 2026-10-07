<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0007-redis-estado-ventanas.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0007: Redis como almacén del estado de las ventanas

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

Cada evento necesita leer y actualizar contadores en ventanas de una hora, un día y siete días en pocos
milisegundos. Ese estado tiene que sobrevivir al reinicio de un consumidor y poder leerse desde la API de scoring.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Redis | Latencia inferior al milisegundo. Estructuras adecuadas para ventanas por tiempo. Compartido entre servicios | Un servicio más y riesgo de perder el estado |
| Estado local en el consumidor | Sin llamadas de red | Se pierde o se redistribuye al reiniciar o escalar consumidores. La API no puede leerlo |
| PostgreSQL | Ya forma parte del sistema | Calcular ventanas en cada evento es demasiado lento para el objetivo de latencia |

## Decisión

El estado de las ventanas se guarda en Redis, con actualizaciones atómicas por evento. En AWS se usa Amazon MemoryDB
for Redis.

## Consecuencias

- En local, Redis persiste su contenido en disco para sobrevivir a reinicios; en AWS, MemoryDB aporta durabilidad entre zonas de disponibilidad.
- Si el estado se pierde, se reconstruye releyendo los últimos siete días del topic de entrada, por lo que su retención debe superar esa ventana.
