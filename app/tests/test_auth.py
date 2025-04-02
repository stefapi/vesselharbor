# tests/test_auth.py

import pytest
from .conftest import test_data
from ..core.auth import create_access_token

def test_reset_password_request(test_client, test_data):
    response = test_client.post(
        "/users/reset_password_request", json={"email": "admin@example.com"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "detail" in data

def test_reset_password(test_client, test_data):
    # Simuler un token de réinitialisation
    reset_token = create_access_token(data={"sub": "1", "token_type": "password_reset"})
    response = test_client.post(
        "/users/reset_password",
        json={"token": reset_token, "new_password": "newadmin123"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    # Vérifier que la réinitialisation a réussi
    assert "success" in data["status"].lower() or "réinitialisé" in data.get("message", data.get("detail", ""))
    # Se reconnecter avec le nouveau mot de passe
    response = test_client.post(
        "/login", data={"username": "admin@example.com", "password": "newadmin123"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    test_data.admin_token = data["access_token"]
