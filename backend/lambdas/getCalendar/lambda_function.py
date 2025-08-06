"""getCalendar Lambda

Returns a portion of the Plano ISD school calendar.  The real function
would read a JSON or CSV file from S3 and filter events for the
requested date range.
"""
import json
from datetime import datetime


SAMPLE_CALENDAR = [
    {"date": "2025-08-18", "event": "First day of school", "isSchoolDay": True},
    {"date": "2025-09-02", "event": "Labor Day", "isSchoolDay": False},
    {"date": "2025-12-20", "event": "Winter break begins", "isSchoolDay": False},
]


def lambda_handler(event, context):
    # In a real implementation you might pass startDate/endDate as query parameters
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"calendar": SAMPLE_CALENDAR}),
    }