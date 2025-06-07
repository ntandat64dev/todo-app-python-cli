import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str


class Todo(BaseModel):
    id: int | None
    title: str
    description: str | None
    due_date: datetime.datetime | None
    priority: int | None
    completed: bool | None
    created_at: datetime.datetime | None
    user_id: int | None
