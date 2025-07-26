from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Annotated

from app.core.dependencies import get_db
from app.crud import update as updates_crud
from app.schemas.comment import CommentPublic

router = APIRouter(prefix="/updates", tags=["Updates"])


@router.post("/{update_id}/comments")
def comment_on_update(
    update_id: int,
    content: dict,
    db: Annotated[Session, Depends(get_db)]
) -> CommentPublic:
    return updates_crud.comment_on_update(db, update_id, content)


@router.post("/{update_id}/likes")
def like_update(
    update_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> dict:
    return updates_crud.like_update(db, update_id)
