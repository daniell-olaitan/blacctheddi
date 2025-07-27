from sqlmodel import Session, select
from app.storage.models import Admin, Event, LiveUpdate, Video, Comment, Like
from app.schemas.event import EventBase
from app.schemas.update import LiveUpdateCreate
from fastapi import UploadFile
from app.schemas.common import StatusJSON
from app.core.utils import store_file


def get_admin(db: Session, username: str) -> Admin | None:
    return db.exec(select(Admin).where(Admin.username == username)).first()


def create_event(db: Session, event: EventBase) -> Event:
    event = Event.model_validate(event)
    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def add_update(
    db: Session,
    event_id: int,
    update_data: LiveUpdateCreate,
    image_file: UploadFile
) -> LiveUpdate:
    image_url = store_file(image_file, 'images') if image_url else None
    update = LiveUpdate(
        **update_data.model_dump(),
        event_id=event_id,
        image_url=image_url
    )

    db.add(update)
    db.commit()
    db.refresh(update)

    return update


def upload_video(db: Session, title: str, file: UploadFile) -> Video:
    video_url = store_file(file)
    video = Video(title=title, url=video_url)
    db.add(video)
    db.commit()
    db.refresh(video)

    return video


def get_like_count_for_update(db: Session, update_id: int) -> int:
    return db.exec(select(Like).where(Like.update_id == update_id)).all().count()


def get_like_count_for_video(db: Session, video_id: int) -> int:
    return db.exec(select(Like).where(Like.video_id == video_id)).all().count()


def get_comments_for_update(db: Session, update_id: int) -> list[Comment]:
    return db.exec(select(Comment).where(Comment.update_id == update_id)).all()


def get_comments_for_video(db: Session, video_id: int) -> list[Comment]:
    return db.exec(select(Comment).where(Comment.video_id == video_id)).all()


# def get_all_views(db: Session) -> dict:
#     return {"total_views": sum(v.views for v in db.exec(select(Video)).all())}


# def get_all_comments(db: Session) -> list[Comment]:
#     return db.exec(select(Comment)).all()


# def get_all_likes(db: Session) -> dict:
#     return {
#         "video_likes": db.exec(select(Like).where(Like.video_id != None)).count(),
#         "update_likes": db.exec(select(Like).where(Like.update_id != None)).count(),
#     }


def delete_event(db: Session, event_id: int) -> dict:
    event = db.get(Event, event_id)
    if event:
        db.delete(event)
        db.commit()

    return StatusJSON(status='ok')
