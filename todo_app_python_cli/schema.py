from datetime import datetime

from models import Priority, Role
from pydantic import BaseModel, field_serializer


class User(BaseModel):
    id: int
    username: str
    role: Role


class Todo(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    due_date: datetime | None = None
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    created_at: datetime = datetime.now()
    user_id: int

    @field_serializer("priority")
    def serialize_priority(self, priority: Priority):
        return priority.name

    @field_serializer("completed")
    def serialize_completed(self, completed: bool):
        return "✓" if completed else ""

    @field_serializer("due_date", "created_at")
    def serialize_datetime(self, field: datetime):
        return field.strftime("%Y-%m-%d %H:%M:%S")
