import datetime as dt
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    MetaData,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID

metadata_obj = MetaData()

user_table = Table(
    "users",
    metadata_obj,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("username", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("password", String(255), nullable=False),
)


todo_table = Table(
    "todos",
    metadata_obj,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("owner_id", ForeignKey("users.id"), nullable=False),
    Column("description", String, nullable=False),
    Column("due_date", Date),
    Column("completed", Boolean, default=False),
    Column(
        "date_created",
        Date,
        nullable=False,
        default=dt.datetime.now(tz=dt.UTC).today(),
    ),
)
