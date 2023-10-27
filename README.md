[![Backend Static Code Analysis](https://github.com/cojua8/todo-app/actions/workflows/static_code_analysis_backend.yml/badge.svg)](https://github.com/cojua8/todo-app/actions/workflows/static_code_analysis_backend.yml)
[![Frontend Static Code Analysis](https://github.com/cojua8/todo-app/actions/workflows/static_code_analysis_frontend.yml/badge.svg)](https://github.com/cojua8/todo-app/actions/workflows/static_code_analysis_frontend.yml)

# TODO APP
This is a Todo app. A basic one. But it has been used for learning ways of abstraction in python, such as Generics and Protocols. Also, I have tried to use best practices of format and such.

## Installation
Requires Poetry to be installed. To install the dependencies, run:
        
    poetry install

Nothing else should be needed.

## Code Style
The tools used for formatting are:
- [black](https://black.readthedocs.io/en/stable/): A code formatter for Python.
- [ruff](https://docs.astral.sh/ruff/): An extremely fast Python linter, written in Rust.

All of the setting for these tools are in the `pyproject.toml` file.

## On Generics and Protocols.
These are two concepts that I have been using in my code. Though they help the type checker tell if something is wrong in code (static analysis), they really have no influence in runtime.

## Dependency Injection
[Dependency injection](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html) is used to decouple the different parts of the program. To use this, objects must not create new instances of classes in their constructors, but receive them as parameters. 


## Docker
[Docker](https://www.docker.com/) is used to run the app in a container. The command used to create and start the containers is:

    docker compose -f docker-compose.development.yml up -d

## Asyncio
[Asyncio](https://docs.python.org/3/library/asyncio.html) is used together with [aiofiles](https://aiofiles.readthedocs.io/en/stable/) to read and write files in an asyncronous way

