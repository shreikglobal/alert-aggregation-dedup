# Deduplication

## Purpose

The deduplication layer prevents multiple alerts representing the same underlying incident from being treated as separate incidents.

The deduplication engine is implemented using AWS Lambda and Amazon DynamoDB.

## Deduplication Rule

The initial correlation rule uses:

```text
Affected Resource
+
Alert Category
+
Time Window

The configured deduplication window is:

5 minutes

When an alert matches an existing incident within the configured time window, the existing incident is updated instead of creating another incident.

Incident Store

Deduplication state is stored in the DynamoDB table:

security-alert-incidents

The table uses:

incident_key

as its partition key.

Incident records maintain information such as:

Incident ID
First seen time
Last seen time
Source
Contributing sources
Severity
Affected resource
Category
Description
Status
Alert count
Deduplication Flow
Incoming Alert
      |
      v
Create Incident Key
      |
      v
Check DynamoDB
      |
      +-------------------+
      |                   |
 Existing Incident     No Match
      |                   |
      v                   v
Check Time Window     Create Incident
      |
      +-------------------+
      |
 Within 5 Minutes
      |
      v
Update Existing Incident
Multi-Source Correlation

When two detection sources report the same underlying condition within the configured window, the incident is updated with the additional contributing source.

Example:

GuardDuty Alert
      |
      v
INC-001
      ^
      |
CloudTrail Alert

The incident can therefore contain:

Sources:
GuardDuty
CloudTrail

instead of creating two unrelated incidents.

False-Merge Risk

A simple resource-plus-category key can incorrectly merge genuinely different incidents when:

The affected resource is the same
The category is the same
The alerts occur within the deduplication window
The underlying activities are actually different

For example:

EC2-01 + SuspiciousActivity + Port Scanning

and

EC2-01 + SuspiciousActivity + IAM Change

could be incorrectly treated as one incident by a simpler key.

False-Merge Safeguard

The deduplication key was strengthened by adding an event signature:

Affected Resource
+
Alert Category
+
Event Signature

The resulting incident key is:

resource|category|event_signature

This provides a more specific identity for an incident.

Example
TEST-RESOURCE
+
SuspiciousActivity
+
port-scanning

and

TEST-RESOURCE
+
SuspiciousActivity
+
iam-change

produce different incident keys and therefore remain separate.

Stage 4 Measurement

The Lambda records every incoming alert using the log marker:

RAW_ALERT_RECEIVED

This provides a way to count raw alerts during a defined test period.

The noise reduction calculation is:

Noise Reduction %
=
(Raw Alerts - Deduplicated Incidents)
/
Raw Alerts
× 100

The test should record:

Test duration
GuardDuty raw alerts
CloudTrail raw alerts
Total raw alerts
Deduplicated incidents
Alerts removed
Noise reduction percentage
Stage 5 Validation

The false-merge safeguard is validated by creating two alerts that:

Affect the same resource
Use the same category
Occur close together
Have different event signatures

Expected result:

Different Event Signature
          |
          v
Different Incident

This demonstrates that genuinely different incidents remain separate after the safeguard is applied.
