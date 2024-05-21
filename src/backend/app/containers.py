from __future__ import annotations

from dependency_injector import containers, providers

from app.infrastructure.json_database_service.todos_json_database_service import (
    TodosJsonDatabaseService,
)
from app.infrastructure.json_database_service.users_json_database_service import (
    UsersJsonDatabaseService,
)
from app.infrastructure.sql_database_service.engine import engine
from app.infrastructure.sql_database_service.todos_service import TodosService
from app.infrastructure.sql_database_service.users_service import UsersService
from app.services.authentication_service import AuthenticationService
from app.services.io_service import IOService
from app.settings import JsonDBSettings, Settings, SqlDBSettings


class Container(containers.DeclarativeContainer):
    @classmethod
    def add_config(cls) -> type[Container]:
        cls.config = Settings()  # type: ignore reportGeneralTypeIssues

        cls.wiring_config = containers.WiringConfiguration(
            packages=["app.resources"]
        )

        return cls

    @classmethod
    def _add_json_database_services(cls) -> type[Container]:
        settings = JsonDBSettings()  # type: ignore reportGeneralTypeIssues
        cls.users_io_service = providers.Resource(
            IOService.create_service, settings.database_path, "users.json"
        )

        cls.users_service = providers.Factory(
            UsersJsonDatabaseService, io_service=cls.users_io_service
        )

        cls.todo_io_service = providers.Resource(
            IOService.create_service, settings.database_path, "todos.json"
        )

        cls.todos_service = providers.Factory(
            TodosJsonDatabaseService, io_service=cls.todo_io_service
        )

        return cls

    @classmethod
    def _add_postgresql_services(cls) -> type[Container]:
        cls.engine = providers.Singleton(
            engine, SqlDBSettings()  # type: ignore reportGeneralTypeIssues
        )

        cls.users_service = providers.Factory(UsersService, engine=cls.engine)

        cls.todos_service = providers.Factory(TodosService, engine=cls.engine)

        return cls

    @classmethod
    def add_database_services(cls) -> type[Container]:
        if cls.config.database == "json":
            cls._add_json_database_services()
        elif cls.config.database == "postgresql":
            cls._add_postgresql_services()

        return cls

    @classmethod
    def add_services(cls) -> type[Container]:
        cls.authentication_service = providers.Factory(
            AuthenticationService, user_service=cls.users_service
        )

        return cls


Container.add_config().add_database_services().add_services()
