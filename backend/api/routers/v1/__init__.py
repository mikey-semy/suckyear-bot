from fastapi import APIRouter
from . import posts, users, tags, bot

__all__ = ["posts", "users", "tags", "bot"]

def get_routers() -> APIRouter:
    router = APIRouter()
    
    for module in __all__:
        module_router = getattr(globals()[module], "router")
        router.include_router(module_router)
    
    return router