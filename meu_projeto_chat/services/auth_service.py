from fastapi import HTTPException

from meu_projeto_chat.core.security import create_access_token, verify_password
from meu_projeto_chat.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate_user(self, email: str, password: str) -> str:
        print(f'e-mail: ', str(email))
        print(f'password: ', str(password))
        user = self.user_repository.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=400, detail='Incorrect email or password'
            )
        access_token = create_access_token(data={'sub': user.email})
        return access_token

    def refresh_user_token(self, user_email: str) -> str:
        new_access_token = create_access_token(data={'sub': user_email})
        return new_access_token
