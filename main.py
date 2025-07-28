import os

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.storage.database import create_db
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, admin, video, update, event, like
from app.schemas.common import StatusJSON
from app.storage.database import engine
from app.storage.models import Admin
from sqlmodel import Session
from app.crud.admin import get_admin
from app.core.utils import get_settings
from fastapi.staticfiles import StaticFiles

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db()

    # Create default admin if not available
    db = Session(engine)
    admin_user = get_admin(db, settings.admin_user)
    if not admin_user:
        admin_user = Admin(
            username=settings.admin_user,
            password=settings.admin_pwd
        )

        db.add(admin_user)
        db.commit()
        db.close()

    yield


os.makedirs("uploads/videos", exist_ok=True)
os.makedirs("uploads/images", exist_ok=True)

app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(video.router, prefix="/tvs", tags=["TV"])
app.include_router(update.router, prefix="/updates", tags=["Live Update"])
app.include_router(event.router, prefix="/events", tags=["Event"])
app.include_router(like.router, prefix='/likes', tags=["Like"])


# Check API status
@app.get('/')
def app_status() -> StatusJSON:
    return StatusJSON(status='active')
