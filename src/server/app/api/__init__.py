from fastapi import APIRouter

from .routers import *

api_router = APIRouter(prefix="/api")
api_router.include_router(test_router)
api_router.include_router(users_router)
api_router.include_router(database_router)
