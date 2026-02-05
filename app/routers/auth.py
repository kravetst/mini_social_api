from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.dependencies import get_jwt_auth_manager, get_current_user
from app.core.security import get_password_hash, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import RegisterSchema, LoginSchema
from app.schemas.user import UserRead

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=UserRead)
async def register_user(payload: RegisterSchema, db: AsyncSession = Depends(get_db)):
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == payload.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Creating a user
    hashed_password = get_password_hash(payload.password)
    new_user = User(
        email=payload.email, hashed_password=hashed_password, is_active=True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@auth_router.post("/login")
async def login(payload: LoginSchema, db: AsyncSession = Depends(get_db),
                auth_manager=Depends(get_jwt_auth_manager)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=401, detail="User not active")

    access_token = auth_manager.create_access_token({"sub": user.email})
    refresh_token = auth_manager.create_refresh_token({"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token}


@auth_router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user