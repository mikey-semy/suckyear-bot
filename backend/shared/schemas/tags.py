from typing import Optional
from shared.schemas.base import BaseSchema

class TagSchema(BaseSchema):
    """
    Схема для тегов.
    Этот класс определяет структуру данных, необходимых для представления тегов.
    Args:
        id (int): Уникальный идентификатор тега.
        name (str): Название тега.
    """
    id: Optional[int]
    name: str