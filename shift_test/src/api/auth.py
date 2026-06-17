from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession


from shift_test.src.models.user import User
from shift_test.src.db.session import get_session
from shift_test.src.crud.user import get_user_by_username, create_user
from shift_test.src.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from shift_test.src.core.security import get_current_user, password_hash, create_access_token, authenticate_user
from shift_test.src.schemas.user import UserRead


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=dict)
async def register(
    data: RegisterRequest,
    session: AsyncSession = Depends(get_session)
):
    user = await get_user_by_username(
        session,
        data.username
    )

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists"
        )

    new_user = await create_user(
        session,
        username=data.username,
        password_hash=password_hash(
            data.password
        )
    )

    return {
        "id": new_user.id,
        "username": new_user.username
    }


@router.post("/login")
async def login(
    data: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(
        data.username,
        data.password,
        session
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or invalid password"
        )

    token = create_access_token(
        {
            "sub": str(user.id),
        }
    )

    response.set_cookie(
        key="users_access_token",
        value=token,
        httponly=True,
        max_age=1800,
        secure=False,
        samesite="lax"
    )

    return {'users_access_token': token, 'refresh_token': None}



@router.post("/logout")
async def logout(
    response: Response
):
    response.delete_cookie(
        "users_access_token"
    )

    return {
        "message": "Logged out"
    }


@router.get("/me", response_model=UserRead)
async def get_me(user: User = Depends(get_current_user)):
    return user