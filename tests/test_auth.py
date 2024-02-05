from freezegun import freeze_time


def test_get_token(client, user):
    """
    Testa a obtenção de um token de acesso para um usuário existente.
    Verifica se o token e o tipo de token são retornados corretamente.
    """
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token


def test_token_expired_after_time(client, user):
    """
    Testa se o token de acesso expira após um determinado período de tempo.
    O token não deve mais ser válido para autenticação após o tempo de expiração.
    """
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == 200
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )
        assert response.status_code == 401
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_inexistent_user(client):
    """
    Testa a tentativa de obtenção de um token usando credenciais de um usuário inexistente.
    Deve retornar um erro indicando que o email ou senha estão incorretos.
    """
    response = client.post(
        '/auth/token',
        data={'username': 'no_user@no_domain.com', 'password': 'testtest'},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_wrong_password(client, user):
    """
    Testa a tentativa de obtenção de um token usando uma senha incorreta para um usuário existente.
    Deve retornar um erro indicando que o email ou senha estão incorretos.
    """
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, user, token):
    """
    Testa a funcionalidade de atualização do token de acesso.
    Verifica se um novo token de acesso é fornecido corretamente.
    """
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == 200
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, user):
    """
    Testa a tentativa de atualização de um token de acesso expirado.
    O token expirado não deve ser capaz de ser atualizado, e um erro deve ser retornado.
    """
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == 200
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == 401
        assert response.json() == {'detail': 'Could not validate credentials'}
