from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from backend.shared.schemas.users import UserSchema, CreateUserSchema, TokenSchema
from backend.shared.services.base import BaseService, BaseDataManager
from backend.shared.models.users import UserModel
from backend.shared.exceptions.users import (
    TokenMissingError,
    InvalidCredentialsError,
    TokenExpiredError,
    AuthenticationError,
)
from backend.settings import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl=settings.auth_url, auto_error=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashingMixin:
    """
    Миксин для хеширования и проверки паролей.
    
    Этот миксин предоставляет методы для хеширования и проверки паролей с использованием bcrypt.
    
    Methods:
        bcrypt: Хеширует пароль с использованием bcrypt.
        verify: Проверяет хешированный пароль с использованием bcrypt.  
    """

    @staticmethod
    def bcrypt(password: str) -> str:
        """ 
        Генерирует хеш пароля с использованием bcrypt.
        
        Args:
            password: Пароль для хеширования.

        Returns:
            Хеш пароля.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        """
        Проверяет, соответствует ли переданный пароль хешу.
        Args:
            hashed_password: Хеш пароля.
            plain_password: Пароль для проверки.

        Returns:
            True, если пароль соответствует хешу, иначе False.
        """
        return pwd_context.verify(plain_password, hashed_password)

class AuthService(HashingMixin, BaseService):
    """
    Сервис для аутентификации пользователей.
    
    Этот класс предоставляет методы для аутентификации пользователей, включая создание нового пользователя,
    аутентификацию пользователя и получение токена доступа.
    
    Args:
        session: Асинхронная сессия для работы с базой данных.
    
    Methods:
        loogin_telegram_user: Авторизует или создает пользователя через Telegram и возвращает токен.
        
        create_web_user: Создает нового пользователя через веб-интерфейс и возвращает токен.
        create_telegram_user: Создает нового пользователя через Telegram и возвращает токен.
        
        authenticate: Аутентифицирует пользователя.
        get_token: Получает токен доступа.
        
    """
    async def create_web_user(self, user: CreateUserSchema) -> UserSchema:
        """
        Создает нового пользователя в базе данных с использованием данных web формы.
        
        Args:
            user: Данные нового пользователя.
        
        Returns:
            Экземпляр созданного пользователя.
        """
        user_model = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=self.bcrypt(user.password)
        )
        return await AuthDataManager(self.session).add_user(user_model)
    
    
    async def create_telegram_user(self, chat_id: int, username: str) -> UserSchema:
        """
        Создает нового пользователя в базе данных с использованием данных Telegram.
        
        Args:
            chat_id: ID чата пользователя.
            username: Имя пользователя.

        Returns:
            Экземпляр созданного пользователя.
        """
        user_model = UserModel(
            chat_id=chat_id,
            username=username
        )
        return await AuthDataManager(self.session).add_user(user_model)
        
        
    async def authenticate(
        self, 
        login: OAuth2PasswordRequestForm = Depends()
    ) -> TokenSchema:
        """
        Аутентифицирует пользователя по логину и паролю и возвращает токен.

        Args:
            login: Данные для аутентификации пользователя.

        Returns:
            Токен доступа.
        """
        user = await AuthDataManager(self.session).get_user_by_email(login.username) #! login.username ?= email
    
        if not user or not user.hashed_password:
            raise HTTPException(status_code=401, detail="Неверные учетные данные")
        
        if not self.verify(user.hashed_password, login.password):
            raise HTTPException(status_code=401, detail="Неверные учетные данные")
        
        access_token = self._create_access_token(user)
        return TokenSchema(access_token=access_token, token_type="bearer")
    
    async def login_telegram_user(self, chat_id: int, username: str) -> TokenSchema:
        """
        Аутентифицирует или создает пользователя через Telegram и возвращает токен.
        Args:
            chat_id: Идентификатор пользователя в Telegram.
            username: Имя пользователя в Telegram.

        Returns:
            Токен доступа.
        """
        user = await AuthDataManager(self.session).get_user_by_chat_id(chat_id)

        if not user:
            user = await self.create_telegram_user(chat_id, username)

        access_token = self._create_access_token(user)
        
        return TokenSchema(access_token=access_token, token_type="bearer")

    def _create_access_token(self, user: UserSchema) -> str:
        """
        Создает токен доступа для пользователя.

        Args:
            user: Данные пользователя.
        
        Returns:
            Токен доступа.
        """
        payload = {
            "sub": str(user.id),
            "username": user.username,
            "chat_id": user.chat_id,
            "role": user.role,
            "expires_at": self._expiration_time()
    }
        
        return jwt.encode(
            payload,
            key=settings.token_key.get_secret_value(),
            algorithm=settings.token_algorithm
        )
    
    @staticmethod
    def _expiration_time() -> str:
        """
        Получает время истечения срока действия токена.
        
        Returns:
             Время истечения срока действия токена в формате строки.
        """
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.token_expire_minutes)
        
        return expires_at.strftime("%Y-%m-%d %H:%M:%S")
    
class AuthDataManager(BaseDataManager[UserSchema]):
    """
    Класс для работы с данными пользователей в базе данных.

    Args:
        session: Асинхронная сессия для работы с базой данных.
        schema: Схема данных пользователя.
        model: Модель данных пользователя.
    
    Methods:
        add_user: Добавляет нового пользователя в базу данных.
        get_user_by_email: Получает пользователя по email.
        get_user_by_chat_id: Получает пользователя по chat_id.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(
            session=session,
            schema=UserSchema,
            model=UserModel
        )

    async def add_user(self, user: UserModel) -> None:
        """
        Добавляет нового пользователя в базу данных.

        Args:
            user: Пользователь для добавления.
        
        Returns:
            None
        """
        await self.add_one(user)
    
    async def get_user_by_email(self, email: str) -> UserSchema:
        """
        Получает пользователя по email.
        
        Args:
            email: Email пользователя.

        Returns:
            Данные пользователя.
        """
        statement = select(self.model).where(self.model.email == email)
        return await self.get_one(statement)

    async def get_user_by_chat_id(self, chat_id: int) -> UserSchema:
        """
        Получает пользователя по chat_id.
        
        Args:
            chat_id: ID чата пользователя.
        
        Returns:
            Данные пользователя.
        """
        statement = select(self.model).where(self.model.chat_id == chat_id) 
        return await self.get_one(statement)


async def get_current_user(token: str = Depends(oauth2_schema)) -> UserSchema | None:
    """
    Получает данные текущего пользователя.

    Args:
        token: Токен доступа.

    Returns:
        Данные текущего пользователя.
    """
    if token is None:
        raise TokenMissingError()

    try:
        payload = jwt.decode(
            token=token,
            key=settings.token_key.get_secret_value(),
            algorithms=[settings.token_algorithm]
        )
        
        user_id = int(payload.get("sub"))
        username = payload.get("username") 
        chat_id = payload.get("chat_id")
        role = payload.get("role")
        expires_at = payload.get("expires_at")

        if user_id is None:
            raise InvalidCredentialsError()

        if is_expired(expires_at):
            raise TokenExpiredError()

        return UserSchema(
            id=user_id,
            username=username,
            chat_id=chat_id,
            role=role
        )

    except JWTError as exc:
        raise AuthenticationError() from exc


def is_expired(expires_at: str) -> bool:
    """
    Проверяет, истек ли срок действия токена.

    Args:
        expires_at: Время истечения срока действия токена.
             
    Returns:
             True, если токен истек, иначе False.
    """
    return datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S") < datetime.now(timezone.utc)