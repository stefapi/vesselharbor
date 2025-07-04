# tests/conftest.py

import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Supprime la base de données de test avant et après les tests (si SQLite est utilisée)
@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    db_path = "test.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    yield
    if os.path.exists(db_path):
        os.remove(db_path)

# Client de test accessible à tous les tests
@pytest.fixture(scope="session")
def test_client() -> TestClient:
    return TestClient(app)

# Un objet pour stocker des données globales durant les tests
class TestData:
    admin_token: str = None
    env_id: int = None
    group_id: int = None
    element_id: int = None

@pytest.fixture(scope="session")
def test_data() -> TestData:
    return TestData()
