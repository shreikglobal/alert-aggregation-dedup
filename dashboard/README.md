# Dashboard — Single-Pane Security View

## Purpose

The dashboard provides a simple single-pane view of current open security incidents.

It reads incident information from the central DynamoDB incident store and presents the information through an AWS Lambda Function URL.

## Dashboard Flow

```text
DynamoDB
security-alert-incidents
        |
        v
Dashboard Lambda
        |
        v
Lambda Function URL
        |
        v
Web Browser
Information Displayed

Each open incident is presented with:

Incident ID
Contributing source(s)
Severity
Affected resource
Status
Alert count
Description

This provides a single location for reviewing the current incident state.

Multi-Source Incident View

When an existing incident receives a corroborating alert from another detection source, the dashboard reflects the additional contributing source on the same incident.

Example:

Incident:
INC-001

Sources:
GuardDuty
CloudTrail

Severity:
HIGH

Status:
OPEN

Alert Count:
2

The second source is therefore represented as part of the existing incident rather than appearing as a separate duplicate incident.

Automatic Refresh

The dashboard is configured to refresh automatically every 15 seconds.

This allows newly updated incident information to become visible without manually refreshing the browser.

Function URL

The dashboard is exposed through an AWS Lambda Function URL so that the generated HTML interface can be accessed through a browser.

Dashboard Outcome

The dashboard provides:

A central view of open incidents
Visibility into contributing detection sources
Incident severity
Incident status
Affected resource information
Alert count
Incident descriptions

This satisfies the single-pane dashboard requirement of the project.
