from sqlmodel import SQLModel, Field, create_engine, Relationship
from config import get_settings
from datetime import datetime, timezone
from app.schemas.event import EventBase
from app.schemas.update import LiveUpdateBase
from app.schemas.comment import CommentBase
from app.schemas.like import LikeBase

settings = get_settings()
engine = create_engine(settings.database_uri)


class Admin(SQLModel, table=True):
    __tablename__ = 'admins'

    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str
    is_admin: bool = True


class Event(EventBase, table=True):
    __tablename__ = 'events'
    id: int | None = Field(default=None, primary_key=True)

    updates: list["LiveUpdate"] = Relationship(back_populates="event", cascade_delete=True)


class LiveUpdate(LiveUpdateBase, table=True):
    __tablename__ = 'liveupdates'

    id: int | None = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="events.id", ondelete='CASCADE')

    event: Event | None = Relationship(back_populates="updates")
    comments: list["Comment"] = Relationship(back_populates="update", cascade_delete=True)
    likes: list["Like"] = Relationship(back_populates="update", cascade_delete=True)


class Video(SQLModel, table=True):
    __tablename__ = 'videos'

    id: int | None = Field(default=None, primary_key=True)
    title: str
    views: int = 0
    url: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    comments: list["Comment"] = Relationship(back_populates="video", cascade_delete=True)
    likes: list["Like"] = Relationship(back_populates="video", cascade_delete=True)


class Comment(CommentBase, table=True):
    __tablename__ = 'comments'

    id: int | None = Field(default=None, primary_key=True)
    update_id: int | None = Field(default=None, foreign_key="liveupdates.id", ondelete='CASCADE')
    video_id: int | None = Field(default=None, foreign_key="videos.id", ondelete='CASCADE')

    update: LiveUpdate | None = Relationship(back_populates="comments")
    video: Video | None = Relationship(back_populates="comments")


class Like(LikeBase, table=True):
    __tablename__ = 'likes'

    id: int | None = Field(default=None, primary_key=True)
    update_id: int | None = Field(default=None, foreign_key="liveupdates.id", ondelete='CASCADE')
    video_id: int | None = Field(default=None, foreign_key="videos.id", ondelete='CASCADE')

    update: LiveUpdate | None = Relationship(back_populates="likes")
    video: Video | None = Relationship(back_populates="likes")
