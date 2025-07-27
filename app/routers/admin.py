from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel import Session
from typing import Annotated

from app.core.dependencies import verify_admin, get_db
from app.crud import admin as admin_crud
from app.storage.models import Video
from app.schemas.event import EventBase, EventPublic
from app.schemas.update import LiveUpdateCreate, LiveUpdatePublic
from app.schemas.comment import CommentPublic

router = APIRouter(dependencies=[Depends(verify_admin)])


@router.post("/events")
def create_event(
    event: EventBase, db: Annotated[Session, Depends(get_db)]
) -> EventPublic:
    return admin_crud.create_event(db, event)


@router.post("/events/{event_id}/updates")
def add_update_to_event(
    event_id: int,
    update: LiveUpdateCreate,
    db: Annotated[Session, Depends(get_db)]
) -> LiveUpdatePublic:
    return admin_crud.add_update(db, event_id, update)


@router.post("/videos")
def upload_video(
    video: Video,
    db: Annotated[Session, Depends(get_db)]
):
    return admin_crud.upload_video(db, video)


@router.get("/updates/{update_id}/likes")
def get_update_likes(
    update_id: int, db: Annotated[Session, Depends(get_db)]
) -> int:
    return admin_crud.get_like_count_for_update(db, update_id)


@router.get("/videos/{video_id}/likes")
def get_video_likes(
    video_id: int, db: Annotated[Session, Depends(get_db)]
) -> int:
    return admin_crud.get_like_count_for_video(db, video_id)


@router.get("/updates/{update_id}/comments")
def get_update_comments(
    update_id: int, db: Annotated[Session, Depends(get_db)]
) -> list[CommentPublic]:
    return admin_crud.get_comments_for_update(db, update_id)


@router.get("/videos/{video_id}/comments")
def get_video_comments(
    video_id: int, db: Annotated[Session, Depends(get_db)]
) -> list[CommentPublic]:
    return admin_crud.get_comments_for_video(db, video_id)


# @router.get("/views")
# def get_all_view_counts(
#     db: Annotated[Session, Depends(get_db)]
# ) -> dict:
#     return admin_crud.get_all_views(db)


# @router.get("/comments")
# def get_all_comments(
#     db: Annotated[Session, Depends(get_db)]
# ) -> list[CommentPublic]:
#     return admin_crud.get_all_comments(db)


# @router.get("/likes")
# def get_all_likes(
#     db: Annotated[Session, Depends(get_db)]
# ) -> dict:
#     return admin_crud.get_all_likes(db)


@router.delete("/events/{event_id}")
def close_and_delete_event(
    event_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    return admin_crud.delete_event(db, event_id)
