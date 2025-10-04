from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from financial_app.common.schemas import Message
from financial_app.common.security import get_password_hash

from .models import User
from .responses import (
    EmailAlreadyExists,
    InvalidUserId,
    UsernameAlreadyExists,
    UserNotFound,
)
from .schemas import UserList, UserPublic, UserSchema


def validate_uuid(uuid: str) -> UUID:
    try:
        converted_uuid = UUID(uuid)
        return converted_uuid

    except ValueError:
        raise InvalidUserId()


def get_all_users(session: Session, limit: int, offset: int) -> UserList:
    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


def get_user_by_id(session: Session, user_uuid: str) -> UserPublic:
    converted_uuid = validate_uuid(user_uuid)

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


def delete_user(session: Session, user_uuid: str) -> Message:
    converted_uuid = validate_uuid(user_uuid)

    db_user = session.scalar(select(User).where(User.id == converted_uuid))

    if db_user is None:
        raise UserNotFound()

    session.delete(db_user)
    session.commit()

    return {'message': 'User successfuly deleted'}


def update_user(
    session: Session, user_id: str, user_schema: UserSchema
) -> UserPublic:
    converted_uuid = validate_uuid(user_id)

    db_user = session.scalar(select(User).where(User.id == converted_uuid))

    if db_user is None:
        raise UserNotFound

    db_user.email = user_schema.email
    db_user.username = user_schema.username
    db_user.password = get_password_hash(user_schema.password)
    db_user.role = user_schema.role

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
