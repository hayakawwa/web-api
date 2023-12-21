from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CategoriesSchemaBase(BaseModel):
    title: str
    author_id: int
    store_id: int


class CategoriesSchemaCreate(CategoriesSchemaBase):
    pass


class CategoriesSchemaUpdate(CategoriesSchemaBase):
    title: Optional[str] = None
    author_id: Optional[int] = None
    store_id: Optional[int] = None


class CategoriesSchema(CategoriesSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
