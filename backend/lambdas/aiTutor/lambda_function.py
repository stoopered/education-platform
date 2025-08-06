"""aiTutor Lambda

This Lambda acts as an interface to an AI model (Amazon Bedrock or
OpenAI) that converses with the student.  It receives a prompt and
conversation history from the front‑end and returns the model’s
response.  The actual call to the model is controlled via an
environment variable `AI_PROVIDER`.  Supported values are `bedrock`
and `openai`.

In this example, the code shows how you might integrate with the
respective SDKs.  It falls back to a canned response if no provider
configuration is set.
"""
import json
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    import boto3
except ImportError:
    boto3 = None

try:
    import openai
except ImportError:
    openai = None


def invoke_bedrock(prompt: str) -> str:
    """Invoke an Anthropic Claude model via Amazon Bedrock.

    The AWS Bedrock runtime client requires the name of the model (e.g.
    `anthropic.claude-v2`), the content, and optionally a maximum token
    count.  See AWS documentation for details.
    """
    if not boto3:
        logger.warning("boto3 not available; returning fallback response")
        return "I'm sorry, I'm unable to provide a response right now."
    client = boto3.client("bedrock-runtime")
    model_id = os.environ.get("BEDROCK_MODEL", "anthropic.claude-instant-v1")
    payload = {
        "prompt": prompt,
        "max_tokens_to_sample": 256,
        "temperature": 0.7,
        "top_k": 250,
        "top_p": 0.95,
    }
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(payload).encode("utf-8"),
        contentType="application/json",
    )
    response_body = json.loads(response["body"].read().decode("utf-8"))
    return response_body.get("completion", "")


def invoke_openai(prompt: str) -> str:
    """Invoke an OpenAI ChatCompletion model.

    Requires the OPENAI_API_KEY environment variable.  Adjust the
    model name (`gpt-3.5-turbo`) as needed.
    """
    if not openai:
        logger.warning("openai module not available; returning fallback response")
        return "I'm sorry, I'm unable to provide a response right now."
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    messages = [
        {"role": "system", "content": "You are a friendly and patient teacher for children."},
        {"role": "user", "content": prompt},
    ]
    try:
        completion = openai.ChatCompletion.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=messages,
            temperature=0.7,
            max_tokens=256,
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        logger.error("OpenAI call failed: %s", e)
        return "I'm sorry, I couldn't think of an answer."


def lambda_handler(event, context):
    """
    Main handler for the AI tutor.  Expects a JSON body with fields:

    * grade: grade level of the student (e.g. "K" or "3").
    * subject: subject of the lesson (Math, Reading or Science).
    * question: text of the question asked.
    * studentAnswer: answer provided by the student.
    * correctAnswer: correct answer for the question.
    * explanation: (optional) short explanation of the correct answer.

    The handler constructs a prompt for the AI model tailored to the
    student's grade and subject.  It then invokes either Amazon
    Bedrock or OpenAI depending on the AI_PROVIDER environment
    variable.  If neither provider is configured or SDKs are
    unavailable it falls back to a simple deterministic response.
    """
    # Safely parse the request body
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Invalid JSON"}),
        }
    # Extract required fields
    grade = body.get("grade")
    subject = body.get("subject")
    question = body.get("question")
    student_answer = body.get("studentAnswer")
    correct_answer = body.get("correctAnswer")
    explanation = body.get("explanation", "")
    # Compose a prompt for the model
    prompt_text = (
        f"You are a friendly and patient teacher for a {grade}-grade student. "
        f"The student is learning {subject}. They were asked: '{question}'. "
        f"They answered: '{student_answer}'. "
        f"The correct answer is: '{correct_answer}'. "
        "Please provide feedback: if the student's answer is correct, praise "
        "them and briefly explain why. If it is incorrect, gently explain the correct "
        "answer and encourage the student to keep trying. Keep the language simple and age-appropriate."
    )
    provider = os.environ.get("AI_PROVIDER", "none").lower()
    logger.info("Invoking AI provider %s", provider)
    response_text = None
    # Invoke the selected provider
    if provider == "bedrock":
        try:
            response_text = invoke_bedrock(prompt_text)
        except Exception as e:
            logger.error("Error invoking Bedrock: %s", e)
            response_text = None
    elif provider == "openai":
        try:
            response_text = invoke_openai(prompt_text)
        except Exception as e:
            logger.error("Error invoking OpenAI: %s", e)
            response_text = None
    # Fallback if no provider or call failed
    if not response_text:
        # Basic deterministic feedback without AI
        if student_answer == correct_answer:
            response_text = (
                f"Great job! '{student_answer}' is correct. {explanation} Keep up the good work!"
            )
        else:
            response_text = (
                f"Good try! The correct answer is '{correct_answer}'. {explanation} You'll get it next time!"
            )
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"response": response_text}),
    }