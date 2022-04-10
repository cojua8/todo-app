import os

from dependency_injector import containers, providers

from app.services.json_database_service.todos_json_database_service import (
    TodosJsonDatabaseService,
)
from app.services.json_database_service.users_json_database_service import (
    UsersJsonDatabaseService,
)


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["app.resources"])

    users_database = providers.Factory(
        UsersJsonDatabaseService,
        directory_path=os.environ["DATABASE_PATH"],
    )

    todos_database = providers.Factory(
        TodosJsonDatabaseService,
        directory_path=os.environ["DATABASE_PATH"],
    )
