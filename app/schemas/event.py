from sqlmodel import SQLModel, Field
from sqlalchemy import Text
from app.schemas.update import LiveUpdatePublic, LiveUpdatePublicWithRel
from datetime import datetime, timezone
from app.schemas.like import LikePublic
from app.schemas.comment import CommentPublic


class EventCreate(SQLModel):
    title: str
    details: str = Field(sa_column=Text)
    status: str = 'live'  # live or ended


class EventBase(EventCreate):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    image_url: str | None = None


class EventPublic(EventBase):
    id: int


class EventPublicWithRel(EventPublic):
    updates: list[LiveUpdatePublic]
    comments: list[CommentPublic]
    likes: list[LikePublic]


class LiveUpdatePublicWithEvent(LiveUpdatePublicWithRel):
    event: EventPublic
