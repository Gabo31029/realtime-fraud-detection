<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0006-libreria-features-compartida.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0006: Una única implementación de las features para batch y streaming

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

Si las features del entrenamiento y las de inferencia se calculan con implementaciones distintas, acaban divergiendo
y el modelo se degrada sin que nada falle de forma visible. Este problema se conoce como training-serving skew.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Una librería común con el almacén de estado intercambiable | Una sola implementación. La paridad se puede comprobar con una prueba automática | La generación del dataset es más lenta, porque recorre el histórico evento a evento |
| SQL para el batch y Python para el streaming | Batch rápido | Dos implementaciones que tienden a divergir |
| Feature store gestionado (SageMaker Feature Store, Feast) | Solución estándar en la industria | Sobredimensionado para el proyecto y oculta la lógica que se quiere demostrar |

## Decisión

Toda la lógica de features vive en una única librería, sin acceso directo a datos externos. El estado de las
ventanas se abstrae detrás de una interfaz común con dos implementaciones: en memoria para el batch y en Redis para el
streaming. El dataset de entrenamiento se genera reproduciendo el histórico en orden temporal con esa misma librería.

## Consecuencias

- Una prueba automática en integración continua compara features y scores de ambos caminos sobre una muestra de 1.000 transacciones.
- El dataset y el modelo guardan la versión del esquema de features con la que se generaron; el consumidor no arranca si no coinciden.
- Cualquier feature nueva que pida el equipo de ciencia de datos se añade a la librería, no a un análisis aparte.
