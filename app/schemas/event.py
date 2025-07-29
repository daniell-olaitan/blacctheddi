from sqlmodel import SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.update import LiveUpdatePublic


class EventBase(SQLModel):
    title: str
    status: str = 'live'  # live or ended


class EventPublic(EventBase):
    id: int


class EventPublicWithRel(EventPublic):
    updates: list["LiveUpdatePublic"]
