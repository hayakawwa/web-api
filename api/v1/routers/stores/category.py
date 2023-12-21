from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.responses import JSONResponse

from api.utils.sockets import notify_clients
from api.utils.dependencies import UOWDep
from schemas.stores.category import CategoriesSchema, CategoriesSchemaCreate, CategoriesSchemaUpdate
from services.stores import StoresService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post("/", response_model=CategoriesSchema)
async def create_category(uow: UOWDep, category_schema: CategoriesSchemaCreate):
    category = await StoresService().create_category(uow, category_schema)
    await notify_clients(f"Category created: {category.title} (Store ID: {category.store_id})")
    return category


@router.get("/", response_model=List[CategoriesSchema])
async def read_categories(uow: UOWDep, offset: int = 0, limit: int = 10):
    categories = await StoresService().get_categories(uow, offset=offset, limit=limit)
    return categories


@router.get("/store/{store_id}/", response_model=List[CategoriesSchema])
async def read_store_categories(uow: UOWDep, store_id: int, offset: int = 0, limit: int = 10):
    try:
        products = await StoresService().get_store_categories(uow, store_id=store_id, offset=offset, limit=limit)
        return products
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Categories not found")


@router.get("/{category_id}", response_model=CategoriesSchema)
async def read_category(uow: UOWDep, category_id: int):
    try:
        category = await StoresService().get_category(uow, category_id)
        return category
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Category not found")


@router.patch("/{category_id}", response_model=CategoriesSchema)
async def update_category(uow: UOWDep, category_id: int, category_schema: CategoriesSchemaUpdate):
    try:
        category = await StoresService().edit_category(uow, category_id, category_schema)
        await notify_clients(f"Category updated: {category.title} (Store ID: {category.store_id})")
        return category
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Category not found")


@router.delete("/{category_id}")
async def delete_category(uow: UOWDep, category_id: int):
    try:
        await StoresService().delete_category(uow, category_id)

        await notify_clients(f"Category deleted: ({category_id} ID)")

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"product": "Category deleted successfully"})
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Category not found")
