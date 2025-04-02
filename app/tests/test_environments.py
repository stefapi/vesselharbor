# tests/test_environments.py

import pytest
from .conftest import test_data

def test_create_environment(test_client, test_data):
    headers = {"Authorization": f"Bearer {test_data.admin_token}"}
    response = test_client.post("/environments", json={"name": "Env1"}, headers=headers)
    assert response.status_code == 200, response.text
    env = response.json()
    assert env["name"] == "Env1"
    test_data.env_id = env["id"]

def test_list_environments(test_client, test_data):
    headers = {"Authorization": f"Bearer {test_data.admin_token}"}
    response = test_client.get("/environments/?skip=0&limit=10&name=Env", headers=headers)
    assert response.status_code == 200, response.text
    envs = response.json()
    assert isinstance(envs, list)
    assert any("Env1" in env["name"] for env in envs)
