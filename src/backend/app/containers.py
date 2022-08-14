import asyncio

from app.services.authentication_service import AuthenticationService
from app.services.io_service import IOService
from app.services.json_database_service.todos_json_database_service import (
    TodosJsonDatabaseService,
)
from app.services.json_database_service.users_json_database_service import (
    UsersJsonDatabaseService,
)
from dependency_injector import containers, providers


async def make_io_services(database_directory: str):
    return await asyncio.gather(
        IOService.create_service(database_directory, "users.json"),
        IOService.create_service(database_directory, "todos.json"),
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.json_database.directory_path.from_env("DATABASE_PATH")

    wiring_config = containers.WiringConfiguration(packages=["app.resources"])

    users_io_service, todo_io_service = asyncio.run(
        make_io_services(config.json_database.directory_path())
    )

    users_service = providers.Factory(
        UsersJsonDatabaseService,
        io_service=users_io_service,
    )

    todos_service = providers.Factory(
        TodosJsonDatabaseService,
        io_service=todo_io_service,
    )

    authentication_service = providers.Factory(
        AuthenticationService,
        user_service=users_service,
    )
