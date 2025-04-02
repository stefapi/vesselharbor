# tests/test_groups.py

import pytest
from .conftest import test_data

def test_create_group(test_client, test_data):
    headers = {"Authorization": f"Bearer {test_data.admin_token}"}
    response = test_client.post(
        f"/groups/{test_data.env_id}",
        json={"name": "Group1", "description": "A test group"},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    group = response.json()
    assert group["name"] == "Group1"
    test_data.group_id = group["id"]

def test_list_groups_in_environment(test_client, test_data):
    headers = {"Authorization": f"Bearer {test_data.admin_token}"}
    response = test_client.get(
        f"/groups/environment/{test_data.env_id}?skip=0&limit=10&name=Group",
        headers=headers,
    )
    assert response.status_code == 200, response.text
    groups = response.json()
    assert isinstance(groups, list)
    assert any(group["name"] == "Group1" for group in groups)
