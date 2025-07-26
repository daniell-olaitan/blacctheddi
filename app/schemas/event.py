from sqlmodel import SQLModel


class EventBase(SQLModel):
    title: str
    status: str = 'live'  # live or ended


class EventPublic(EventBase):
    id: int
