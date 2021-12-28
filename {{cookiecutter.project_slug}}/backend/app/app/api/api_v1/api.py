from fastapi import APIRouter

from app.api.api_v1.endpoints import login, utils
from app.users.endpoints import router as users_router
from app.items.endpoints import router as items_router

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items_router, prefix="/items", tags=["items"])
