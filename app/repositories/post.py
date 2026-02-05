from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.post import Post


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, title: str, content: str, author_id: int) -> Post:
        new_post = Post(title=title, content=content, author_id=author_id)
        self.db.add(new_post)
        await self.db.commit()
        await self.db.refresh(new_post)
        return new_post

    async def get_by_id(self, post_id: int) -> Post | None:
        stmt = select(Post).where(Post.id == post_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
            self,
            limit: int = 10,
            offset: int = 0,
            author_id: int | None = None,
            search: str | None = None,
            sort: str = "created_at",
            order: str = "desc",
    ):
        stmt = select(Post)
        if author_id:
            stmt = stmt.where(Post.author_id == author_id)
        if search:
            stmt = stmt.where(Post.title.ilike(f"%{search}%") | Post.content.ilike(f"%{search}%"))

        # Sort
        if sort == "likes":
            stmt = stmt.order_by(Post.likes)
        else:
            stmt = stmt.order_by(Post.created_at.desc() if order == "desc" else Post.created_at.asc())

        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return result.scalars().all()
