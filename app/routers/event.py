from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import Annotated

from app.core.dependencies import get_db
from app.crud import event as events_crud
from app.schemas.event import EventPublicWithRel
from app.schemas.update import LiveUpdatePublicWithRel

router = APIRouter()


@router.get("/")
def list_events(
    db: Annotated[Session, Depends(get_db)]
) -> list[EventPublicWithRel]:
    return events_crud.get_all_live_events(db)


@router.get("/{event_id}/updates")
def get_event_updates(
    event_id: int,
    db: Annotated[Session, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[LiveUpdatePublicWithRel]:
    return events_crud.get_updates_for_event(db, event_id, limit, offset)
