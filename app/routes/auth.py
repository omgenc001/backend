from ast import Pass

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.db_connections import get_db
from app.db.tables import User
from app.schemas.users import CreateUser, CreateUserResponse, LoginUser, LoginUserResponse
from app.encrption.encrption import hash_password, verify_password
from app.encrption.jwt import create_access_token, restrict_route


auth_router = APIRouter(tags=["Authentication"])


@auth_router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserResponse,
)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    password = hash_password(user.password)
    new_user = User(
        player_name=user.player_name,
        email=user.email,
        password=password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return CreateUserResponse(
        email=new_user.email,
        player_name=new_user.player_name,
    )


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginUserResponse,
)
def login_user(user: LoginUser, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    password_match = verify_password(user.password, user_db.password)
    if not password_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    access_token = create_access_token({"sub": str(user_db.id)})

    return LoginUserResponse(
        email=user_db.email,
        player_name=user_db.player_name,
        access_token=access_token,
        token_type="bearer",
    )

@auth_router.post(
    "/check_login",
    status_code=status.HTTP_200_OK,
)
def check_logged_in_user(current_user = Depends(restrict_route)):
    if not current_user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "Unauthorized"
            )
    return current_user
    