from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from backend.settings import settings

class BlockDocsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not settings.docs_access and request.url.path in ["/docs", "/redoc"]:
            return JSONResponse(status_code=403, content={"detail": "Доступ к документации запрещён."})
        response = await call_next(request)
        return response