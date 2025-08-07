## Dockerfile for the backend service
#
# This image installs the required Python dependencies and runs the
# Flask application defined in app.py.  It exposes port 3001 by
# default and accepts AI configuration via environment variables.  To
# build and run this container as part of a full stack use the
# accompanying docker-compose.yml file in the repository root.

FROM python:3.11-slim

# Avoid generating .pyc files and ensure output is unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the Flask port
EXPOSE 3001

# Default command to run the Flask server.  The AI configuration can
# be overridden via environment variables at runtime.
CMD ["python", "app.py"]