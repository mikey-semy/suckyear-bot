from fastapi import APIRouter
from settings import settings

from api.routers import v1
# from api.routers import v2 - когда появится, тогда и раскомментируем

def all_routers() -> APIRouter:
    """
    Возвращает APIRouter, содержащий все роутеры в папке routers для FastAPI.
        
    Returns:
        APIRouter: APIRouter, содержащий все роутеры приложения.
    """
    router = version_router = APIRouter()
    
    for version in settings.api_versions:
        if version == "v1":
            version_router = v1.get_routers()
        # if version == "v2":
        #     version_router = v2.get_routers()
    
        router.include_router(
            router=version_router,
            prefix=f"/api/{version}"
        )
    
    return router