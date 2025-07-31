from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session
from typing import Annotated
from app.core.dependencies import get_db
from app.crud import video as videos_crud
from app.schemas.comment import CommentPublic, CommentCreate
from app.schemas.like import LikePublic
from app.schemas.video import VideoCombined, VideoPublicWithRel

router = APIRouter()


@router.get("/")
def get_all_videos(
    db: Annotated[Session, Depends(get_db)]
) -> list[VideoPublicWithRel]:
    return videos_crud.get_all_videos(db)


@router.get('/recent')
def fetch_recent_videos(
    db: Annotated[Session, Depends(get_db)]
) -> list[VideoPublicWithRel]:
    return videos_crud.get_recent_videos(db)


@router.get("/{video_id}")
def get_video(
    video_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> VideoCombined:
    video = videos_crud.get_video_and_increment_views(db, video_id)
    if video:
        return video

    raise HTTPException(status_code=404, detail="Video not found")


@router.get("/{video_id}/views")
def get_video_views(
    video_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> int:
    return videos_crud.get_view_count_for_video(db, video_id)


@router.post("/{video_id}/comments")
def comment_on_video(
    video_id: int,
    content: CommentCreate,
    db: Annotated[Session, Depends(get_db)]
) -> CommentPublic:
    return videos_crud.comment_on_video(db, video_id, content)


@router.get("/{video_id}/comments")
def get_video_comments(
    video_id: int, db: Annotated[Session, Depends(get_db)]
) -> list[CommentPublic]:
    return videos_crud.get_comments_for_video(db, video_id)


@router.post("/{video_id}/likes")
def like_video(
    video_id: int,
    db: Annotated[Session, Depends(get_db)]
) -> LikePublic:
    return videos_crud.like_video(db, video_id)


@router.get("/{video_id}/likes")
def get_video_likes(
    video_id: int, db: Annotated[Session, Depends(get_db)]
) -> int:
    return videos_crud.get_like_count_for_video(db, video_id)
