import jwt

from fastapi import Depends, APIRouter, HTTPException, status
from typing import Annotated
from app.schemas.auth import Token, PWDReset, TokenFull, LoginRequest
from app.core.utils import create_token, verify_password, get_password_hash, get_settings
from datetime import timedelta
from sqlmodel import Session
from app.schemas.common import StatusJSON
from app.core.dependencies import get_db, verify_admin
from app.crud.admin import get_admin
from app.storage.models import Admin

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()
settings = get_settings()


@router.post("/login")
def login_for_access_token(
    payload: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
) -> TokenFull:
    admin = get_admin(db=db, username=payload.username)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username"
        )

    if not verify_password(payload.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )

    refresh_token = create_token(
        data={"sub": admin.username}, expires_delta=timedelta(days=7)
    )

    return TokenFull(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh")
def refresh_token(refresh_token: str) -> Token:
    try:
        payload = jwt.decode(refresh_token, get_settings().secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Issue new access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_token(
            data={"sub": username}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@router.post("/change-password")
def change_admin_password(
    user_details: PWDReset,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[Admin, Depends(verify_admin)],
) -> StatusJSON:
    if verify_password(user_details.old_password, admin.password):
        admin.password = get_password_hash(user_details.new_password)
        db.add(admin)
        db.commit()

        return StatusJSON(status='ok')
    return StatusJSON(status='error')
