import json
import boto3
from datetime import datetime, timezone


TABLE_NAME = "security-alert-incidents"
DEDUP_WINDOW_MINUTES = 5

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    for record in event.get("Records", []):

        # SNS message
        message = record["Sns"]["Message"]

        # Convert JSON message to dictionary
        alert = json.loads(message)

        # Common alert fields
        timestamp = alert.get("timestamp")
        source = alert.get("source", "Unknown")
        severity = alert.get("severity", "UNKNOWN")
        resource = alert.get("affected_resource", "Unknown")
        description = alert.get("description", "")

        # Category used for deduplication
        category = alert.get(
            "category",
            "SuspiciousActivity"
        )

        # Stage 4 - raw alert measurement
        print(
            f"RAW_ALERT_RECEIVED | "
            f"source={source} | "
            f"timestamp={timestamp} | "
            f"resource={resource} | "
            f"category={category}"
        )

        # Stage 5 - false-merge safeguard
        #
        # Include an event signature so that two
        # genuinely different incidents affecting the
        # same resource can remain separate.

        event_signature = alert.get("event_signature")

        # Backward-compatible fallback
        if not event_signature:
            event_signature = description.strip().lower()

        event_signature = str(
            event_signature
        ).strip().lower()

        # Improved incident key
        incident_key = (
            f"{resource}|"
            f"{category}|"
            f"{event_signature}"
        )

        # Convert timestamp
        try:
            alert_time = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
        except Exception:
            alert_time = datetime.now(timezone.utc)

        # Check existing incident
        response = table.get_item(
            Key={
                "incident_key": incident_key
            }
        )

        existing = response.get("Item")

        # Existing incident found
        if existing:

            last_seen = datetime.fromisoformat(
                existing["last_seen"].replace(
                    "Z",
                    "+00:00"
                )
            )

            time_difference = abs(
                (
                    alert_time - last_seen
                ).total_seconds()
            )

            if (
                time_difference
                <= DEDUP_WINDOW_MINUTES * 60
            ):

                # Add source if it is new
                sources = set(
                    existing.get(
                        "sources",
                        []
                    )
                )

                sources.add(source)

                new_alert_count = (
                    int(
                        existing.get(
                            "alert_count",
                            1
                        )
                    ) + 1
                )

                # Update existing incident
                table.update_item(
                    Key={
                        "incident_key": incident_key
                    },
                    UpdateExpression="""
                        SET last_seen = :last_seen,
                            #sev = :severity,
                            #desc = :description,
                            sources = :sources,
                            alert_count = :count
                    """,
                    ExpressionAttributeNames={
                        "#sev": "severity",
                        "#desc": "description"
                    },
                    ExpressionAttributeValues={
                        ":last_seen":
                            alert_time.isoformat(),
                        ":severity":
                            severity,
                        ":description":
                            description,
                        ":sources":
                            list(sources),
                        ":count":
                            new_alert_count
                    }
                )

                print(
                    f"DEDUPLICATED | "
                    f"source={source} | "
                    f"incident={incident_key} | "
                    f"event_signature="
                    f"{event_signature} | "
                    f"alert_count="
                    f"{new_alert_count} | "
                    f"time_difference_seconds="
                    f"{time_difference}"
                )

                continue

        # No matching incident - create new incident
        incident_id = (
            "INC-"
            + incident_key.replace(
                "|",
                "-"
            )
        )

        table.put_item(
            Item={
                "incident_key":
                    incident_key,
                "incident_id":
                    incident_id,
                "first_seen":
                    alert_time.isoformat(),
                "last_seen":
                    alert_time.isoformat(),
                "source":
                    source,
                "sources":
                    [source],
                "severity":
                    severity,
                "affected_resource":
                    resource,
                "category":
                    category,
                "event_signature":
                    event_signature,
                "description":
                    description,
                "status":
                    "OPEN",
                "alert_count":
                    1
            }
        )

        print(
            f"NEW_INCIDENT_CREATED | "
            f"source={source} | "
            f"incident={incident_key} | "
            f"event_signature="
            f"{event_signature} | "
            f"alert_count=1"
        )

    return {
        "statusCode": 200,
        "body": json.dumps(
            "Deduplication completed"
        )
    }
