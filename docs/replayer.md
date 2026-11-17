# Replayer

`src/replayer.py` lee los CSV de Sparkov, los ordena por fecha y publica cada transacción en el topic
`transactions.raw` de Kafka, comprimiendo el tiempo para simular tráfico en vivo.

## Qué publica

Cada evento sigue `schemas/transaction.avsc` (Avro, subject `transactions.raw-value`):

- `trans_num`, `cc_num`, `merchant`, `category`, `amt`, `lat`, `long`, `merch_lat`, `merch_long`, `city_pop`, `dob`
- `event_time`: `trans_date_trans_time`. Sparkov guarda hora local sin zona; por convención se interpreta como UTC,
  igual que en el camino batch, para que las features de hora y día coincidan
- `produced_at`: hora real de publicación, para medir latencia

No publica `is_fraud` ([ADR-0011](decisions/es/0011-etiquetas-fuera-del-stream.md)) ni datos personales (`first`, `last`,
`gender`, `street`, `city`, `state`, `zip`, `job`). Al comercio se le quita el prefijo `fraud_` que Sparkov pone a todos.

La clave del mensaje es `cc_num`, así las transacciones de una tarjeta llegan en orden ([ADR-0004](decisions/es/0004-clave-particion-cc-num.md)).

Si un evento no cumple el esquema, no se publica: se informa con su `trans_num`, se cuenta como inválido y el replayer
sigue con el siguiente. Al terminar muestra el total de enviados, fallidos (no confirmados por Kafka) e inválidos.

## Uso

Los ejemplos usan rutas relativas a la raíz del repositorio; el esquema se localiza solo, así que el script
funciona desde cualquier directorio.

```powershell
pip install -r requirements-dev.txt

# Validar y ver los eventos sin Kafka
python src/replayer.py data/raw/fraudTest.csv --dry-run --limit 5

# Publicar: 1 hora de datos por segundo
python src/replayer.py data/raw/fraudTest.csv --speedup 3600

# Carga fija de 500 eventos/s
python src/replayer.py data/raw/fraudTest.csv --speedup 0 --max-rate 500

python -m pytest tests -q
```

| Opción | Por defecto | |
|---|---|---|
| `--speedup` | 3600 | Aceleración del tiempo; `0` = sin esperas |
| `--max-rate` | 0 | Tope de eventos/s; `0` = sin tope |
| `--limit` | — | Enviar solo los primeros N eventos (`0` = ninguno) |
| `--dry-run` | — | Validar contra el esquema e imprimir en vez de publicar; no necesita Kafka ni Schema Registry |

La conexión se toma de `KAFKA_BOOTSTRAP_SERVERS` (por defecto `localhost:9092`) y `SCHEMA_REGISTRY_URL`
(por defecto `http://localhost:8081`). El topic `transactions.raw` debe existir antes de ejecutar.
