from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from financial_app.common.security import get_password_hash

from .models import User
from .responses import (
    EmailAlreadyExists,
    InvalidUserId,
    UsernameAlreadyExists,
    UserNotFound,
)
from .schemas import UserList, UserPublic, UserSchema


def get_all_users(session: Session, limit: int, offset: int) -> UserList:
    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


def get_user_by_id(session: Session, user_uuid: str) -> UserPublic:
    converted_uuid = None

    try:
        converted_uuid = UUID(user_uuid)

    except ValueError:
        raise InvalidUserId()

    db_user = session.scalar(select(User).where(User.id == converted_uuid))

    if db_user is None:
        raise UserNotFound()

    return db_user


def get_user_by_username(session: Session, username: str) -> UserPublic:
    db_user = session.scalar(select(User).where(User.username == username))

    if db_user is None:
        raise UserNotFound()

    return db_user


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
            raise UsernameAlreadyExists()

        raise EmailAlreadyExists()

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
