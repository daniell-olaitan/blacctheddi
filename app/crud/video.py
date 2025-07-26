from sqlmodel import Session, select
from app.storage.models import Video, Comment, Like
from app.schemas.comment import CommentBase


def get_recent_videos(db: Session) -> list[Video]:
    return db.exec(select(Video).order_by(Video.timestamp.desc())).all()


def get_video_and_increment_views(db: Session, video_id: int) -> Video:
    video = db.get(Video, video_id)
    if video:
        video.views += 1
        db.add(video)
        db.commit()
        db.refresh(video)

    return video


def get_like_count_for_video(db: Session, video_id: int) -> int:
    return db.exec(select(Like).where(Like.video_id == video_id)).all().count()


def get_view_count_for_video(db: Session, video_id: int) -> int:
    video = db.get(Video, video_id)
    return video.views if video else 0


def get_related_videos(db: Session, video_id: int) -> list[Video]:
    videos = db.exec(select(Video).order_by(Video.views.desc())).all()
    return [v for v in videos if v.id != video_id][:5]


def comment_on_video(
    db: Session,
    video_id: int,
    content_data: CommentBase
) -> Comment:
    comment = Comment(**content_data.model_dump(), video_id=video_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


def like_video(db: Session, video_id: int) -> dict:
    like = Like(video_id=video_id)
    db.add(like)
    db.commit()

    return {"message": "Liked"}
