from meu_projeto_chat.core.exceptions import EmailAlreadyExistsException
from meu_projeto_chat.repositories.user_repository import UserRepository
from meu_projeto_chat.core.security import get_password_hash


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, user_data: dict):
        existing_user = self.user_repository.get_user_by_email(user_data["email"])
        if existing_user:
            raise EmailAlreadyExistsException(user_data["email"])

        return self.user_repository.create_user(user_data)

    def get_user_by_email(self, email: str):
        return self.user_repository.get_user_by_email(email)

    def get_user_details(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)

    def update_user(self, user_id: int, update_data: dict):
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            update_data["password"] = hashed_password
        return self.user_repository.update_user(user_id, update_data)

    def delete_user(self, user_id: int):
        self.user_repository.delete_user(user_id)

    def get_all_users(self):
        return self.user_repository.get_all_users()
