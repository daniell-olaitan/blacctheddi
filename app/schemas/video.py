from sqlmodel import SQLModel, Field
from datetime import timezone, datetime
from pydantic import BaseModel
from app.schemas.like import LikePublic
from app.schemas.comment import CommentPublic


class VideoBase(SQLModel):
    title: str
    description: str
    views: int = 0
    url: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    thumbnail_url: str | None = None


class VideoPublic(VideoBase):
    id: int


class VideoPublicWithRel(VideoPublic):
    comments: list[CommentPublic]
    likes: list[LikePublic]


class VideoCombined(BaseModel):
    video: VideoPublicWithRel
    related_videos: list[VideoPublicWithRel]
