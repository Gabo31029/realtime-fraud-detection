<p align="right">
  <img src="https://img.shields.io/badge/Espa%C3%B1ol-1f6feb?style=for-the-badge" alt="Español">
  <a href="../en/0001-dataset-sparkov.md"><img src="https://img.shields.io/badge/English-6e7781?style=for-the-badge" alt="English"></a>
</p>

# ADR-0001: Dataset Sparkov como fuente de datos

| Estado | Fecha |
|---|---|
| Aceptada | 2026-10-05 |

## Contexto

No existe una fuente pública de transacciones de pago en vivo, por lo que el flujo de eventos se simula a partir de un
dataset histórico. Ese dataset tiene que permitir construir features con significado de negocio, como la distancia
entre cliente y comercio o la velocidad entre compras, para poder comprobar que las features calculadas en streaming
son correctas.

## Opciones consideradas

| Opción | A favor | En contra |
|---|---|---|
| Sparkov (Credit Card Transactions) | Columnas interpretables: tarjeta, comercio, ubicación y fecha. Volumen suficiente (1,85 millones de transacciones en dos años) | Datos simulados, con patrones de fraude más simples que los reales |
| IEEE-CIS Fraud Detection | Datos reales y con problemas de calidad realistas | Cientos de variables anonimizadas sin significado conocido, lo que impide validar las features. La información de identidad solo cubre parte de las transacciones |

## Decisión

Sparkov es la fuente principal del proyecto. IEEE-CIS queda como extensión opcional para probar la tubería con datos
más sucios.

## Consecuencias

- El contrato del evento de transacción se diseña a partir de los campos de Sparkov.
- Incorporar IEEE-CIS en el futuro exigirá un contrato de evento distinto y una transformación propia.
