from sqlmodel import Session, select
from app.storage.models import Video, Comment, Like
from app.schemas.comment import CommentBase


def get_recent_videos(db: Session) -> list[Video]:
    return db.exec(select(Video).order_by(Video.timestamp.desc())).all()[:3]


def get_all_videos(db: Session) -> list[Video]:
    return db.exec(select(Video).order_by(Video.timestamp.desc())).all()


def get_video_and_increment_views(db: Session, video_id: int) -> dict:
    video = db.get(Video, video_id)
    if video:
        video.views += 1
        db.add(video)
        db.commit()
        db.refresh(video)

        videos = db.exec(select(Video).order_by(Video.views.desc())).all()
        related_videos = [v for v in videos if v.id != video_id][:5]

        return {
            "video": video,
            "related_videos": related_videos
        }

    return None


def get_like_count_for_video(db: Session, video_id: int) -> int:
    return len(db.exec(select(Like).where(Like.video_id == video_id)).all())


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

    return like
