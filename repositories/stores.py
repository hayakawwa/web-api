from sqlalchemy import select

from models import Store, Category, Product
from repositories.base.repository import SQLAlchemyRepository


class StoresRepository(SQLAlchemyRepository):
    model = Store


class CategoriesRepository(SQLAlchemyRepository):
    model = Category

    async def get_all_by_store(self, store_id: int, offset: int = 0, limit: int | None = None):
        stmt = select(self.model).offset(offset=offset).filter_by(store_id=store_id)

        if limit:
            stmt = stmt.limit(limit=limit)

        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items


class ProductsRepository(SQLAlchemyRepository):
    model = Product

    async def get_all_by_category(self, category_id: int, offset: int = 0, limit: int | None = None):
        stmt = select(self.model).offset(offset=offset).filter_by(category_id=category_id)

        if limit:
            stmt = stmt.limit(limit=limit)

        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items
