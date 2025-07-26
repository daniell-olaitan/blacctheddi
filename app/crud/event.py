from sqlmodel import Session, select
from app.storage.models import Event, LiveUpdate


def get_all_live_events(db: Session) -> list[Event]:
    return db.exec(select(Event).where(Event.status == "live")).all()


def get_updates_for_event(db: Session, event_id: int) -> list[LiveUpdate]:
    return db.exec(select(LiveUpdate).where(
        LiveUpdate.event_id == event_id
    ).order_by(LiveUpdate.timestamp.desc())).all()
