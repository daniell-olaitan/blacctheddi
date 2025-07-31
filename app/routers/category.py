from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Annotated
from app.core.dependencies import get_db
from app.crud import category as category_crud
from app.schemas.category import CategoryPublic

router = APIRouter()


@router.get('/')
def fetch_all_video_categories(
    db: Annotated[Session, Depends(get_db)]
) -> list[CategoryPublic]:
    return category_crud.get_all_categories(db)
