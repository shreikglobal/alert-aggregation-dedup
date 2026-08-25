# Centralised Security Alert Aggregation and Deduplication

## Project Overview

This project implements a centralised security alert aggregation and deduplication workflow using AWS services.

The objective is to collect alerts from multiple detection sources into a common alert intake, normalise them into a consistent format, deduplicate related alerts into a single incident, provide a single-pane dashboard, measure alert noise, and reduce the risk of false merges.

## Project Goal

The project uses at least two detection sources:

- Amazon GuardDuty
- AWS CloudTrail-based detection rules

Both sources send alerts to a common central alert destination.

The alerts are then processed by a deduplication engine and stored as incidents for dashboard viewing.

## Architecture

```text
GuardDuty
    |
    v
EventBridge
    |
    v
Input Transformer
    |
    v
SNS: central-security-alerts
    |
    v
Deduplication Lambda
    |
    v
DynamoDB
security-alert-incidents
    |
    v
Dashboard Lambda
    |
    v
Lambda Function URL
