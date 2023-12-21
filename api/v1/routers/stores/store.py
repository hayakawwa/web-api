from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.responses import JSONResponse

from api.utils.sockets import notify_clients
from api.utils.dependencies import UOWDep
from schemas.stores.store import StoreSchema, StoreSchemaCreate, StoreSchemaUpdate
from services.stores import StoresService

router = APIRouter(
    prefix="/stores",
    tags=["Stores"],
)


@router.post("/", response_model=StoreSchema)
async def create_store(uow: UOWDep, store_schema: StoreSchemaCreate):
    store = await StoresService().create_store(uow, store_schema)
    await notify_clients(f"Store created: {store.title} (Author ID: {store.author_id})")
    return store


@router.get("/", response_model=List[StoreSchema])
async def read_stores(uow: UOWDep, offset: int = 0, limit: int = 10):
    stores = await StoresService().get_stores(uow, offset=offset, limit=limit)
    return stores


@router.get("/{store_id}", response_model=StoreSchema)
async def read_store(uow: UOWDep, store_id: int):
    store = await StoresService().get_store(uow, store_id)
    return store


@router.patch("/{store_id}", response_model=StoreSchema)
async def update_store(uow: UOWDep, store_id: int, store_schema: StoreSchemaUpdate):
    try:
        store = await StoresService().edit_store(uow, store_id, store_schema)
        await notify_clients(f"Store updated: {store.title} (Author ID: {store.author_id})")
        return store
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Store not found")


@router.delete("/{store_id}")
async def delete_store(uow: UOWDep, store_id: int):
    try:
        await StoresService().delete_store(uow, store_id)

        await notify_clients(f"Store deleted: ({store_id} ID)")

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"product": "Store deleted successfully"})
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Store not found")
