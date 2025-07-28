import jwt
import boto3

from pathlib import Path
from shutil import copyfileobj
from uuid import uuid4
from passlib.context import CryptContext
from config import get_settings
from datetime import timedelta, timezone, datetime
from fastapi import UploadFile, HTTPException

settings = get_settings()

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)

    return encoded_jwt


# File Upload

# r2_client = boto3.client(
#     "s3",
#     endpoint_url=settings.r2_endpoint_url_s3,
#     aws_access_key_id=settings.r2_access_key_id,
#     aws_secret_access_key=settings.r2_secret_access_key
# )


# def store_file(file: UploadFile, file_type: str = 'videos') -> str:
#     try:
#         # Generate unique key with folder prefix
#         key = f"{file_type}/{uuid4()}_{file.filename}"

#         # Upload to R2
#         r2_client.upload_fileobj(
#             Fileobj=file.file,
#             Bucket=settings.r2_bucket_name,
#             Key=key,
#             ExtraArgs={"ContentType": file.content_type}
#         )

#         public_url = f"{settings.r2_public_url}/{key}"
#         return public_url

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# Local storage
def store_file(file: UploadFile, file_type: str = 'videos') -> str:
    try:
        # Define local upload directory
        upload_dir = Path("uploads") / file_type
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename
        filename = f"{uuid4()}_{file.filename}"
        file_path = upload_dir / filename

        # Save file locally
        with file_path.open("wb") as buffer:
            copyfileobj(file.file, buffer)

        # Construct and return public URL
        public_url = f"/uploads/{file_type}/{filename}"
        return public_url

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
