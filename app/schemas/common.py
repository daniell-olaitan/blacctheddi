from pydantic import BaseModel


class StatusJSON(BaseModel):
    status: str
