"""getLearningStyle Lambda

Returns the current learning‑style profile for a student.  It would
normally compute this from historical answer data and update the
DynamoDB profile.  Here we return a dummy profile.
"""
import json


def lambda_handler(event, context):
    student_id = None
    if event.get("queryStringParameters"):
        student_id = event["queryStringParameters"].get("studentId")
    student_id = student_id or "unknown"
    profile = {
        "studentId": student_id,
        "preferredModalities": ["visual", "hands-on"],
        "accuracy": 0.85,
        "averageTimeSeconds": 12,
    }
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(profile),
    }