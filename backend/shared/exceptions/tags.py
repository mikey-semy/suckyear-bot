from fastapi import HTTPException

class TagNotFoundError(HTTPException):
    def __init__(self, tag_id: int):
        super().__init__(
            status_code=404,
            detail=f"Тег с ID {tag_id} не найден"
        )

class DuplicateTagError(HTTPException):
    def __init__(self, tag_name: str):
        super().__init__(
            status_code=409,
            detail=f"Тег с именем {tag_name} уже существует"
        )