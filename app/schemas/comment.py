from sqlmodel import SQLModel, Field
from datetime import timezone, datetime


class CommentBase(SQLModel):
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_id: int | None = Field(default=None, foreign_key="liveupdates.id", ondelete='CASCADE')
    video_id: int | None = Field(default=None, foreign_key="videos.id", ondelete='CASCADE')


class CommentPublic(CommentBase):
    id: int
