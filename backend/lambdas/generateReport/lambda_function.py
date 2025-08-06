"""generateReport Lambda

Generates a PDF report of a student's performance for a given period.  In
production this function would query DynamoDB for all answers within the
period, compute accuracy and mastery metrics, then use a library such as
WeasyPrint or ReportLab to generate a PDF.  The PDF would be uploaded
to S3 and an email sent to the parent via SES.

Input event example:
{
  "body": "{\"studentId\":\"abc123\", \"startDate\":\"2025-08-01\", \"endDate\":\"2025-08-07\"}"
}
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
    student_id = body.get("studentId")
    start_date = body.get("startDate")
    end_date = body.get("endDate")
    logger.info("Generating report for %s from %s to %s", student_id, start_date, end_date)
    # TODO: Query DynamoDB and generate PDF
    # TODO: Upload PDF to S3 and send an email via SES
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Report generation initiated"}),
    }