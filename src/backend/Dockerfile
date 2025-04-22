FROM python:3.11.2-slim
WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV POETRY_HOME=/opt/poetry
ENV POETRY_CACHE_DIR=/opt/poetry/cache
ARG FRAMEWORK
ENV FRAMEWORK=$FRAMEWORK

COPY ./app ./app
COPY ./poetry.lock .
COPY ./pyproject.toml .


RUN pip install poetry 
RUN poetry install --with $FRAMEWORK

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["poetry", "run", "opentelemetry-instrument", "uvicorn", "app.app:app", "--reload", "--host", "0.0.0.0",  "--port", "5000"]
