<p align="right">
  <a href="../es/0001-dataset-sparkov.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-6e7781?style=for-the-badge" alt="Español"></a>
  <img src="https://img.shields.io/badge/English-1f6feb?style=for-the-badge" alt="English">
</p>

# ADR-0001: Sparkov dataset as the data source

| Status | Date |
|---|---|
| Accepted | 2026-10-05 |

## Context

There is no public source of live payment transactions, so the event stream is simulated from a historical dataset.
That dataset must allow building features with business meaning, such as the distance between customer and merchant or
the speed between purchases, so that the features computed in streaming can be verified.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| Sparkov (Credit Card Transactions) | Interpretable columns: card, merchant, location and date. Enough volume (1.85 million transactions over two years) | Simulated data, with simpler fraud patterns than real ones |
| IEEE-CIS Fraud Detection | Real data with realistic quality issues | Hundreds of anonymized variables with no known meaning, which makes the features impossible to validate. Identity information covers only part of the transactions |

## Decision

Sparkov is the project's main source. IEEE-CIS remains an optional extension to test the pipeline with dirtier data.

## Consequences

- The transaction event contract is designed from the Sparkov fields.
- Adding IEEE-CIS in the future will require a different event contract and its own transformation.
