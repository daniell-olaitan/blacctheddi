from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Annotated

from app.core.dependencies import get_db
from app.crud import update as updates_crud
from app.schemas.comment import CommentPublic, CommentCreate
from app.schemas.like import LikePublic
from app.schemas.event import LiveUpdatePublicWithEvent

router = APIRouter()


@router.get('/recent')
def fetch_recent_updates(
    db: Annotated[Session, Depends(get_db)]
) -> list[LiveUpdatePublicWithEvent]:
    return updates_crud.get_recent_updates(db)


@router.get("/{update_id}")
def get_event_update(
    update_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> LiveUpdatePublicWithEvent:
    update = updates_crud.get_update(db, update_id)
    if update:
        return update

    raise HTTPException(status_code=404, detail="Live update not found")


@router.post("/{update_id}/comments")
def comment_on_update(
    update_id: int,
    content: CommentCreate,
    db: Annotated[Session, Depends(get_db)]
) -> CommentPublic:
    return updates_crud.comment_on_update(db, update_id, content)


@router.get("/{update_id}/comments")
def get_update_comments(
    update_id: int, db: Annotated[Session, Depends(get_db)]
) -> list[CommentPublic]:
    return updates_crud.get_comments_for_update(db, update_id)


@router.post("/{update_id}/likes")
def like_update(
    update_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> LikePublic:
    return updates_crud.like_update(db, update_id)


@router.get("/{update_id}/likes")
def get_update_likes(
    update_id: int, db: Annotated[Session, Depends(get_db)]
) -> int:
    return updates_crud.get_like_count_for_update(db, update_id)
