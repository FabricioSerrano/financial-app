from http import HTTPStatus
from typing import Annotated, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from financial_app.common.database import get_session
from financial_app.users import repositories

from .schemas import UserList, UserPublic, UserSchema

router = APIRouter(prefix='/users', tags=['Users'])

T_Session = Annotated[Session, Depends(get_session)]


@router.get('/', status_code=HTTPStatus.OK)
def get_users(
    session: T_Session,
    user_id: str = None,
    username: str = None,
    limit: int = 10,
    offset: int = 0,
) -> Union[UserList, UserPublic]:
    """Get all users or especific user by username or user id"""

    if user_id is not None:
        return repositories.get_user_by_id(session, user_id)

    if username is not None:
        return repositories.get_user_by_username(session, username)

    return repositories.get_all_users(session, limit, offset)


@router.post('/', status_code=HTTPStatus.CREATED)
def create_user(session: T_Session, user_schema: UserSchema) -> UserPublic:
    return repositories.create_user(session, user_schema)
