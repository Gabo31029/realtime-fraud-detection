# Real-Time Fraud Detector

Detects fraudulent transactions as they happen. Events are ingested from a
stream, cleaned and enriched in flight, then scored by an ML model that flags
suspicious activity in near real time.

The focus is on the pipeline: low-latency ingestion, strong data-quality
guarantees, and feature consistency between training and serving.

> Early development. Architecture and stack are still being decided.

## Status

- [ ] Event source / producer
- [ ] Stream ingestion
- [ ] Processing & feature engineering
- [ ] Model training
- [ ] Real-time scoring
- [ ] Monitoring

## About

Built by Gabriel (data engineering - streaming and pipelines) and Alain
(data scientist - modeling).