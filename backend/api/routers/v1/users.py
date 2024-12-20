from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from shared.database.session import get_async_session
from shared.schemas.users import TokenSchema, CreateUserSchema
from shared.services.users import AuthService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/telegram/login")
async def telegram_login(
    chat_id: int,
    username: str,
    auth_service: AuthService = Depends()
) -> TokenSchema:
    return await auth_service.login_telegram_user(chat_id, username)

@router.post("")
async def authenticate(
    login: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
    ) -> TokenSchema | None:
    """
    Аутентифицирует пользователя.

    Raises:
        HTTPException: 401 Unauthorized
        HTTPException: 404 Not Found

    Returns:
        Возвращает токен доступа.
    """
    return await AuthService(session).authenticate(login)

@router.post("/create")
async def create_user(
    name: str,
    email: str,
    password: str,
    session: AsyncSession = Depends(get_async_session)
    ) -> None:
    """
    Создает нового пользователя.

    Raises:
        HTTPException: 400 Bad Request

    Returns:
        None
    """
    await AuthService(session).create_web_user(
        CreateUserSchema(name=name, email=email, password=password)
    )