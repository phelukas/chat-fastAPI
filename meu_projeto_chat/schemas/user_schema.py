# app/schemas/user_schema.py

from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str | None = None


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class Message(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserUpdateSchema(BaseModel):
    username: str | None = None
    password: str | None = None
