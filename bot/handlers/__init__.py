from aiogram import Router
from . import base, fails

__all__ = ["base", "fails"]

def all_handlers() -> Router:
    router = Router()
    
    for module in __all__:
        module_router = getattr(globals()[module], "router")
        router.include_router(module_router)
    
    return router