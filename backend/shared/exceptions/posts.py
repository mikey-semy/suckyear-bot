from fastapi import HTTPException

class PostNotFoundError(HTTPException):
    def __init__(self, post_id: int):
        super().__init__(
            status_code=404,
            detail=f"Пост с ID {post_id} не найден"
        )

class PostCreateError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=400,
            detail=f"Не могу создать пост: {message}"
        )

class PostUpdateError(HTTPException):
    def __init__(self, post_id: int, message: str):
        super().__init__(
            status_code=400,
            detail=f"Не могу обновить пост {post_id}: {message}"
        )

class PostDeleteError(HTTPException):
    def __init__(self, post_id: int):
        super().__init__(
            status_code=403,
            detail=f"Нельзя удалить пост {post_id}"
        )