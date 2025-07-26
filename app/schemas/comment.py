from sqlmodel import SQLModel, Field
from datetime import timezone, datetime


class CommentBase(SQLModel):
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CommentPublic(CommentBase):
    id: int
