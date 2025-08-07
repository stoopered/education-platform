"""A lightweight Flask server that routes HTTP requests to our Lambda
functions for local and containerised development.

This app allows you to run the backend entirely within a Docker
container without relying on `sam local start-api`.  Each route
constructs a minimal event dict (similar to API Gateway v2) and
delegates to the corresponding Lambda handler.  The response body
returned by the Lambda is parsed and returned as JSON with the
appropriate HTTP status code.

To run locally:

    python app.py

This will start the server on port 3001 by default.
"""
from __future__ import annotations
import os
import json
from flask import Flask, request, jsonify

# Import Lambda handlers
"""Flask application to route HTTP requests to our Lambda functions.

When running inside a Docker container we copy the contents of
``education-platform/backend`` into the image root.  In that
environment the `lambdas` package lives directly under the working
directory rather than under a ``backend`` namespace.  To make the
imports work in both scenarios (local development from the repository
root and packaged container execution) we attempt to import the
handlers from two possible locations: first under the ``backend``
namespace, then from the top‑level ``lambdas`` package.  The first
successful import wins.
"""

from importlib import import_module


def _resolve_handler(module_path: str, fallback_path: str, attr: str):
    """Attempt to import a Lambda handler from two possible module paths.

    When running ``python app.py`` from the ``backend`` directory the
    modules live under ``lambdas``; when invoked from the repository
    root (e.g. via ``sam local start-api``) they live under
    ``backend.lambdas``.  This helper tries both and returns the
    requested attribute.

    Args:
        module_path: Primary module path to import (e.g. 'backend.lambdas.getLessons.lambda_function').
        fallback_path: Secondary module path to import if the first fails (e.g. 'lambdas.getLessons.lambda_function').
        attr: Name of the attribute to retrieve from the imported module (typically 'lambda_handler').
    Returns:
        The resolved attribute.
    Raises:
        ImportError: If neither module can be imported or the attribute is missing.
    """
    try:
        module = import_module(module_path)
    except ImportError:
        module = import_module(fallback_path)
    return getattr(module, attr)


# Resolve Lambda handlers lazily so import errors surface clearly
get_lessons = _resolve_handler(
    "backend.lambdas.getLessons.lambda_function",
    "lambdas.getLessons.lambda_function",
    "lambda_handler",
)
ai_tutor = _resolve_handler(
    "backend.lambdas.aiTutor.lambda_function",
    "lambdas.aiTutor.lambda_function",
    "lambda_handler",
)
submit_answer = _resolve_handler(
    "backend.lambdas.submitAnswer.lambda_function",
    "lambdas.submitAnswer.lambda_function",
    "lambda_handler",
)
generate_report = _resolve_handler(
    "backend.lambdas.generateReport.lambda_function",
    "lambdas.generateReport.lambda_function",
    "lambda_handler",
)
get_calendar = _resolve_handler(
    "backend.lambdas.getCalendar.lambda_function",
    "lambdas.getCalendar.lambda_function",
    "lambda_handler",
)
get_learning_style = _resolve_handler(
    "backend.lambdas.getLearningStyle.lambda_function",
    "lambdas.getLearningStyle.lambda_function",
    "lambda_handler",
)

from flask_cors import CORS

app = Flask(__name__)

# Enable Cross‑Origin Resource Sharing (CORS) so the frontend running on
# a different port/domain can call the backend without browser errors.
# In production you should restrict the allowed origins via the
# ``CORS_ORIGINS`` environment variable.  Here we allow all origins by
# default for local development.
CORS(app, resources={r"/*": {"origins": os.environ.get("CORS_ORIGINS", "*")}})


def call_lambda(handler, event):
    """Call a Lambda handler and unpack the response into status, headers, body."""
    result = handler(event, None)  # context is unused in our functions
    status = result.get("statusCode", 200)
    body = result.get("body", "{}")
    try:
        json_body = json.loads(body)
    except json.JSONDecodeError:
        json_body = {"message": body}
    return status, json_body


@app.route("/lessons", methods=["GET"])
def lessons_route():
    event = {"queryStringParameters": request.args.to_dict() or None}
    status, body = call_lambda(get_lessons, event)
    return jsonify(body), status


@app.route("/ai", methods=["POST"])
def ai_route():
    event = {"body": request.data.decode("utf-8")}
    status, body = call_lambda(ai_tutor, event)
    return jsonify(body), status


@app.route("/answer", methods=["POST"])
def answer_route():
    event = {"body": request.data.decode("utf-8")}
    status, body = call_lambda(submit_answer, event)
    return jsonify(body), status


@app.route("/report", methods=["POST"])
def report_route():
    event = {"body": request.data.decode("utf-8")}
    status, body = call_lambda(generate_report, event)
    return jsonify(body), status


@app.route("/calendar", methods=["GET"])
def calendar_route():
    event = {}
    status, body = call_lambda(get_calendar, event)
    return jsonify(body), status


@app.route("/learning-style", methods=["GET"])
def learning_style_route():
    # In a real implementation you might pass a studentId via query parameters
    event = {}
    status, body = call_lambda(get_learning_style, event)
    return jsonify(body), status


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3001))
    app.run(host="0.0.0.0", port=port)