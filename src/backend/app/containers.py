import asyncio

from dependency_injector import containers, providers

from app.services.authentication_service import AuthenticationService
from app.services.io_service import IOService
from app.services.json_database_service.todos_json_database_service import (
    TodosJsonDatabaseService,
)
from app.services.json_database_service.users_json_database_service import (
    UsersJsonDatabaseService,
)


class Container(containers.DeclarativeContainer):
    @classmethod
    def add_config(cls) -> type["Container"]:
        cls.config = providers.Configuration()
        cls.config.json_database.directory_path.from_env(
            "DATABASE_PATH", "./database/"
        )

        cls.wiring_config = containers.WiringConfiguration(
            packages=["app.resources"]
        )

        return cls

    @classmethod
    def add_json_database_services(cls) -> type["Container"]:
        cls.users_io_service = asyncio.run(
            IOService.create_service(
                cls.config.json_database.directory_path(),
                "users.json",
            )
        )

        cls.todo_io_service = asyncio.run(
            IOService.create_service(
                cls.config.json_database.directory_path(),
                "todos.json",
            )
        )

        return cls

    @classmethod
    def add_services(cls) -> type["Container"]:
        cls.users_service = providers.Factory(
            UsersJsonDatabaseService,
            io_service=cls.users_io_service,
        )

        cls.todos_service = providers.Factory(
            TodosJsonDatabaseService,
            io_service=cls.todo_io_service,
        )

        cls.authentication_service = providers.Factory(
            AuthenticationService,
            user_service=cls.users_service,
        )

        return cls


Container.add_config().add_json_database_services().add_services()
