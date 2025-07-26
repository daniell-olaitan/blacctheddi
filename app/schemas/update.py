from sqlmodel import SQLModel, Field
from datetime import timezone, datetime


class LiveUpdateCreate(SQLModel):
    title: str
    details: str


class LiveUpdateBase(LiveUpdateCreate):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LiveUpdatePublic(LiveUpdateBase):
    id: int
