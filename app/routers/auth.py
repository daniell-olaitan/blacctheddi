from fastapi import Depends, APIRouter, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token, PWDReset
from app.core.utils import create_access_token, verify_password, get_password_hash
from datetime import timedelta
from sqlmodel import Session
from app.schemas.common import StatusJSON
from app.core.dependencies import get_db, verify_admin
from app.crud.admin import get_admin

ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()


@router.post("/login")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    admin = get_admin(db=db, username=form_data.username)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username"
        )

    if not verify_password(form_data.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/change-password", dependencies=[Depends(verify_admin)])
def change_admin_password(
    user_details: PWDReset,
    db: Annotated[Session, Depends(get_db)],
) -> StatusJSON:
    admin = get_admin(db=db, username=user_details.username)
    if admin:
        admin.password = get_password_hash(user_details.password)
        db.add(admin)
        db.commit()

        return StatusJSON(status='ok')
    return StatusJSON(status='error')
