"""
Replayer: reproduce el histórico de Sparkov en orden temporal y lo publica en Kafka.

    python src/replayer.py data/raw/fraudTest.csv --dry-run --limit 5
    python src/replayer.py data/raw/fraudTest.csv --speedup 0 --max-rate 500
"""

import argparse
import os
import sys
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pandas as pd
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import MessageField, SerializationContext

TOPIC = "transactions.raw"
SCHEMA_FILE = Path(__file__).resolve().parents[1] / "schemas" / "transaction.avsc"
FIELDS = ["trans_num", "event_time", "cc_num", "merchant", "category", "amt",
          "lat", "long", "merch_lat", "merch_long", "city_pop", "dob"]


def load_events(paths: list[str]) -> pd.DataFrame:
    df = pd.concat(pd.read_csv(p, dtype={"cc_num": str, "amt": str}) for p in paths)
    # Sparkov guarda hora local sin zona; por convención se interpreta como UTC en ambos caminos
    df["event_time"] = pd.to_datetime(df["trans_date_trans_time"], utc=True)
    df["dob"] = pd.to_datetime(df["dob"]).dt.date
    df["amt"] = df["amt"].map(Decimal)  # Avro decimal(12,2) necesita Decimal, no float
    df["merchant"] = df["merchant"].str.removeprefix("fraud_")  # Sparkov lo pone en todos los comercios
    # is_fraud no se publica: la etiqueta llega ~30 días después (ADR-0011)
    return df.sort_values(["event_time", "trans_num"])[FIELDS]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", nargs="+", help="CSV de Sparkov")
    parser.add_argument("--speedup", type=float, default=3600, help="3600 = 1 h de datos por segundo; 0 = sin esperas")
    parser.add_argument("--max-rate", type=float, default=0, help="Tope de eventos por segundo; 0 = sin tope")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true",
                        help="Valida e imprime los eventos en vez de publicarlos (no necesita Kafka)")
    args = parser.parse_args()

    events = load_events(args.csv)
    if args.limit is not None:
        events = events.head(args.limit)
    if events.empty:
        print("0 eventos")
        return
    print(f"{len(events):,} eventos, {events.event_time.min()} -> {events.event_time.max()}")

    # En dry-run el registro es simulado: los eventos se validan contra el esquema igual que al publicar
    registry_url = "mock://dry-run" if args.dry_run else os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:8081")
    serialize = AvroSerializer(SchemaRegistryClient.new_client({"url": registry_url}),
                               SCHEMA_FILE.read_text(encoding="utf-8"))
    ctx = SerializationContext(TOPIC, MessageField.VALUE)

    producer = None
    if not args.dry_run:
        producer = Producer({
            "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            "enable.idempotence": True,  # sin duplicados por reintentos, implica acks=all
        })
    failed = 0

    def on_delivery(err, _msg):
        nonlocal failed
        if err is not None:
            if not failed:
                print(f"Error de entrega: {err}")
            failed += 1

    def wait(seconds: float) -> None:
        # Mientras espera, el productor sigue atendiendo las confirmaciones del broker
        if producer:
            producer.poll(seconds)
        else:
            time.sleep(seconds)

    start_wall = time.monotonic()
    start_event = events.event_time.iloc[0]
    sent = invalid = 0
    try:
        for event in events.itertuples(index=False):
            event = event._asdict()

            # Hora a la que debe salir este evento, medida desde el inicio (así los retrasos no se acumulan)
            target = start_wall
            if args.speedup:
                target += (event["event_time"] - start_event).total_seconds() / args.speedup
            if args.max_rate:
                target = max(target, start_wall + sent / args.max_rate)
            while (remaining := target - time.monotonic()) > 0:
                wait(remaining)

            event["produced_at"] = datetime.now(timezone.utc)
            try:
                value = serialize(event, ctx)
            except (ValueError, TypeError) as e:  # no cumple el esquema: no se publica
                invalid += 1
                print(f"Evento inválido {event['trans_num']}: {e}")
                continue

            if args.dry_run:
                print(event)
            else:
                while True:
                    try:
                        # Clave = cc_num: misma tarjeta → misma partición → orden garantizado (ADR-0004)
                        producer.produce(TOPIC, key=event["cc_num"], value=value, on_delivery=on_delivery)
                        break
                    except BufferError:  # cola local llena: esperar a que el broker confirme
                        producer.poll(1)
                producer.poll(0)

            sent += 1
            if sent % 10_000 == 0:
                print(f"{sent:,} enviados | event_time={event['event_time']}")
    except KeyboardInterrupt:
        print("Interrumpido")
    finally:
        if producer:
            failed += producer.flush(30)  # mensajes que no llegaron a confirmarse
        print(f"{sent:,} enviados, {failed} fallidos, {invalid} inválidos")


if __name__ == "__main__":
    main()
