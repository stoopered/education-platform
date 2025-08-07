# Serverless AI‑Powered Learning Platform

This repository contains the code and infrastructure for a serverless learning platform designed for Kindergarten and 3rd Grade students.  The application delivers daily lessons in math, reading and science, adapts to each student’s learning style and provides detailed reports for parents and teachers.  It uses an entirely serverless architecture built on AWS to stay within the free tier whenever possible.

## Repository Structure

```
education-platform/
  frontend/            # React/Next.js front‑end (static site hosted on S3 + CloudFront)
  backend/
    lambdas/           # Individual Lambda functions for API endpoints
    tests/             # Unit tests for Lambda functions
    cdk_or_sam/        # Infrastructure code (if using CDK)
    schemas/           # JSON schemas for API requests and responses
  infra/
    template.yaml      # AWS SAM template defining serverless resources
    terraform/         # Terraform configuration for the same resources
  README.md            # This file
```

### Front‑End

The front‑end is a simple React application.  It communicates with AWS services using the Amplify JS SDK (Cognito for authentication, API Gateway for REST endpoints and S3 for storage).  You can scaffold a more complete application using [`create-react-app`](https://create-react-app.dev/) or Next.js.

To run the front‑end locally:

```bash
cd frontend
npm install
npm start
```

### Back‑End

The back‑end consists of several AWS Lambda functions written in Python.  Each Lambda handles a specific API endpoint:

* **getLessons** – Returns the current day’s lessons based on the student’s grade and the Plano ISD calendar.
* **submitAnswer** – Receives the student’s answer, records it in DynamoDB and optionally returns a hint or next question.
* **trackProgress** – A nightly job that analyses answers and updates each student’s learning‑style profile.
* **generateReport** – Generates PDF reports for parents/teachers and stores them in S3.
* **getCalendar** – Returns school calendar information from a JSON/CSV file in S3.
* **getLearningStyle** – Computes learning‑style signals from recent interactions.

To test a Lambda locally:

```bash
cd backend/lambdas/getLessons
sam local invoke --event event.json
```

### Infrastructure

The `infra` directory contains both a **SAM template** (`template.yaml`) and **Terraform configuration** (`terraform/main.tf`).  Either tool can be used to deploy the same infrastructure:

* **SAM** – Run `sam build` and `sam deploy --guided` from the repository root.  The template provisions S3 buckets, a CloudFront distribution, Lambda functions, DynamoDB tables, a Cognito User Pool, API Gateway routes and EventBridge rules.
* **Terraform** – Initialise with `terraform init`, plan with `terraform plan` and apply with `terraform apply`.  You will need to supply values for variables in `terraform/variables.tf`.

## Notes

* The code provided here is a starting point.  You will need to fill out the lesson content, implement the AI prompt logic and fine‑tune IAM permissions.
* See the accompanying project plan for design details and free‑tier considerations.

## Running Locally with Docker

In addition to running the backend via the SAM CLI and the frontend via
`npm start`, you can spin up the entire stack using Docker.  This is
particularly useful if you want to test the application without
installing Python or Node.js on your host machine.

The repository includes a `docker-compose.yml` file and Dockerfiles
for both the backend and frontend.  To build and run the containers:

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) if
   you haven’t already.
2. From the `education-platform` directory run:

   ```bash
   # Build the images and start the services
   docker-compose up --build
   ```

   This command creates two containers: `backend` (Flask API on
   port 3001) and `frontend` (React app on port 3000).  The
   containers communicate over an internal Docker network and expose
   their ports to your localhost.  Once both services are up you can
   open your browser to `http://localhost:3000` to interact with the
   app.

3. Environment variables for the AI provider and OpenAI/Bedrock
   credentials can be passed via the `docker-compose` command or
   defined in a `.env` file.  For example:

   ```bash
   AI_PROVIDER=openai OPENAI_API_KEY=sk-your-key \
   docker-compose up --build
   ```

   When no AI provider is configured the backend falls back to
   deterministic responses.

4. Source code changes under `backend/lambdas` and `frontend/src` are
   automatically reflected in the running containers thanks to bind
   mounts.  You may need to refresh your browser to see the changes.

Stopping the services is as simple as pressing `Ctrl+C` in the
terminal.  If you encounter caching issues, add the `--force-recreate`
flag to the `docker-compose` command to rebuild containers from
scratch.
