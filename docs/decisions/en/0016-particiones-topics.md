<p align="right">
  <a href="../es/0016-particiones-topics.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0016: Number of topic partitions

| Status | Date |
|---|---|
| Accepted | 2026-11-17 |

## Context

A topic's partition count sets the maximum consumer parallelism: each partition is read by a single consumer in the
group ([ADR-0004](0004-clave-particion-cc-num.md)). Also, a message's partition is computed as the hash of its key
modulo the partition count, so changing that count later moves cards from one partition to another and temporarily
breaks per-card ordering. It should be chosen well from the start.

### Measured data

Over the full Sparkov dataset (`fraudTrain.csv` and `fraudTest.csv`):

| Measure | Value |
|---|---|
| Transactions | 1,852,394, from January 2019 to December 2020 |
| Distinct cards | 999 |
| Distinct merchants | 693 |
| Transactions per hour of data | Mean 106, 99th percentile 306, maximum 362 |
| Most active card | 4,392 transactions (0.24 % of the total) |
| Message size in `transactions.raw` (Avro value and key) | Mean 151 bytes, maximum 181 |

At the replayer's default speed (`--speedup 3600`, one hour of data per second), the mean rate is 106 events per
second, with peaks of 362. The sustained throughput requirement is 500 events per second, reached with
`--max-rate 500`.

### Estimates

- **Design load:** 500 events per second with a 2x margin for peaks and reprocessing: 1,000 events per second.
- **Kafka volume:** 1,000 events per second of 151 bytes is about 150 KB/s. A Kafka partition handles several MB/s, so
  the broker is not the limit.
- **Consumer capacity:** estimated at about 200 events per second per instance. This is a conservative figure for a
  Python consumer ([ADR-0005](0005-consumidor-python.md)) that batches Redis reads, runs the model in memory
  ([ADR-0009](0009-modelo-embebido-consumidor.md)) and writes to PostgreSQL. **It has not been measured**: the
  consumer does not exist yet.
- **Partitions needed:** 1,000 / 200 = 5 consumers in parallel, and therefore at least 5 partitions.

### Card distribution

The `confluent-kafka` producer (librdkafka) assigns the partition with the CRC32 of the key. Applied to the 999 cards:

| Partitions | Cards per partition | Events in the busiest partition relative to the mean |
|---|---|---|
| 3 | Between 326 and 344 | 1.06 |
| 6 | Between 149 and 185 | 1.10 |
| 12 | Between 67 and 99 | 1.18 |

No card carries enough traffic to unbalance a partition.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| 3 partitions | Most even distribution. One per broker on MSK | At most 3 consumers: about 600 events per second estimated, below the design load |
| 6 partitions | Covers the design load with margin. Splits evenly across 1, 2, 3 and 6 consumers. Two partitions per broker on MSK | Slightly more imbalance than with 3 (10 %) |
| 12 partitions | More room to grow | 18 % imbalance. More files and connections on the broker without the load requiring it |
| One partition per card | Full isolation per card | Does not scale: new cards appear every day and thousands of partitions degrade the broker. Useful parallelism is bounded by the number of consumers, not of cards |

## Decision

| Topic | Partitions | Reason |
|---|---|---|
| `transactions.raw` | 6 | Covers the design load (5 consumers) with margin and spreads evenly across the 3 MSK brokers |
| `transactions.scored` | 6 | Same key and same count as `transactions.raw`: a card's decision lands in the partition matching its transaction (co-partitioning), so both topics can be joined per card without reshuffling data |
| `transactions.dlq` | 1 | Receives a tiny fraction of the traffic, needs no per-card ordering and is not consumed in parallel |

## Consequences

- Up to 6 consumers can run in parallel without changing the topics. Locally one is enough, reading all 6 partitions.
- The estimate of 200 events per second per consumer must be validated once the consumer exists, by publishing with
  the replayer at increasing `--max-rate`. If real capacity is below about 170 events per second, 6 consumers do not
  cover the design load and this decision must be revisited before any data depends on the current distribution.
- All producers must use the same partitioner. The Kafka Java client (and Kafka Connect) uses murmur2 instead of
  CRC32: a Java producer would send the same card to a different partition. If one is added, both must be configured
  with the same algorithm.
- Storage is not a constraint: the full dataset takes about 280 MB per replica in `transactions.raw`.
