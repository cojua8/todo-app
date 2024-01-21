from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class JsonDBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_path: str = Field(validation_alias="DATABASE_PATH")


class SqlDBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    db_dialect: str = Field(validation_alias="DB_DIALECT")
    db_username: str = Field(validation_alias="DB_USERNAME")
    db_password: str = Field(validation_alias="DB_PASSWORD")
    db_host: str = Field(validation_alias="DB_HOST")
    db_port: int = Field(validation_alias="DB_PORT")
    db_name: str = Field(validation_alias="DB_NAME")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database: str = Field(validation_alias="DATABASE")
