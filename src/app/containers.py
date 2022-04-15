import os

from dependency_injector import containers, providers

from app.services.authentication_service.authentication_service import (
    AuthenticationService,
)
from app.services.json_database_service.todos_json_database_service import (
    TodosJsonDatabaseService,
)
from app.services.json_database_service.users_json_database_service import (
    UsersJsonDatabaseService,
)


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["app.resources"])

    users_service = providers.Factory(
        UsersJsonDatabaseService,
        directory_path=os.environ["DATABASE_PATH"],
    )

    todos_service = providers.Factory(
        TodosJsonDatabaseService,
        directory_path=os.environ["DATABASE_PATH"],
    )

    authentication_service = providers.Factory(
        AuthenticationService,
        user_service=users_service,
    )
