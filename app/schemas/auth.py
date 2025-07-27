from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class PWDReset(BaseModel):
    username: str
    password: str
