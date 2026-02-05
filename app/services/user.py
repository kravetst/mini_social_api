from app.database.user import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, email: str, password: str):
        # логіка хешування пароля + створення користувача
        pass