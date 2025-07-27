from sqlmodel import SQLModel
from app.schemas.update import LiveUpdatePublic


class EventBase(SQLModel):
    title: str
    status: str = 'live'  # live or ended


class EventPublic(EventBase):
    id: int


class EventPublicWithRel(EventPublic):
    updates: list[LiveUpdatePublic]
