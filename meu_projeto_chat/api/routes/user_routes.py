from typing import List

from fastapi import APIRouter, Depends, HTTPException

from meu_projeto_chat.api.dependencies import get_user_service
from meu_projeto_chat.core.security import get_current_user
from meu_projeto_chat.models.user import User
from meu_projeto_chat.schemas.user_schema import (
    UserPublic,
    UserSchema,
    UserUpdateSchema,
)
from meu_projeto_chat.services.user_service import UserService

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/all', response_model=List[UserPublic])
def list_all_users(user_service: UserService = Depends(get_user_service)):
    users = user_service.get_all_users()
    return users


@router.post('/', response_model=UserPublic)
def create_user(
    user: UserSchema, user_service: UserService = Depends(get_user_service)
):
    if user_service.get_user_by_email(user.model_dump()['email']):
        raise HTTPException(status_code=400, detail=str("E-mail já em uso"))
    created_user = user_service.register_user(user.model_dump())
    return created_user


@router.get('/', response_model=UserPublic)
def get_user(
    current_user: User = Depends(get_current_user)
):
    user = current_user
    if not user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return user


@router.put('/', response_model=UserPublic)
def update_user(
    user_update: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    if current_user.email != user_update.email:
        raise HTTPException(
            status_code=403, detail='Não autorizado a atualizar este usuário'
        )
    updated_user = user_service.update_user(
        current_user.id, user_update.dict(exclude_none=True)
    )
    return updated_user


@router.delete('/{user_id}', response_model=dict)
def delete_user(
     current_user: User = Depends(get_current_user), user_service: UserService = Depends(get_user_service)
):
    user_id = current_user.id
    user_service.delete_user(user_id)
    return {'detail': 'Usuário deletado com sucesso'}
