from sqlmodel import SQLModel, Field
from datetime import timezone, datetime


class VideoBase(SQLModel):
    title: str
    views: int = 0
    url: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class VideoPublic(VideoBase):
    id: str


class VideoCombined:
    video: VideoPublic
    related_videos: list[VideoPublic]
