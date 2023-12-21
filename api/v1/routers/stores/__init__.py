from fastapi import APIRouter

from .store import router as store_router
from .category import router as category_router
from .product import router as product_router

# Определение основного роутера
router = APIRouter()

# Добавление роутеров с условиями по ID
router.include_router(store_router)
router.include_router(category_router, prefix="/stores")
router.include_router(product_router, prefix="/stores/categories")
