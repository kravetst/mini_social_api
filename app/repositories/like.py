from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from app.models.like import Like


class LikeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_like(self, user_id: int, post_id: int) -> Like | None:
        stmt = select(Like).where(Like.user_id == user_id, Like.post_id == post_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_like(self, user_id: int, post_id: int) -> Like:
        like = Like(user_id=user_id, post_id=post_id)
        self.db.add(like)
        await self.db.commit()
        await self.db.refresh(like)
        return like

    async def delete_like(self, user_id: int, post_id: int) -> None:
        stmt = delete(Like).where(Like.user_id == user_id, Like.post_id == post_id)
        await self.db.execute(stmt)
        await self.db.commit()

    async def count_likes(self, post_id: int) -> int:
        stmt = select(func.count(Like.id)).where(Like.post_id == post_id)
        result = await self.db.execute(stmt)
        return result.scalar_one()
