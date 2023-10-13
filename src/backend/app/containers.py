from __future__ import annotations

from dependency_injector import containers, providers

from app.services.authentication_service import AuthenticationService
from app.services.io_service import IOService
from app.services.json_database_service.todos_json_database_service import (
    TodosJsonDatabaseService,
)
from app.services.json_database_service.users_json_database_service import (
    UsersJsonDatabaseService,
)
from app.services.sql_database_service.engine import engine
from app.services.sql_database_service.todos_service import TodosService
from app.services.sql_database_service.users_service import UsersService


class Container(containers.DeclarativeContainer):
    @classmethod
    def add_config(cls) -> type[Container]:
        cls.config = providers.Configuration()
        cls.config.database.from_env("DATABASE")

        cls.wiring_config = containers.WiringConfiguration(
            packages=["app.resources"]
        )

        return cls

    @classmethod
    def add_json_database_services(cls) -> type[Container]:
        cls.config.json_database.directory_path.from_env(
            "DATABASE_PATH", "./database/"
        )

        cls.users_io_service = providers.Resource(
            IOService.create_service,
            cls.config.json_database.directory_path(),
            "users.json",
        )

        cls.users_service = providers.Factory(
            UsersJsonDatabaseService, io_service=cls.users_io_service
        )

        cls.todo_io_service = providers.Resource(
            IOService.create_service,
            cls.config.json_database.directory_path(),
            "todos.json",
        )

        cls.todos_service = providers.Factory(
            TodosJsonDatabaseService, io_service=cls.todo_io_service
        )

        return cls

    @classmethod
    def add_postgresql_services(cls) -> type[Container]:
        cls.engine = providers.Singleton(engine)

        cls.users_service = providers.Factory(UsersService, engine=cls.engine)

        cls.todos_service = providers.Factory(TodosService, engine=cls.engine)

        return cls

    @classmethod
    def add_database_services(cls) -> type[Container]:
        if cls.config.database() == "json":
            cls.add_json_database_services()
        elif cls.config.database() == "postgresql":
            cls.add_postgresql_services()

        return cls

    @classmethod
    def add_services(cls) -> type[Container]:
        cls.authentication_service = providers.Factory(
            AuthenticationService, user_service=cls.users_service
        )

        return cls


Container.add_config().add_database_services().add_services()
