import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from meu_projeto_chat.core.security import get_password_hash
from meu_projeto_chat.database import Base
from meu_projeto_chat.models.user import User
from meu_projeto_chat.repositories.user_repository import UserRepository


def test_create_user(session):
    user_data = {
        'email': 'test@test.com',
        'username': 'testuser',
        'password': 'password123',
    }
    user_repository = UserRepository(db_session=session)
    new_user = user_repository.create_user(user_data)

    assert new_user.email == user_data['email']
    assert (
        session.query(User).filter_by(email=user_data['email']).first()
        is not None
    )


def test_update_user(session):
    user_data = {
        'email': 'testupdate@test.com',
        'username': 'testupdateuser',
        'password': 'password123',
    }
    user_repository = UserRepository(db_session=session)
    user = user_repository.create_user(user_data)
    update_data = {
        'username': 'updateduser',
        'email': 'updated@test.com',
    }
    updated_user = user_repository.update_user(user.id, update_data)
    retrieved_user = session.query(User).filter_by(id=user.id).first()

    assert retrieved_user is not None
    assert updated_user.id == retrieved_user.id
    assert retrieved_user.username == update_data['username']
    assert retrieved_user.email == update_data['email']
    assert retrieved_user.password == user.password


def test_delete_user(session):
    user_data = {
        'email': 'testdelete@test.com',
        'username': 'testdeleteuser',
        'password': 'password123',
    }
    user_repository = UserRepository(db_session=session)
    user = user_repository.create_user(user_data)
    created_user = (
        session.query(User).filter_by(email=user_data['email']).first()
    )
    assert created_user is not None
    user_repository.delete_user(created_user.id)
    deleted_user = (
        session.query(User).filter_by(email=user_data['email']).first()
    )
    assert deleted_user is None


def test_update_user_password(session):
    user_data = {
        'email': 'testpasswordupdate@test.com',
        'username': 'testpasswordupdateuser',
        'password': get_password_hash('oldpassword'),
    }
    user_repository = UserRepository(db_session=session)
    user = user_repository.create_user(user_data)
    new_password = 'newpassword123'
    hashed_new_password = get_password_hash(new_password)
    user_repository.update_user(user.id, {'password': hashed_new_password})
    updated_user = session.query(User).filter_by(id=user.id).first()
    assert updated_user is not None
    assert updated_user.password == hashed_new_password
