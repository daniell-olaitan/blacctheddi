from sqlmodel import SQLModel, Field
from sqlalchemy import Text
from datetime import timezone, datetime
from pydantic import BaseModel
from app.schemas.like import LikePublic
from app.schemas.comment import CommentPublic
from app.schemas.category import CategoryPublic


class VideoBase(SQLModel):
    title: str
    description: str = Field(sa_column=Text)
    views: int = 0
    url: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    thumbnail_url: str | None = None


class VideoPublic(VideoBase):
    id: int


class VideoPublicWithRel(VideoPublic):
    comments: list[CommentPublic]
    likes: list[LikePublic]
    categories: list[CategoryPublic]


class VideoCombined(BaseModel):
    video: VideoPublicWithRel
    related_videos: list[VideoPublicWithRel]


class CategoryPublicRel(CategoryPublic):
    videos: list[VideoPublic]
