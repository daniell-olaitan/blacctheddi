from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.storage.database import create_db
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, admin, video, update, event, like


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db()
    yield


app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

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
app.include_router(like.router, prefix='/likes', tages=["Like"])
