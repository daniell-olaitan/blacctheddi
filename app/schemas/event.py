from sqlmodel import SQLModel
from app.schemas.update import LiveUpdatePublic, LiveUpdatePublicWithRel


class EventBase(SQLModel):
    title: str
    status: str = 'live'  # live or ended


class EventPublic(EventBase):
    id: int


class EventPublicWithRel(EventPublic):
    updates: list[LiveUpdatePublic]


class LiveUpdatePublicWithEvent(LiveUpdatePublicWithRel):
    event: EventPublic
