"""
Модуль для аутентификации и регистрации пользователей через REST API.

Этот модуль предоставляет эндпоинты для:
- Аутентификации существующих пользователей с выдачей JWT токена
- Регистрации новых пользователей через веб-интерфейс

Роуты:
- POST /users - Аутентификация пользователя
- POST /users/create - Создание нового пользователя

Зависимости:
- FastAPI для API эндпоинтов
- OAuth2 для аутентификации
- AuthService для бизнес-логики
"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from shared.database.session import get_async_session
from shared.schemas.users import TokenSchema, CreateUserSchema, UserUpdateSchema, UserSchema
from shared.services.users import AuthService, UserService

router = APIRouter(prefix="/users", tags=["Users"])

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

@router.get("/me")
async def get_profile(
    session: AsyncSession = Depends(get_async_session)
    ) -> UserSchema:
    """
    Возвращает информацию о текущем пользователе.

    Returns:
        Возвращает информацию о текущем пользователе.
    """
    return await UserService(session).get_profile()

@router.patch("/me")
async def update_profile(
    data: UserUpdateSchema,
    session: AsyncSession = Depends(get_async_session)

    ) -> UserSchema:
    """
    Обновляет информацию о текущем пользователе.
    Args:
        data: Данные для обновления.

    Returns:
        Обновленные данные пользователя.
    
    """
    return await UserService(session).update_profile(data)
