from fastapi import Depends
from sqlalchemy.orm import Session

from meu_projeto_chat.database import get_session
from meu_projeto_chat.repositories.user_repository import UserRepository
from meu_projeto_chat.services.auth_service import AuthService
from meu_projeto_chat.services.user_service import UserService


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)


def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    user_repository = UserRepository(session)
    return AuthService(user_repository)
