from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StoreSchemaBase(BaseModel):
    title: str
    author_id: int


class StoreSchemaCreate(StoreSchemaBase):
    pass


class StoreSchemaUpdate(StoreSchemaBase):
    title: Optional[str] = None
    author_id: Optional[int] = None


class StoreSchema(StoreSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
