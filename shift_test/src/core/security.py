from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request, Security
from fastapi.security import OAuth2PasswordBearer, APIKeyCookie
from jose import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt, JWTError

from shift_test.src.crud.user import get_user_by_username, get_user_by_id
from shift_test.src.db.session import get_session
from shift_test.src.models.user import User
from shift_test.src.core.config import settings 



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/", auto_error=False)
cookie_scheme = APIKeyCookie(name="users_access_token", auto_error=False)

def password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=settings.MINUTES_EXPIRE)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt


async def authenticate_user(username: str, password: str, session: AsyncSession) -> User | None:
    user = await get_user_by_username(session=session, username=username)
    if not user or verify_password(plain_password=password, hashed_password=user.password_hash) is False:
        return None
    return user


async def get_token(
    request: Request,
    # header_token: str | None = Security(oauth2_scheme),
    cookie_token: str | None = Security(cookie_scheme),
) -> str:
    
    if cookie_token:
        return cookie_token  # Токен из куки
    
    # для других способов аутентификации, например, через заголовок Authorization
    # if header_token:
    #     return header_token  # Bearer-токен из заголовка
    
    raise HTTPException(status_code=401, detail="Not authenticated")


async def get_current_user(token: str = Depends(get_token), session: AsyncSession = Depends(get_session)) -> User | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is not valid!')

    expire = payload.get('exp')
    if not expire:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired')

    if isinstance(expire, datetime):
        expire_time = expire if expire.tzinfo is not None else expire.replace(tzinfo=timezone.utc)
    else:
        try:
            expire_ts = int(float(expire))
            expire_time = datetime.fromtimestamp(expire_ts, tz=timezone.utc)
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid format for exp in token')

    if expire_time < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User ID not found')

    user = await get_user_by_id(session=session, user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user


async def get_admin_rights(user: User | None = Depends(get_current_user)) -> User | None:
    if user is None or user.is_administrator != True:
        raise HTTPException(
            status_code=403,
            detail="Admin rights required"
        )
    return user

