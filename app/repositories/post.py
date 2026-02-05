from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models.post import Post
from app.models.like import Like
from app.models.user import User
from app.schemas.post import PostRead
from app.schemas.user import UserRead


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
        stmt = (
            select(
                Post,
                User.id.label("author_id"),
                User.email.label("author_email"),
                func.count(Like.id).label("likes_count"),
            )
            .join(User, Post.author_id == User.id)
            .outerjoin(Like, Like.post_id == Post.id)
            .where(Post.id == post_id)
            .group_by(Post.id, User.id)
        )

        result = await self.db.execute(stmt)
        row = result.first()
        if not row:
            return None

        post, author_id, author_email, likes_count = row

        # adding attributes to Post
        post.likes_count = likes_count
        post.author = type("Author", (), {"id": author_id, "email": author_email})()
        return post

    async def list(
        self,
        limit: int = 10,
        offset: int = 0,
        author_id: int | None = None,
        search: str | None = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> list[PostRead]:
        # a basic query with join on author and left join on likes
        stmt = (
            select(
                Post,
                User.id.label("author_id"),
                User.email.label("author_email"),
                func.count(Like.id).label("likes_count"),
            )
            .join(User, Post.author_id == User.id)
            .outerjoin(Like, Like.post_id == Post.id)
            .group_by(Post.id, User.id)
        )

        if author_id:
            stmt = stmt.where(Post.author_id == author_id)
        if search:
            stmt = stmt.where(
                Post.title.ilike(f"%{search}%") | Post.content.ilike(f"%{search}%")
            )

        # Sort
        if sort == "likes":
            stmt = stmt.order_by(
                func.count(Like.id).desc() if order == "desc" else func.count(Like.id).asc()
            )
        else:
            stmt = stmt.order_by(Post.created_at.desc() if order == "desc" else Post.created_at.asc())

        stmt = stmt.limit(limit).offset(offset)

        result = await self.db.execute(stmt)
        rows = result.all()

        # forming the Pydantic PostRead list
        posts_list: list[PostRead] = []
        for post, author_id, author_email, likes_count in rows:
            posts_list.append(
                PostRead(
                    id=post.id,
                    title=post.title,
                    content=post.content,
                    created_at=post.created_at,
                    author=UserRead(id=author_id, email=author_email),
                    likes_count=likes_count,
                )
            )

        return posts_list
