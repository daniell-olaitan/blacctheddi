from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Annotated

from app.core.dependencies import get_db
from app.crud import like as like_crud

router = APIRouter()


@router.delete('/{like_id}')
def unlike_update_or_video(
    like_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> dict:
    return like_crud.unlike_item(db, like_id)
