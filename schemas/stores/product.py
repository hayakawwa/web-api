from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductSchemaBase(BaseModel):
    title: str
    description: str
    author_id: int
    category_id: int


class ProductSchemaCreate(ProductSchemaBase):
    pass


class ProductSchemaUpdate(ProductSchemaBase):
    title: Optional[str] = None
    description: Optional[str] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None


class ProductSchema(ProductSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
