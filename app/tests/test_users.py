# tests/test_users.py

import pytest
from .conftest import test_data

# --- Tests de création et de connexion ---

def test_create_superadmin_user(test_client, test_data):
    response = test_client.post(
        "/users", json={"email": "admin@example.com", "password": "admin123"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "admin@example.com"
    assert data["is_superadmin"] is True

def test_create_user_existing_email(test_client, test_data):
    # Tentative de créer un utilisateur avec un email déjà utilisé (admin@example.com)
    response = test_client.post(
        "/users", json={"email": "admin@example.com", "password": "anotherpass"}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    # Le message d'erreur doit indiquer que l'email est déjà enregistré
    assert "déjà enregistré" in data.get("detail", "").lower()

def test_login_superadmin(test_client, test_data):
    response = test_client.post(
        "/login", data={"username": "admin@example.com", "password": "admin123"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    test_data.admin_token = data["access_token"]

def test_login_wrong_password(test_client, test_data):
    # Tentative de connexion avec un mauvais mot de passe
    response = test_client.post(
        "/login", data={"username": "admin@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert "incorrect" in data.get("detail", "").lower()

def test_login_non_existing_email(test_client, test_data):
    # Tentative de connexion avec un email non enregistré
    response = test_client.post(
        "/login", data={"username": "nonexist@example.com", "password": "nopass"}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert "incorrect" in data.get("detail", "").lower()

# --- Tests de changement de mot de passe ---
def test_change_password_wrong_old_password(test_client, test_data):
    headers = {"Authorization": f"Bearer {test_data.admin_token}"}
    # Tentative de changement de mot de passe avec un ancien mot de passe incorrect
    response = test_client.put(
        "/users/1/password",
        json={"old_password": "wrongoldpass", "new_password": "newpass123"},
        headers=headers,
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert "invalid" in data.get("detail", "").lower()

# --- Tests de suppression d'utilisateur ---
def test_delete_self(test_client, test_data):
    headers = {"Authorization": f"Bearer {test_data.admin_token}"}
    # L'utilisateur tente de se supprimer lui-même
    response = test_client.delete("/users/1", headers=headers)
    assert response.status_code == 400, response.text
    data = response.json()
    assert "vous ne pouvez pas vous supprimer" in data.get("detail", "").lower()

def test_delete_non_existing_user(test_client, test_data):
    headers = {"Authorization": f"Bearer {test_data.admin_token}"}
    # Tentative de suppression d'un utilisateur inexistant (par exemple, id 999)
    response = test_client.delete("/users/999", headers=headers)
    assert response.status_code == 404, response.text
    data = response.json()
    assert "non trouvé" in data.get("detail", "").lower()

# --- Tests d'accès non autorisé et de gestion de superadmin ---
def test_change_superadmin_by_non_superadmin(test_client, test_data):
    # Création d'un utilisateur non-superadmin
    response = test_client.post(
        "/users", json={"email": "user@example.com", "password": "userpass"}
    )
    assert response.status_code == 200, response.text
    user_data = response.json()
    # Connexion de cet utilisateur
    response = test_client.post(
        "/login", data={"username": "user@example.com", "password": "userpass"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    user_token = data["access_token"]

    # Tentative de cet utilisateur de modifier le statut superadmin d'un autre utilisateur (ici admin)
    headers = {"Authorization": f"Bearer {user_token}"}
    response = test_client.put(
        "/users/1/superadmin", json={"is_superadmin": False}, headers=headers
    )
    assert response.status_code == 403, response.text
    data = response.json()
    assert "non autorisé" in data.get("detail", "").lower()

def test_list_users_non_superadmin(test_client, test_data):
    # L'utilisateur non-superadmin essaie de lister tous les utilisateurs
    # On utilise le token de "user@example.com"
    response = test_client.post(
        "/login", data={"username": "user@example.com", "password": "userpass"}
    )
    assert response.status_code == 200, response.text
    user_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {user_token}"}
    response = test_client.get("/users", headers=headers)
    assert response.status_code == 403, response.text
    data = response.json()
    assert "non autorisé" in data.get("detail", "").lower()

def test_invalid_token(test_client, test_data):
    # Utilisation d'un token invalide pour accéder à un endpoint protégé
    headers = {"Authorization": "Bearer invalidtoken"}
    response = test_client.get("/users/1/environments", headers=headers)
    assert response.status_code in [401, 403], response.text
    data = response.json()
    assert "token invalide" in data.get("detail", "").lower() or "identifiants invalides" in data.get("detail", "").lower()

# --- Test de réinitialisation de mot de passe pour un email inexistant ---
def test_reset_password_request_non_existing(test_client, test_data):
    response = test_client.post(
        "/users/reset_password_request", json={"email": "nonexist@example.com"}
    )
    # Pour des raisons de sécurité, on doit renvoyer la même réponse même si l'email n'existe pas
    assert response.status_code == 200, response.text
    data = response.json()
    assert "detail" in data

# --- Test de réinitialisation effective avec un token mal formé ---
def test_reset_password_with_invalid_token(test_client, test_data):
    response = test_client.post(
        "/users/reset_password", json={"token": "malformedtoken", "new_password": "whatever"}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert "token invalide" in data.get("detail", "").lower() or "token" in data.get("detail", "").lower()
