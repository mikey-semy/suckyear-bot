from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.shared.models.posts import PostModel
from backend.shared.schemas.posts import PostSchema, PostCreateSchema, PostStatus
from .base import BaseService, BaseDataManager

class PostService(BaseService):
    
    async def create_post(self, post: PostCreateSchema, user_id: int) -> PostSchema:
        return PostDataManager(self.session).create_post(post, user_id)
    
    def get_post(self, post_id: int) -> PostSchema:
        return PostDataManager(self.session).get_post(post_id)

    def get_posts(self) -> List[PostSchema]:
        return PostDataManager(self.session).get_posts()


class PostDataManager(BaseDataManager):
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, PostSchema)
    
    async def create_post(self, post: PostCreateSchema, user_id: int) -> PostSchema:
        post_data = post.model_dump()
        post_data['user_id'] = user_id
        post_data['status'] = PostStatus.CHECKING
        post_model = PostModel(**post_data)
        return await self.add_one(post_model)
    
    def get_post(self, post_id: int) -> PostSchema:
        statement = select(PostModel).where(PostModel.id == post_id)
        return self.get_one(statement)

    def get_posts(self) -> List[PostSchema]:
        schemas: List[PostSchema] = list()
        statement = select(PostModel)
        for model in self.get_all(statement):
            schemas.append(PostSchema(**model.to_dict()))
        return schemas
