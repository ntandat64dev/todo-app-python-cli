from datetime import datetime
from enum import Enum
from pydantic import BaseModel

from models import Priority


class User(BaseModel):
    id: int
    username: str


class Todo(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    due_date: datetime | None = None
    priority: Priority | None = Priority.MEDIUM
    completed: bool | None = False
    created_at: datetime | None = datetime.now()
    user_id: int | None = None
