# BASIC TODO APP

[![Backend Static Code Analysis](https://github.com/cojua8/todo-app/actions/workflows/static_code_analysis_backend.yml/badge.svg)](https://github.com/cojua8/todo-app/actions/workflows/static_code_analysis_backend.yml)
[![Frontend Static Code Analysis](https://github.com/cojua8/todo-app/actions/workflows/static_code_analysis_frontend.yml/badge.svg)](https://github.com/cojua8/todo-app/actions/workflows/static_code_analysis_frontend.yml)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Svelte](https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white)](https://svelte.dev/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)](https://grafana.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)](https://prometheus.io/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

This is a Todo app. A basic one. But it has been used for learning ways of abstraction in python, such as Generics and Protocols. Also, I have tried to use best practices of format and such.

## Usage

The best way to get the running is by using Docker. To do this, you must have Docker installed in your machine. Once you have it, you can run the following command:

    docker compose -f docker-compose.development.yml up -d

This will get you:

- The frontend running in [port 3000](http://localhost:3000/)
- The backend running in [port 5000](http://localhost:5000/)
- Prometheus running in [port 9090](http://localhost:9090/)
- Grafana running in [port 7000](http://localhost:7000/)

> To stop the app, you can run: `docker compose -f docker-compose.development.yml down`

## Frontend development:

To start development of the frontend app, do the following:

    cd src\frontend && npm install

For linting and formatting, do:

    npm run prettier
    npm run eslint

## Backend development:

To start development of the frontend app, do the following:

    cd src\backend && poetry install

For linting and formatting, do:

    poetry run pyright .
    poetry run ruff check .
    poetry run black --check .

Tests require Docker to be running. To run them, just do:

    poetry run pytest

## On Python

### Generics and Protocols.

These are two concepts that I have been using in my code. Though they help the type checker tell if something is wrong in code (static analysis), they really have no influence in runtime.

### Dependency Injection

[Dependency injection](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html) is used to decouple the different parts of the program. To use this, objects must not create new instances of classes in their constructors, but receive them as parameters.

### Asyncio

[Asyncio](https://docs.python.org/3/library/asyncio.html) is used together with [aiofiles](https://aiofiles.readthedocs.io/en/stable/) to read and write files in an asyncronous way
Also, SQLAlchemy uses an async backend [asyncpg](https://magicstack.github.io/asyncpg/current/)
