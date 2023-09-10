FROM python:3.11.2-slim
WORKDIR /app/backend

COPY ./app ./app
COPY ./poetry.lock .
COPY ./pyproject.toml .

ENV POETRY_HOME=/opt/poetry
ENV POETRY_CACHE_DIR=/opt/poetry/cache

RUN pip install poetry
RUN poetry install
CMD poetry run uvicorn app.app:app --reload --host 0.0.0.0 --port 5000
