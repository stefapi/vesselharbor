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
        f"/elements/environment/{test_data.env_id}?skip=0&limit=10&name=Element",
        headers=headers,
    )
    assert response.status_code == 200, response.text
    elements = response.json()
    assert isinstance(elements, list)
    assert any(elem["name"] == "Element1" for elem in elements)
