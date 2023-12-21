from typing import List, Optional

from models import Store, Category, Product

from schemas.stores.store import StoreSchemaCreate, StoreSchemaUpdate
from schemas.stores.category import CategoriesSchemaCreate, CategoriesSchemaUpdate
from schemas.stores.product import ProductSchemaCreate, ProductSchemaUpdate
from repositories.base.unit_of_work import UnitOfWork


class StoresService:
    # Store
    async def create_store(self, uow: UnitOfWork, store_schema: StoreSchemaCreate) -> Store:
        async with uow:
            store = await uow.stores.create(store_schema)
            await uow.commit()
            return store

    async def get_stores(self, uow: UnitOfWork, offset: int = 0, limit: Optional[int] = None) -> List[Store]:
        async with uow:
            stores = await uow.stores.get_all(offset=offset, limit=limit)
            return stores

    async def get_store(self, uow: UnitOfWork, store_id: int) -> Store:
        async with uow:
            store = await uow.stores.get(store_id)
            return store

    async def edit_store(self, uow: UnitOfWork, store_id: int, store_schema: StoreSchemaUpdate) -> Store:
        async with uow:
            store = await uow.stores.edit(store_id, store_schema)
            await uow.commit()
            return store

    async def delete_store(self, uow: UnitOfWork, store_id: int):
        async with uow:
            await uow.stores.delete(store_id)
            await uow.commit()

    # Category
    async def create_category(self, uow: UnitOfWork, category_schema: CategoriesSchemaCreate) -> Category:
        async with uow:
            category = await uow.categories.create(category_schema)
            await uow.commit()
            return category

    async def get_categories(self, uow: UnitOfWork, offset: int = 0, limit: Optional[int] = None) -> List[Category]:
        async with uow:
            categories = await uow.categories.get_all(offset=offset, limit=limit)
            return categories

    async def get_store_categories(self, uow: UnitOfWork, store_id: int, offset: int = 0, limit: Optional[int] = None) -> List[Product]:
        async with uow:
            categories = await uow.categories.get_all_by_store(store_id=store_id, offset=offset, limit=limit)
            return categories

    async def get_category(self, uow: UnitOfWork, category_id: int) -> Category:
        async with uow:
            category = await uow.categories.get(category_id)
            return category

    async def edit_category(self, uow: UnitOfWork, category_id: int, category_schema: CategoriesSchemaUpdate) -> Category:
        async with uow:
            category = await uow.categories.edit(category_id, category_schema)
            await uow.commit()
            return category

    async def delete_category(self, uow: UnitOfWork, category_id: int):
        async with uow:
            await uow.categories.delete(category_id)
            await uow.commit()

    # Product
    async def create_product(self, uow: UnitOfWork, product_schema: ProductSchemaCreate) -> Product:
        async with uow:
            product = await uow.products.create(product_schema)
            await uow.commit()
            return product

    async def get_products(self, uow: UnitOfWork, offset: int = 0, limit: Optional[int] = None) -> List[Product]:
        async with uow:
            products = await uow.products.get_all(offset=offset, limit=limit)
            return products

    async def get_category_products(self, uow: UnitOfWork, category_id: int, offset: int = 0, limit: Optional[int] = None) -> List[Product]:
        async with uow:
            products = await uow.products.get_all_by_category(category_id=category_id, offset=offset, limit=limit)
            return products

    async def get_product(self, uow: UnitOfWork, product_id: int) -> Product:
        async with uow:
            product = await uow.products.get(product_id)
            return product

    async def edit_product(self, uow: UnitOfWork, product_id: int, product_schema: ProductSchemaUpdate) -> Product:
        async with uow:
            product = await uow.products.edit(product_id, product_schema)
            await uow.commit()
            return product

    async def delete_product(self, uow: UnitOfWork, product_id: int):
        async with uow:
            await uow.products.delete(product_id)
            await uow.commit()