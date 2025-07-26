from sqlmodel import Session, select
from app.storage.models import Admin


def get_admin(db: Session, username: str) -> Admin | None:
    return db.exec(select(Admin).where(Admin.username == username)).first()
