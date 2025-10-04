from http import HTTPStatus
from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from financial_app.common.security import get_password_hash

from .models import User
from .schemas import UserList, UserPublic, UserSchema


def get_all_users(session: Session, limit: int, offset: int) -> UserList:
    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


def get_user_by_id(session: Session, user_uuid: str) -> UserPublic:
    converted_uuid = UUID(user_uuid)

    user = session.scalar(select(User).where(User.id == converted_uuid))

    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user


def create_user(session: Session, user_schema: UserSchema) -> UserPublic:
    db_user = session.scalar(
        select(User).where(
            (
                user_schema.username == User.username
                or user_schema.email == User.email
            )
        )
    )

    if db_user is not None:
        if db_user.username == user_schema.username:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST, detail='Username already exists'
            )

        raise HTTPException(
            HTTPStatus.BAD_REQUEST, detail='Email already exists'
        )

    db_user = User(
        username=user_schema.username,
        name=user_schema.name,
        email=user_schema.email,
        password=get_password_hash(user_schema.password),
        role=user_schema.role,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
