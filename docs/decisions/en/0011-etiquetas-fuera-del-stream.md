<p align="right">
  <a href="../es/0011-etiquetas-fuera-del-stream.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0011: Fraud labels outside the stream and delayed

| Status | Date |
|---|---|
| Accepted | 2026-10-05 |

## Context

In reality, fraud is confirmed weeks after the transaction, when the chargeback arrives. If the label travels with
the event, or is used before it would be available, training learns from information about the future.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Labels in a separate store, with an availability date | Reproduces the real delay and prevents information leakage | More logic when generating the training dataset |
| Label inside the event | Simple | Direct information leakage and does not reflect reality |

## Decision

The replayer removes the label before publishing. Labels are stored separately with an availability date 30 days after
the transaction, and the training dataset only uses those already available at the cut-off date.

## Consequences

- Retraining always works with a 30-day lag behind the most recent data.
- The time-based split between training and validation is defined by cut-off date and agreed with the data science team.
