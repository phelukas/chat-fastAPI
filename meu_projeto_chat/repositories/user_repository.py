from sqlalchemy.orm import Session
from meu_projeto_chat.models.user import User
from meu_projeto_chat.database import get_session
from meu_projeto_chat.core.security import get_current_user
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from meu_projeto_chat.core.security import get_password_hash


__session__ = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


class UserRepository:
    def __init__(self, db_session: __session__):
        self.db_session = db_session

    def get_all_users(self):
        return self.db_session.query(User).all()

    def create_user(self, user_data: dict) -> User:
        hashed_password = get_password_hash(user_data["password"])

        user_data["password"] = hashed_password

        new_user = User(**user_data)
        self.db_session.add(new_user)
        self.db_session.commit()
        return new_user

    def get_user_by_id(self, user_id: int) -> User:
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User:
        return self.db_session.scalar(select(User).where(User.email == email))

    def update_user(self, user_id: int, update_data: dict) -> User:
        user = self.get_user_by_id(user_id)
        if user:
            for key, value in update_data.items():
                setattr(user, key, value)
            self.db_session.commit()
            return user
        return None

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()
