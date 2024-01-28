import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from meu_projeto_chat.app import app

from meu_projeto_chat.database import get_session
from meu_projeto_chat.core.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(__app__) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    __app__.dependency_overrides.clear()
