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
    """Return today’s lessons for the given grade.

    Reads lesson definitions from a JSON file bundled with the code
    (`backend/lessons/lessons.json`).  Lessons are organized by grade and
    subject.  To vary the content each day, the function computes the
    day‑of‑year and uses it as an index into the lesson list for each
    subject.  If the grade or subject is not found, a message is
    returned instead.
    """
    # Determine the student’s grade (default to Kindergarten)
    grade = None
    if event.get("queryStringParameters"):
        grade = event["queryStringParameters"].get("grade")
    grade = grade or "K"

    # Load lessons from the JSON file at invocation time.  Try multiple
    # locations so the function works when packaged on Lambda or run
    # locally.  The first match wins.
    import os
    lesson_file = None
    candidate_paths = [
        # When packaged, the file may be copied into the same directory as
        # the handler (e.g. via CodeUri packaging).
        os.path.join(os.path.dirname(__file__), "lessons.json"),
        # Fallback to the shared lessons directory in the repository.
        os.path.join(os.path.dirname(__file__), "..", "..", "lessons", "lessons.json"),
    ]
    for path in candidate_paths:
        if os.path.isfile(path):
            lesson_file = path
            break
    if not lesson_file:
        raise FileNotFoundError("lessons.json not found in expected locations")
    with open(lesson_file, "r", encoding="utf-8") as f:
        all_lessons = json.load(f)

    grade_lessons = all_lessons.get(grade)
    if not grade_lessons:
        return {
            "statusCode": 404,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": f"No lessons found for grade {grade}"}),
        }

    # Compute a deterministic index based on the current date.  Use
    # America/Chicago time zone in production.  Here we use UTC.
    day_of_year = datetime.utcnow().timetuple().tm_yday
    response_lessons = {}
    for subject, lessons_list in grade_lessons.items():
        if not lessons_list:
            continue
        index = day_of_year % len(lessons_list)
        response_lessons[subject] = lessons_list[index]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "grade": grade,
            "lessons": response_lessons,
        }),
    }