from app.repositories.post import PostRepository
from app.repositories.like import LikeRepository


class PostService:
    def __init__(self, post_repo: PostRepository, like_repo: LikeRepository | None = None):
        self.post_repo = post_repo
        self.like_repo = like_repo

    async def create_post(self, title: str, content: str, author_id: int):
        return await self.post_repo.create(title, content, author_id)

    async def get_posts(
        self,
        limit: int = 10,
        offset: int = 0,
        author_id: int | None = None,
        search: str | None = None,
        sort: str = "created_at",
        order: str = "desc",
    ):
        posts = await self.post_repo.list(limit, offset, author_id, search, sort, order)
        # Add likes_count for each post
        if self.like_repo:
            for post in posts:
                post.likes_count = await self.like_repo.count_likes(post.id)
        return posts
    