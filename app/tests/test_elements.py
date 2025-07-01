# tests/test_elements.py

import pytest
from .conftest import test_data

def test_create_element(test_client, test_data):
    headers = {"Authorization": f"Bearer {test_data.admin_token}"}
    response = test_client.post(
        f"/elements/{test_data.env_id}",
        json={"name": "Element1", "description": "Test element"},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    element = response.json()
    assert element["name"] == "Element1"
    test_data.element_id = element["id"]

def test_list_elements(test_client, test_data):
    headers = {"Authorization": f"Bearer {test_data.admin_token}"}
    response = test_client.get(
        f"/environments/{test_data.env_id}/elements?skip=0&limit=10&name=Element",
        headers=headers,
    )
    assert response.status_code == 200, response.text
    elements = response.json()
    assert isinstance(elements, list)
    assert any(elem["name"] == "Element1" for elem in elements)

def test_update_element_environment(test_client, test_data):
    headers = {"Authorization": f"Bearer {test_data.admin_token}"}

    # Create a second environment
    response = test_client.post(
        "/environments",
        json={"name": "Env2"},
        headers=headers
    )
    assert response.status_code == 200, response.text
    env2 = response.json()
    assert env2["name"] == "Env2"
    env2_id = env2["id"]

    # Update the element to use the new environment
    response = test_client.put(
        f"/elements/{test_data.element_id}",
        json={"name": "Element1-Updated", "environment_id": env2_id},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    updated_element = response.json()
    assert updated_element["name"] == "Element1-Updated"
    assert updated_element["environment_id"] == env2_id

    # Verify the element is now in the new environment
    response = test_client.get(
        f"/environments/{env2_id}/elements?skip=0&limit=10",
        headers=headers,
    )
    assert response.status_code == 200, response.text
    elements = response.json()
    assert isinstance(elements, list)
    assert any(elem["name"] == "Element1-Updated" for elem in elements)
