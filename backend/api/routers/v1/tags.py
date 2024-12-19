from typing import List, Dict
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from backend.shared.database.session import get_async_session
from backend.shared.schemas.tags import TagSchema
from backend.shared.services.tags import TagService

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagSchema)
async def add_tags(
    tag_names: List[str],
    session: AsyncSession = Depends(get_async_session)
) -> TagSchema:
    """
    Добавляет новые теги в базу данных.
    
    Args:
        tag_names (List[str]): Список названий тегов.
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        TagSchema: Схема тега.
    
    Raises:
        HTTPException: Если не удалось создать теги.
    """
    try:
        tag_ids = await TagService(session).add_tags(tag_names)
        return await TagService(session).get_tags_by_ids(tag_ids)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Не удалось создать теги: {str(e)}"
        ) from e

@router.get("/{post_id}/tags", response_model=List[TagSchema]) 
async def get_post_tags(
    post_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> List[TagSchema]:
    """
    Получает теги поста по его ID.
    
    Args:
        post_id (int): ID поста.
        session (AsyncSession): Асинхронная сессия базы данных.
        
    Returns:
            List[TagSchema]: Список тегов поста.
    Raises:
        HTTPException: Если не удалось получить теги поста.
    """
    try:
        return await TagService(session).get_tags_by_post_id(post_id)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Не удалось получить теги поста: {str(e)}"
        ) from e

@router.post("/post-tags")
async def add_post_tags(
    post_tag_pairs: List[Dict[str, int]],
    session: AsyncSession = Depends(get_async_session)
) -> Dict[str, str]:
    """
    Добавляет теги к посту.

    Args:
        post_tag_pairs (List[Dict[str, int]]): Список пар "пост-тег".
        session (AsyncSession): Асинхронная сессия базы данных.
    
    Returns:
        Dict[str, str]: Статус операции.

    Raises:
        HTTPException: Если не удалось связать теги с постом.
    """
    try:
        await TagService(session).add_post_tags(post_tag_pairs)
        return {"status": "success"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Не удалось связать теги с постом: {str(e)}"
        ) from e
