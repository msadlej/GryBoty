from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models.user import get_user_by_username
from app.schemas.user import TokenData, DBUser
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from typing import Annotated, Any
import jwt


SECRET_KEY = "1365209f8d9033360934a875f588f8075296a115e712beee38a5a23c527a0dd4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    result: bool = pwd_context.verify(plain_password, hashed_password)
    return result


def get_password_hash(password: str) -> str:
    hashed_password: str = pwd_context.hash(password)
    return hashed_password


def authenticate_user(username: str, password: str) -> DBUser | None:
    user: DBUser | None = get_user_by_username(username)

    if user is None or not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode: dict[str, Any] = data.copy()
    expire: datetime = datetime.now(timezone.utc)

    if expires_delta is not None:
        expire += expires_delta
    else:
        expire += timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> DBUser:
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user: DBUser | None = get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[DBUser, Depends(get_current_user)]
) -> DBUser:
    if current_user.is_banned:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
