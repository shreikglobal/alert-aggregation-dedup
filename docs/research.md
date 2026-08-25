# Research and Written Analysis

## 1. Alert Correlation vs Alert Deduplication

Alert correlation and alert deduplication are related but different concepts.

### Alert Correlation

Alert correlation connects multiple security alerts that may be related to the same underlying activity.

For example:

```text
GuardDuty Alert
       +
CloudTrail Alert
       |
       v
Potentially Related Activity

Correlation focuses on understanding relationships between alerts.

Alert Deduplication

Alert deduplication focuses on preventing repeated alerts for the same underlying incident from creating multiple incident records.

In this project, deduplication uses:

Affected Resource
+
Category
+
Event Signature
+
Time Window

to determine whether a new alert should update an existing incident or create a new one.

Key Difference
Correlation
    =
Find relationships between alerts

Deduplication
    =
Prevent duplicate incident records

A practical security monitoring system can use both concepts together.

2. In-House Aggregation vs SIEM/SOAR
In-House Aggregation

A lightweight in-house aggregation approach can be useful when:

The number of detection sources is limited
The alert volume is manageable
The organisation needs a focused workflow
The team wants control over the implementation
A complete SIEM/SOAR platform would be excessive for the requirement

The solution developed in this project is an example of a focused aggregation and deduplication workflow.

The architecture uses AWS-native services:

Detection Sources
       |
       v
EventBridge
       |
       v
SNS
       |
       v
Lambda
       |
       v
DynamoDB
       |
       v
Dashboard
SIEM

A SIEM provides broader security monitoring capabilities such as:

Centralised log collection
Search and analysis
Detection rules
Alert management
Investigation support
Reporting and monitoring

A SIEM becomes more appropriate when the organisation needs broad visibility across many systems and large volumes of security data.

SOAR

SOAR platforms focus more heavily on security orchestration and automated response.

They can support:

Automated investigation
Workflow orchestration
Response actions
Case management
Integration with multiple security tools
Comparison
Area	Lightweight Aggregation	SIEM	SOAR
Alert aggregation	Yes	Yes	Usually through integrations
Deduplication	Yes	Yes	Can support through workflows
Large-scale log analysis	Limited	Strong	Not the primary purpose
Investigation	Basic	Strong	Strong with automation
Automated response	Limited	Limited/varies	Strong
Complexity	Lower	Higher	Higher
Best fit	Focused use cases	Broad monitoring	Automated response
3. When the Lightweight Approach Becomes Insufficient

A lightweight aggregation system can become insufficient as the environment grows.

Examples include:

Increasing Alert Volume

A large number of alerts may require more advanced:

Correlation
Prioritisation
Search
Analytics
Retention
Increasing Number of Sources

If the environment grows from a few AWS sources to many:

Cloud platforms
Endpoints
Network devices
Identity systems
SaaS applications

a more comprehensive security platform may become appropriate.

Advanced Investigation Requirements

Security teams may require:

Historical event searching
Cross-source investigation
Threat intelligence enrichment
Advanced detection analytics
Investigation timelines

These requirements can exceed the scope of a simple aggregation workflow.

Automated Response

If the organisation requires automated actions such as:

Detect
  |
  v
Investigate
  |
  v
Contain
  |
  v
Remediate

then SOAR-style orchestration can provide capabilities beyond simple alert aggregation.

4. Why Deduplication Still Matters

Even when a SIEM or SOAR platform is used, duplicate-alert reduction remains useful.

Multiple security tools can report the same underlying activity.

Without effective deduplication:

One Incident
   |
   +-- GuardDuty Alert
   +-- CloudTrail Alert
   +-- Endpoint Alert
   +-- Network Alert

may appear as multiple separate items.

A good deduplication strategy reduces analyst noise while preserving genuinely different incidents.

5. False-Merge Risk

Deduplication must balance two risks:

Duplicate Creation

The same incident appears multiple times.

One Incident
    |
    +-- Alert A
    +-- Alert B

Without deduplication:

Incident A
Incident B
False Merge

Two different incidents are incorrectly combined.

Incident A
+
Incident B
      |
      v
Incorrectly treated as one incident

The project therefore strengthens the incident key using an event signature.

Resource
+
Category
+
Event Signature

This helps preserve genuinely different activities affecting the same resource.

6. Project Approach

The project follows a staged approach:

Stage 1
Central Alert Intake
        |
        v
Stage 2
Deduplication
        |
        v
Stage 3
Single-Pane Dashboard
        |
        v
Stage 4
Noise Measurement
        |
        v
Stage 5
False-Merge Safeguard

The staged approach provides evidence for both the functionality of the solution and the limitations that need to be considered when scaling the design.

7. Conclusion

A lightweight AWS-native alert aggregation and deduplication workflow can provide a practical solution for a focused security monitoring requirement.

The approach centralises alerts, reduces duplicate incident records, provides a simple dashboard, measures alert noise, and introduces a safeguard against false merges.

As the number of data sources, alert volume, investigation requirements, and automated response requirements increase, a broader SIEM/SOAR solution may become more appropriate.
