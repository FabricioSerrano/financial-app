from http import HTTPStatus

from fastapi.exceptions import HTTPException


class InvalidUserId(HTTPException):
    def __init__(self):
        super().__init__(HTTPStatus.BAD_REQUEST, 'User Id is not valid')


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(HTTPStatus.NOT_FOUND, 'User not found')


class EmailAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(HTTPStatus.BAD_REQUEST, 'Email already exists')


class UsernameAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(HTTPStatus.BAD_REQUEST, 'Username already exists')
