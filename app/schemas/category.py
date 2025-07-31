from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class CategoryBase(SQLModel):
    name: str = Field(index=True, unique=True)


class CategoryPublic(CategoryBase):
    id: int
