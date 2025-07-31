from sqlmodel import SQLModel, Field, create_engine, Relationship
from config import get_settings
from app.schemas.event import EventBase
from app.schemas.update import LiveUpdateBase
from app.schemas.comment import CommentBase
from app.schemas.like import LikeBase
from app.schemas.video import VideoBase
from app.schemas.category import CategoryBase

settings = get_settings()
engine = create_engine(settings.database_uri)


class VideoCategoryLink(SQLModel, table=True):
    video_id: int | None = Field(default=None, foreign_key="videos.id", primary_key=True)
    category_id: int | None = Field(default=None, foreign_key="categories.id", primary_key=True)


class Admin(SQLModel, table=True):
    __tablename__ = 'admins'

    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str


class Event(EventBase, table=True):
    __tablename__ = 'events'
    id: int | None = Field(default=None, primary_key=True)

    updates: list["LiveUpdate"] = Relationship(back_populates="event", cascade_delete=True)


class LiveUpdate(LiveUpdateBase, table=True):
    __tablename__ = 'liveupdates'
    id: int | None = Field(default=None, primary_key=True)

    event: Event | None = Relationship(back_populates="updates")
    comments: list["Comment"] = Relationship(back_populates="update", cascade_delete=True)
    likes: list["Like"] = Relationship(back_populates="update", cascade_delete=True)


class Video(VideoBase, table=True):
    __tablename__ = 'videos'
    id: int | None = Field(default=None, primary_key=True)

    comments: list["Comment"] = Relationship(back_populates="video", cascade_delete=True)
    likes: list["Like"] = Relationship(back_populates="video", cascade_delete=True)
    categories: list["Category"] = Relationship(back_populates="videos", link_model=VideoCategoryLink)


class Category(CategoryBase, table=True):
    __tablename__ = 'categories'
    id: int | None = Field(default=None, primary_key=True)

    videos: list["Video"] = Relationship(back_populates="categories", link_model=VideoCategoryLink)


class Comment(CommentBase, table=True):
    __tablename__ = 'comments'
    id: int | None = Field(default=None, primary_key=True)

    update: LiveUpdate | None = Relationship(back_populates="comments")
    video: Video | None = Relationship(back_populates="comments")


class Like(LikeBase, table=True):
    __tablename__ = 'likes'
    id: int | None = Field(default=None, primary_key=True)

    update: LiveUpdate | None = Relationship(back_populates="likes")
    video: Video | None = Relationship(back_populates="likes")
