from sqlmodel import Session
from app.storage.models import Like


def unlike_item(db: Session, like_id: int) -> dict:
    event = db.get(Like, like_id)
    if event:
        db.delete(event)
        db.commit()

    return {"message": "Unliked"}
