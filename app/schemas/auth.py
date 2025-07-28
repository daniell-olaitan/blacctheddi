from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenFull(Token):
    refresh_token: str


class PWDReset(BaseModel):
    old_password: str
    new_password: str
