import json
from backend.lambdas.getLessons import lambda_function


def test_get_lessons_returns_default_grade():
    response = lambda_function.lambda_handler({}, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["title"].startswith("Sample K Lesson")