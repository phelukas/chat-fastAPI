# tests/test_user_routes.py

from fastapi.testclient import TestClient


def test_list_all_users(client, user, other_user):
    """
    Testa a rota de listagem de todos os usuários.
    Deve retornar uma lista com todos os usuários registrados.
    """
    response = client.get("/users/all")
    assert response.status_code == 200
    assert (
        len(response.json()) >= 2
    )  # Verifica se pelo menos os dois usuários de teste estão na resposta


def test_create_user(client):
    """
    Testa a rota de criação de um novo usuário.
    Deve retornar o usuário criado com o status HTTP 200.
    """
    new_user_data = {
        "username": "new_user",
        "email": "new_user@test.com",
        "password": "new_password",
    }
    response = client.post("/users/", json=new_user_data)
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == new_user_data["email"]
    # Adicione mais asserções conforme necessário para validar a resposta


def test_get_user(client, user):
    """
    Testa a rota de obtenção dos detalhes de um usuário específico.
    Deve retornar os detalhes do usuário solicitado.
    """
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["id"] == user.id
    assert user_data["email"] == user.email
    # Verifica outros campos conforme necessário


def test_update_user(client, user, token):
    """
    Testa a rota de atualização de um usuário.
    Deve atualizar e retornar o usuário com os novos dados.
    """
    updated_data = {
        "username": "updated_user",
        "email": user.email,
    }
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json=updated_data,
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == "updated_user"
    # Verifique outros campos conforme necessário


def test_delete_user(client, user, token):
    """
    Testa a rota de exclusão de um usuário.
    Deve excluir o usuário e retornar uma mensagem de sucesso.
    """
    response = client.delete(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Usuário deletado com sucesso"}
