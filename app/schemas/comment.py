from sqlmodel import SQLModel, Field
from sqlalchemy import Text
from datetime import timezone, datetime


class CommentCreate(SQLModel):
    content: str = Field(sa_column=Text)


class CommentBase(CommentCreate):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_id: int | None = Field(default=None, foreign_key="liveupdates.id", ondelete='CASCADE')
    event_id: int | None = Field(default=None, foreign_key="events.id", ondelete='CASCADE')
    video_id: int | None = Field(default=None, foreign_key="videos.id", ondelete='CASCADE')


class CommentPublic(CommentBase):
    id: int
