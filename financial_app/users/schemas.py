from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from .enums import UserRole


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str
    role: UserRole


class UserPublic(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    role: UserRole
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: UUID


class UserList(BaseModel):
    users: list[UserPublic]
