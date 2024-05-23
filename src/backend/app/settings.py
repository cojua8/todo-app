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
