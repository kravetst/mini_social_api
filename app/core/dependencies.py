from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt
from app.db.session import get_db
from app.models.user import User
from app.core.config import settings
from app.core.security import create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class JWTAuthManager:
    """A manager for generating and decoding JWT tokens"""

    def create_access_token(self, data: dict):
        return create_access_token(
            data, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    def create_refresh_token(self, data: dict):
        # Refresh token lives 7 days
        return create_access_token(data, expires_delta=timedelta(days=7))

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(
                token,
                settings.JWT_ACCESS_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )


# Depends
def get_jwt_auth_manager():
    return JWTAuthManager()


async def _get_user_from_token(token: str, db: AsyncSession):
    manager = JWTAuthManager()
    payload = manager.decode_token(token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    """Get current user by access token"""
    return await _get_user_from_token(token, db)


async def get_current_user_by_refresh(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    """Get user by refresh token"""
    return await _get_user_from_token(token, db)
