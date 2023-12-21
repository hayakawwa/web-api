from fastapi import APIRouter

from api.v1.routers.users import router as users_router
from api.v1.routers.stores import router as stores_router

router = APIRouter(prefix='/v1')

router.include_router(users_router)
router.include_router(stores_router)
