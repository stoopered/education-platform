"""submitAnswer Lambda

Receives a student's answer and records it.  In production this Lambda
would write a new item to a DynamoDB table with the studentId, questionId,
answer given, whether it was correct and the time taken.  It might also
call an AI model to generate feedback or hints.

Expected event body (JSON):
{
  "studentId": "abc123",
  "questionId": "Q1",
  "answer": "4",
  "correct": true
}

Returns a confirmation message.
"""
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Invalid JSON"}),
        }

    logger.info("Received answer: %s", body)
    # TODO: Insert into DynamoDB table
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Answer recorded"}),
    }