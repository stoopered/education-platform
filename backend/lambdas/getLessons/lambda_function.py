"""getLessons Lambda

This function returns today’s lessons for a given student.  In a real
application the function would read the studentId from the request context,
look up the student’s grade in DynamoDB, check the Plano ISD calendar and
retrieve the appropriate lesson content from another DynamoDB table or S3.

For this skeleton implementation we simply return a hard‑coded lesson.

Expected event (API Gateway v2 format):
{
  "queryStringParameters": {"grade": "K"}
}

Returns:
  200 response with JSON body containing lesson title and description.
"""
import json
from datetime import datetime


def lambda_handler(event, context):
    grade = None
    # Extract grade from query string or default to Kindergarten
    if event.get("queryStringParameters"):
        grade = event["queryStringParameters"].get("grade")
    grade = grade or "K"

    # Determine date; in a real implementation consider America/Chicago timezone
    today = datetime.utcnow().strftime("%Y-%m-%d")

    lesson = {
        "title": f"Sample {grade} Lesson for {today}",
        "description": "This is a placeholder lesson. Implement logic to fetch real content.",
        "content": {
            "subject": "Math",
            "question": "What is 2 + 2?",
            "options": ["3", "4", "5"],
        },
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(lesson),
    }