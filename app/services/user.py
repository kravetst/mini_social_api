from fastapi import HTTPException, status
from app.repositories.user import UserRepository
from app.core.security import get_password_hash, verify_password
from app.models.user import User

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, email: str, password: str) -> User:
        # Перевірка, чи користувач вже існує
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        # Хешування пароля
        hashed_password = get_password_hash(password)

        # Створення нового користувача
        new_user = await self.user_repo.create(
            email=email,
            hashed_password=hashed_password
        )
        return new_user

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.user_repo.get_by_email(email)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not active"
            )

        return user
