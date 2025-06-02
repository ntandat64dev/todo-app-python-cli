from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    SmallInteger,
    String,
    Table,
)

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(30)),
    Column("password", String(30)),
)

todos_table = Table(
    "todos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", String),
    Column("due_date", DateTime),
    Column("priority", SmallInteger, nullable=False),
    Column("completed", Boolean),
    Column("created_at", DateTime, nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
)
