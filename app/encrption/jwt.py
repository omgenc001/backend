from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.db.db_connections import get_db
from app.db.tables import User
from settings.load_env import ACCESS_TIME, ALGORITHM, SECRET_KEY


def create_access_token(data: dict):
    to_encode = data.copy()
    expires_time = datetime.now(timezone.utc) + timedelta(days=float(ACCESS_TIME))
    to_encode.update({"exp": expires_time})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    jwt_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("id")
        if id is None:
            raise jwt_error
        return id
    except JWTError:
        raise jwt_error


def restrict_route(request: Request, db: Session = Depends(get_db)):
    authorization_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
    )

    header = request.headers.get("Authorization")
    if not header:
        raise authorization_error

    parts = header.split()
    if len(parts) != 2:
        raise authorization_error

    bearer, access_token = parts
    if bearer.lower() != "bearer":
        raise authorization_error

    id = verify_token(token=access_token)
    user_db = db.query(User).filter(User.id == id).first()
    if not user_db:
        raise authorization_error

    return user_db