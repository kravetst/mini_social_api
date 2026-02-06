from app.repositories.post import PostRepository
from app.repositories.like import LikeRepository
from app.schemas.post import PostRead
from app.schemas.user import UserRead
from app.core.redis import get_redis
import json

CACHE_TTL = 30  # cache for 30 seconds


class PostService:
    def __init__(
            self, post_repo: PostRepository,
            like_repo: LikeRepository | None = None
    ):
        self.post_repo = post_repo
        self.like_repo = like_repo

    async def create_post(self, title: str, content: str, author_id: int) -> PostRead:
        post = await self.post_repo.create(title, content, author_id)
        # invalidate cache after creating post
        redis = get_redis()
        keys = await redis.keys("posts:*")
        if keys:
            await redis.delete(*keys)
        return PostRead(
            id=post.id,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            author=post.author,  # Pydantic UserRead is here
            likes_count=0,
        )

    async def get_posts(
        self,
        limit: int = 10,
        offset: int = 0,
        author_id: int | None = None,
        search: str | None = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> list[PostRead]:

        redis = get_redis()
        cache_key = f"posts:{limit}:{offset}:{author_id}:{search}:{sort}:{order}"

        cached = await redis.get(cache_key)
        if cached:
            # returning data from cache
            posts_data = json.loads(cached)
            return [PostRead(**p) for p in posts_data]

        # if there is no cache, take from the DB
        posts = await self.post_repo.list(limit, offset, author_id, search, sort, order)

        # stored in Redis
        await redis.set(
            cache_key, json.dumps([p.model_dump() for p in posts]), ex=CACHE_TTL
        )

        return posts

    async def get_post_by_id(self, post_id: int) -> PostRead | None:
        post = await self.post_repo.get_by_id(post_id)
        if not post:
            return None

        likes_count = 0
        if self.like_repo:
            likes_count = await self.like_repo.count_likes(post.id)

        return PostRead(
            id=post.id,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            author=UserRead(id=post.author.id, email=post.author.email),
            likes_count=likes_count
        )
