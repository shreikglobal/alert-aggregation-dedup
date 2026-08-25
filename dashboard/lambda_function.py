import boto3
import html


TABLE_NAME = "security-alert-incidents"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    # Read incidents from DynamoDB
    response = table.scan()

    incidents = [
        item
        for item in response.get("Items", [])
        if item.get("status", "").upper() == "OPEN"
    ]

    rows = ""

    for item in incidents:

        incident_id = html.escape(
            str(item.get("incident_id", "N/A"))
        )

        sources = item.get("sources", [])

        if not sources:
            source_text = item.get(
                "source",
                "Unknown"
            )
        else:
            source_text = ", ".join(
                str(source)
                for source in sources
            )

        source_text = html.escape(
            source_text
        )

        severity = html.escape(
            str(
                item.get(
                    "severity",
                    "UNKNOWN"
                )
            )
        )

        resource = html.escape(
            str(
                item.get(
                    "affected_resource",
                    "Unknown"
                )
            )
        )

        status = html.escape(
            str(
                item.get(
                    "status",
                    "UNKNOWN"
                )
            )
        )

        description = html.escape(
            str(
                item.get(
                    "description",
                    ""
                )
            )
        )

        alert_count = html.escape(
            str(
                item.get(
                    "alert_count",
                    "1"
                )
            )
        )

        rows += f"""
        <tr>
            <td><strong>{incident_id}</strong></td>
            <td>{source_text}</td>
            <td>{severity}</td>
            <td>{resource}</td>
            <td>{status}</td>
            <td>{alert_count}</td>
            <td>{description}</td>
        </tr>
        """

    if not rows:

        rows = """
        <tr>
            <td colspan="7">
                No open incidents found.
            </td>
        </tr>
        """

    html_page = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <meta
            http-equiv="refresh"
            content="15"
        >

        <title>
            Security Alert Dashboard
        </title>

        <style>

            body {{
                font-family:
                    Arial,
                    sans-serif;

                margin: 0;

                background:
                    #f4f6f8;

                color:
                    #222;
            }}

            .header {{

                background:
                    #172b3a;

                color:
                    white;

                padding:
                    24px 40px;
            }}

            .header h1 {{

                margin: 0;

                font-size:
                    28px;
            }}

            .header p {{

                margin:
                    8px 0 0;

                opacity:
                    0.85;
            }}

            .container {{

                padding:
                    30px 40px;
            }}

            .card {{

                background:
                    white;

                border-radius:
                    10px;

                padding:
                    24px;

                box-shadow:
                    0 2px 8px
                    rgba(0,0,0,0.08);
            }}

            table {{

                width:
                    100%;

                border-collapse:
                    collapse;

                margin-top:
                    15px;
            }}

            th,
            td {{

                padding:
                    14px;

                border-bottom:
                    1px solid #ddd;

                text-align:
                    left;

                vertical-align:
                    top;
            }}

            th {{

                background:
                    #eef2f5;
            }}

            .summary {{

                margin-bottom:
                    20px;

                font-size:
                    18px;
            }}

            .footer {{

                margin-top:
                    20px;

                color:
                    #666;

                font-size:
                    13px;
            }}

        </style>

    </head>

    <body>

        <div class="header">

            <h1>
                Central Security Alert Dashboard
            </h1>

            <p>
                Centralised Security Alert
                Aggregation and Deduplication
            </p>

        </div>


        <div class="container">

            <div class="card">

                <div class="summary">

                    <strong>
                        Open Incidents:
                    </strong>

                    {len(incidents)}

                </div>


                <table>

                    <thead>

                        <tr>

                            <th>
                                Incident
                            </th>

                            <th>
                                Contributing Source(s)
                            </th>

                            <th>
                                Severity
                            </th>

                            <th>
                                Affected Resource
                            </th>

                            <th>
                                Status
                            </th>

                            <th>
                                Alert Count
                            </th>

                            <th>
                                Description
                            </th>

                        </tr>

                    </thead>


                    <tbody>

                        {rows}

                    </tbody>

                </table>


                <div class="footer">

                    Dashboard refreshes
                    automatically every
                    15 seconds.

                </div>

            </div>

        </div>

    </body>

    </html>
    """


    return {

        "statusCode":
            200,

        "headers": {

            "Content-Type":
                "text/html"

        },

        "body":
            html_page

    }
