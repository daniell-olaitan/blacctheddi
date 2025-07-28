from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenFull(Token):
    refresh_token: str


class PWDReset(BaseModel):
    old_password: str
    new_password: str
