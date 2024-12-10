from fastapi import APIRouter
from backend.api.routers.v1 import bot
from backend.settings import settings

__all__ = ["bot"]

def all_routers(api_prefix: str = settings.api_prefix) -> APIRouter:
    """
    Возвращает APIRouter, содержащий все роутеры в папке routers для FastAPI.
    
    Attributes:
        api_prefix (str): Префикс для всех роутеров.
        
    Returns:
        APIRouter: APIRouter, содержащий все роутеры приложения.
    """
    router = APIRouter()
    
    for module in __all__:
        module_router = getattr(globals()[module], "router")
        if module == "bot":
            router.include_router(module_router) 
        else:
            router.include_router(module_router, prefix=api_prefix)
    
    return router