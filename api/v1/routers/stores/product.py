from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.responses import JSONResponse

from api.utils.sockets import notify_clients
from api.utils.dependencies import UOWDep
from schemas.stores.product import ProductSchema, ProductSchemaCreate, ProductSchemaUpdate
from services.stores import StoresService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/", response_model=ProductSchema)
async def create_product(uow: UOWDep, product_schema: ProductSchemaCreate):
    product = await StoresService().create_product(uow, product_schema)
    await notify_clients(f"Product created: {product.id} (Category ID: {product.category_id})")
    return product


@router.get("/", response_model=List[ProductSchema])
async def read_products(uow: UOWDep, offset: int = 0, limit: int = 10):
    products = await StoresService().get_products(uow, offset=offset, limit=limit)
    return products


@router.get("/category/{category_id}/", response_model=List[ProductSchema])
async def read_category_products(uow: UOWDep, category_id: int, offset: int = 0, limit: int = 10):
    try:
        products = await StoresService().get_category_products(uow, category_id=category_id, offset=offset, limit=limit)
        return products
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Products not found")


@router.get("/{product_id}", response_model=ProductSchema)
async def read_product(uow: UOWDep, product_id: int):
    product = await StoresService().get_product(uow, product_id)
    return product


@router.patch("/{product_id}", response_model=ProductSchema)
async def update_product(uow: UOWDep, product_id: int, product_schema: ProductSchemaUpdate):
    try:
        product = await StoresService().edit_product(uow, product_id, product_schema)
        await notify_clients(f"Product updated: {product.id} (Category ID: {product.category_id})")
        return product
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product not found")


@router.delete("/{product_id}")
async def delete_product(uow: UOWDep, product_id: int):
    try:
        await StoresService().delete_product(uow, product_id)

        await notify_clients(f"Product deleted: ({product_id} ID)")

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"product": "Product deleted successfully"})
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product not found")
