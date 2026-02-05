from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import RegisterSchema, LoginSchema, TokenSchema
from app.schemas.user import UserRead
from app.services.user import UserService
from app.repositories.user import UserRepository
from app.core.dependencies import get_db, get_jwt_auth_manager, get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead)
async def register_user(register_data: RegisterSchema, db: AsyncSession = Depends(get_db)):
    user_service = UserService(UserRepository(db))
    user = await user_service.register_user(
        email=register_data.email,
        password=register_data.password
    )
    return user

@router.post("/login", response_model=TokenSchema)
async def login_user(
    payload: LoginSchema,
    db: AsyncSession = Depends(get_db),
    auth_manager=Depends(get_jwt_auth_manager),
):
    user_service = UserService(UserRepository(db))
    user = await user_service.authenticate_user(
        email=payload.email,
        password=payload.password
    )
    return {
        "access_token": auth_manager.create_access_token({"sub": user.email}),
        "refresh_token": auth_manager.create_refresh_token({"sub": user.email}),
    }

@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user