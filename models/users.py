from datetime import datetime
from typing import List

from sqlalchemy import DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

    stores: Mapped[List["Store"]] = relationship(back_populates="author", lazy="selectin")
    categories: Mapped[List["Category"]] = relationship(back_populates="author", lazy="selectin")
    products: Mapped[List["Product"]] = relationship(back_populates="author", lazy="selectin")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
