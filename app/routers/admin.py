from fastapi import APIRouter, Depends, UploadFile, Form, File, HTTPException
from sqlmodel import Session
from typing import Annotated
from app.core.dependencies import verify_admin, get_db
from app.crud import admin as admin_crud
from app.schemas.video import VideoPublic
from app.schemas.event import EventBase, EventPublic
from app.schemas.update import LiveUpdateCreate, LiveUpdatePublic
from app.schemas.comment import CommentPublic
from app.schemas.common import StatusJSON
from app.schemas.admin import Analytics

router = APIRouter(dependencies=[Depends(verify_admin)])


@router.post("/events")
def create_event(
    event: EventBase, db: Annotated[Session, Depends(get_db)]
) -> EventPublic:
    return admin_crud.create_event(db, event)


@router.post("/events/{event_id}/updates")
def add_update_to_event(
    event_id: int,
    title: Annotated[str, Form()],
    details: Annotated[str, Form()],
    db: Annotated[Session, Depends(get_db)],
    image_file: Annotated[UploadFile | None, File()] = None,
) -> LiveUpdatePublic:
    update = LiveUpdateCreate(title=title, details=details)
    return admin_crud.add_update(db, event_id, update, image_file)


@router.post("/videos")
def upload_video(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    category_ids: Annotated[list[int], Form()],
    thumbnail: Annotated[UploadFile, File()],
    video_file: Annotated[UploadFile, File()],
    db: Annotated[Session, Depends(get_db)]
) -> VideoPublic:
    categories = admin_crud.validate_category_ids(db, category_ids)
    if categories is None:
        raise HTTPException(status_code=400, detail="Some category IDs are invalid.")

    video_data = {
        'title': title,
        'description': description,
        'categories': categories
    }

    return admin_crud.upload_files(db, video_data, thumbnail, video_file)


@router.get("/analytics")
def get_the_analytics(
    db: Annotated[Session, Depends(get_db)]
) -> Analytics:
    return admin_crud.get_analytics(db)


@router.delete("/events/{event_id}")
def close_and_delete_event(
    event_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> StatusJSON:
    return admin_crud.delete_event(db, event_id)
