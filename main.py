from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.storage.database import create_db
# from fastapi_app.core.exception_handlers import handle_validation_exception, handle_httpexception
# from fastapi.exceptions import HTTPException, RequestValidationError


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db()
    yield


app = FastAPI(lifespan=lifespan)

# from fastapi_app.routers.auth import auth_router
# app.include_router(auth_router)
# app.add_exception_handler(HTTPException, handle_httpexception)
# app.add_exception_handler(RequestValidationError, handle_validation_exception)
# app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
