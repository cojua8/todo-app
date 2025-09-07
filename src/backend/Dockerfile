FROM python:3.11.9-slim
WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ARG FRAMEWORK
ENV FRAMEWORK=$FRAMEWORK

COPY ./app ./app
COPY ./uv.lock .
COPY ./pyproject.toml .


RUN pip install uv
RUN uv sync --only-group $FRAMEWORK

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

#using --reload here fucks up otlp. Maybe try another tool like watchdog
CMD ["uv", "run", "opentelemetry-instrument", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5000"]
