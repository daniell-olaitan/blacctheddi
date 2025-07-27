from pydantic import BaseModel


class Analytics(BaseModel):
    total_views: int
    total_updates: int
    total_videos: int
