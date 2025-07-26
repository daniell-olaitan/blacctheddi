from sqlmodel import SQLModel, Field
from datetime import timezone, datetime


class LikeBase(SQLModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LikePublic(LikeBase):
    id: int
