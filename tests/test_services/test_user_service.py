from unittest.mock import ANY, MagicMock, patch

import pytest

from meu_projeto_chat.core.exceptions import EmailAlreadyExistsException
from meu_projeto_chat.repositories.user_repository import UserRepository
from meu_projeto_chat.services.user_service import UserService


@pytest.fixture
def user_repository_mock():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def user_service(user_repository_mock):
    return UserService(user_repository=user_repository_mock)


def test_register_user_success(user_service, user_repository_mock):
    user_data = {
        'email': 'new@test.com',
        'username': 'newuser',
        'password': 'password123',
    }
    user_repository_mock.get_user_by_email.return_value = None

    user_service.register_user(user_data)

    user_repository_mock.create_user.assert_called_once()


def test_register_user_failure_email_exists(
    user_service, user_repository_mock
):
    user_data = {
        'email': 'existing@test.com',
        'username': 'newuser',
        'password': 'password123',
    }
    user_repository_mock.get_user_by_email.return_value = user_data

    with pytest.raises(EmailAlreadyExistsException):
        user_service.register_user(user_data)


def test_get_user_by_email(user_service, user_repository_mock):
    email = 'test@test.com'
    user_service.get_user_by_email(email)

    user_repository_mock.get_user_by_email.assert_called_once_with(email)


def test_get_user_details(user_service, user_repository_mock):
    user_id = 1
    user_service.get_user_details(user_id)

    user_repository_mock.get_user_by_id.assert_called_once_with(user_id)


def test_update_user(user_service, user_repository_mock):
    user_id = 1
    update_data = {'username': 'updateduser', 'email': 'updated@test.com'}
    user_repository_mock.get_user_by_id.return_value = MagicMock()

    user_service.update_user(user_id, update_data)

    user_repository_mock.update_user.assert_called_once_with(
        user_id, update_data
    )


def test_delete_user(user_service, user_repository_mock):
    user_id = 1
    user_service.delete_user(user_id)

    user_repository_mock.delete_user.assert_called_once_with(user_id)


def test_get_all_users(user_service, user_repository_mock):
    user_service.get_all_users()

    user_repository_mock.get_all_users.assert_called_once()


def test_update_user_password(user_service, user_repository_mock):
    user_id = 1
    new_password = 'newSecurePassword123'

    with patch(
        'meu_projeto_chat.core.security.get_password_hash'
    ) as mock_get_password_hash:
        mock_get_password_hash.return_value = 'hashedNewPassword'
        user_service.update_user(user_id, {'password': new_password})
    user_repository_mock.update_user.assert_called_once_with(
        user_id, {'password': ANY}
    )
