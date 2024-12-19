from fastapi import HTTPException

class UserNotFoundError(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=404,
            detail=f"Пользователь с ID {user_id} не найден"
        )

class TokenMissingError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Токен отсутствует"
        )

class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Неверные учетные данные"
        )

class TokenExpiredError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Токен просрочен"
        )

class AuthenticationError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Неверные учетные данные, попробуйте снова"
        )