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


# @pytest.fixture
# def session():
#     engine = create_engine(
#         "sqlite:///:memory:",
#         connect_args={"check_same_thread": False},
#         poolclass=StaticPool,
#     )
#     Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#     Base.metadata.create_all(engine)

#     Session = sessionmaker(bind=engine)

#     yield Session()

#     Base.metadata.drop_all(engine)


# @pytest.fixture
# def user(session):
#     password = "testtest"
#     user = UserFactory(password=get_password_hash(password))

#     session.add(user)
#     session.commit()
#     session.refresh(user)

#     user.clean_password = "testtest"

#     return user


# @pytest.fixture
# def other_user(session):
#     password = "testtest"
#     user = UserFactory(password=get_password_hash(password))

#     session.add(user)
#     session.commit()
#     session.refresh(user)

#     user.clean_password = "testtest"

#     return user


# @pytest.fixture
# def token(client, user):
#     response = client.post(
#         "/auth/token",
#         data={"username": user.email, "password": user.clean_password},
#     )
#     return response.json()["access_token"]


# class UserFactory(factory.Factory):
#     class Meta:
#         model = User

#     id = factory.Sequence(lambda n: n)
#     username = factory.LazyAttribute(lambda obj: f"test{obj.id}")
#     email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
#     password = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
