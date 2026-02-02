from app.database.post import PostRepository

class PostService:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    async def create_post(self, title: str, content: str, author_id: int):
        # логіка створення поста
        pass