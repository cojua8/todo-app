
from pydantic import Field
from pydantic_settings import BaseSettings


class JsonDBSettings(BaseSettings):
    database_path: str = Field(validation_alias="DATABASE_PATH")


class SqlDBSettings(BaseSettings):
    db_dialect: str = Field(validation_alias="DB_DIALECT")
    db_username: str = Field(validation_alias="DB_USERNAME")
    db_password: str = Field(validation_alias="DB_PASSWORD")
    db_host: str = Field(validation_alias="DB_HOST")
    db_port: int = Field(validation_alias="DB_PORT")
    db_name: str = Field(validation_alias="DB_NAME")


class Settings(BaseSettings):
    database: str = Field(validation_alias="DATABASE")
    framework: str = Field(validation_alias="FRAMEWORK")
    log_level: str = Field(validation_alias="LOG_LEVEL")


class CorsSettings(BaseSettings):
    origins: list[str] = Field(
        ["http://localhost:3000"], validation_alias="CORS_ORIGINS"
    )
    methods: list[str] | str = Field(
        ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
        validation_alias="CORS_METHODS",
    )
    allow_headers: list[str] | str = Field(
        "*", validation_alias="CORS_ALLOW_HEADERS"
    )
    supports_credentials: bool = Field(
        default=True, validation_alias="CORS_SUPPORTS_CREDENTIALS"
    )
