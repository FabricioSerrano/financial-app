from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from financial_app.common.database import get_session
from financial_app.users import repositories

from .schemas import UserList, UserPublic, UserSchema

router = APIRouter(prefix='/users', tags=['Users'])

T_Session = Annotated[Session, Depends(get_session)]


@router.get('/', status_code=HTTPStatus.OK)
def get_all_users(
    session: T_Session, limit: int = 10, offset: int = 0
) -> UserList:
    return repositories.get_all_users(session, limit, offset)


@router.post('/', status_code=HTTPStatus.CREATED)
def create_user(session: T_Session, user_schema: UserSchema) -> UserPublic:
    return repositories.create_user(session, user_schema)
