from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session
from typing import Annotated

from app.core.dependencies import get_db
from app.crud import event as events_crud
from app.schemas.event import EventPublicWithRel, LiveUpdatePublicWithEvent
from app.schemas.comment import CommentCreate, CommentPublic
from app.schemas.like import LikeBase, LikePublic

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
) -> list[LiveUpdatePublicWithEvent]:
    return events_crud.get_updates_for_event(db, event_id, limit, offset)


@router.get("/{event_id}")
def get_an_event(
    event_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> EventPublicWithRel:
    event = events_crud.get_event(db, event_id)
    if event:
        return event

    raise HTTPException(status_code=404, detail="Event not found")


@router.post("/{event_id}/comments")
def comment_on_event(
    event_id: int,
    content: CommentCreate,
    db: Annotated[Session, Depends(get_db)]
) -> CommentPublic:
    return events_crud.comment_on_event(db, event_id, content)


@router.get("/{event_id}/comments")
def get_event_comments(
    event_id: int, db: Annotated[Session, Depends(get_db)]
) -> list[CommentPublic]:
    return events_crud.get_comments_for_event(db, event_id)


@router.post("/{event_id}/likes")
def like_an_event(
    event_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> LikePublic:
    return events_crud.like_event(db, event_id)


@router.get("/{event_id}/likes")
def get_event_likes(
    event_id: int, db: Annotated[Session, Depends(get_db)]
) -> int:
    return events_crud.get_like_count_for_event(db, event_id)
