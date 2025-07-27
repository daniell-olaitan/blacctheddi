from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Annotated

from app.core.dependencies import get_db
from app.crud import update as updates_crud
from app.schemas.comment import CommentPublic
from app.schemas.like import LikePublic

router = APIRouter()


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
) -> LikePublic:
    return updates_crud.like_update(db, update_id)
