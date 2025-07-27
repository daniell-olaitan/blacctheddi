from sqlmodel import Session
from app.storage.models import Comment, Like
from app.schemas.comment import CommentBase


def comment_on_update(
    db: Session,
    update_id: int,
    content_data: CommentBase
) -> Comment:
    comment = Comment(**content_data.model_dump(), update_id=update_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


def like_update(db: Session, update_id: int) -> dict:
    like = Like(update_id=update_id)
    db.add(like)
    db.commit()

    return like
