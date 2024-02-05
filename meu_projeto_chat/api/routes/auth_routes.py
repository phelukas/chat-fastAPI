from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from meu_projeto_chat.api.dependencies import get_auth_service
from meu_projeto_chat.core.security import get_current_user
from meu_projeto_chat.models.user import User
from meu_projeto_chat.schemas.user_schema import Token
from meu_projeto_chat.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    access_token = auth_service.authenticate_user(
        form_data.username, form_data.password
    )
    print({'access_token': access_token, 'token_type': 'bearer'})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(
    user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    new_access_token = auth_service.refresh_user_token(user.email)
    return {'access_token': new_access_token, 'token_type': 'bearer'}
