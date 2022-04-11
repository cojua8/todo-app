# TODO APP
This is a Todo app. A basic one. But it has been used for learning ways of abstraction in python, such as Generics and Protocols. Also, I have tried to use best practices of format and such.

## Installation
        
    pip install -r requirements.txt

Nothing else should be needed.

## Code Style
The tools used for formatting are:
- [black](https://black.readthedocs.io/en/stable/): A code formatter for Python.
- [isort](https://isort.readthedocs.io/en/stable/): Sorts imports.

All of the setting for these tools are in the `pyproject.toml` file.

**Note** that `flake8` should be used as `flake8p` for it to read the settings of `pyproject.toml`. 

## On Generics and Protocols.
These are two concepts that I have been using in my code. Though they help the type checker tell if something is wrong in code (static analysis), they really have no influence in runtime.

## Dependendy Injection
[Dependency injection](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html) is used to decouple the different parts of the program. To use this, objects must not create new instances of classes in their constructors, but receive them as parameters. 


## Docker
[Docker](https://www.docker.com/) is used to run the app in a container. The command used to create and start the containers is:
    
    docker-compose up -d

This will run the container in detached mode.