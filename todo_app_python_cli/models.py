import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

metadata = MetaData()


class Priority(enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Role(enum.Enum):
    ADMIN = 1
    USER = 2


users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(30), nullable=False, unique=True),
    Column("password", String(64), nullable=False),
    Column("role", Enum(Role), nullable=False),
)

todos_table = Table(
    "todos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("description", String),
    Column("due_date", DateTime),
    Column("priority", Enum(Priority), nullable=False),
    Column("completed", Boolean, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
)
