import pytest

from meu_projeto_chat.api.dependencies import (
    get_auth_service,
    get_user_service,
)


def test_get_user_service(session):
    """
    Testa se a função `get_user_service` retorna uma instância correta de UserService.
    """
    user_service = get_user_service(session)
    assert user_service.user_repository.db_session == session


def test_get_auth_service(session):
    """
    Testa se a função `get_auth_service` retorna uma instância correta de AuthService.
    """
    auth_service = get_auth_service(session)
    assert auth_service.user_repository.db_session == session
