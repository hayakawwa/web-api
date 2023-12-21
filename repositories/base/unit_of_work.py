from db import async_session_maker
from repositories.stores import StoresRepository, CategoriesRepository, ProductsRepository
from repositories.users import UsersRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.stores = StoresRepository(self.session)
        self.categories = CategoriesRepository(self.session)
        self.products = ProductsRepository(self.session)

    async def __aexit__(self, *args):
        # await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
