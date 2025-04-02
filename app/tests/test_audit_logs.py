# tests/test_audit_logs.py

import pytest
from .conftest import test_data

def test_list_audit_logs(test_client, test_data):
    headers = {"Authorization": f"Bearer {test_data.admin_token}"}
    response = test_client.get(
        "/audit-logs/?skip=0&limit=10", headers=headers,
    )
    assert response.status_code == 200, response.text
    logs = response.json()
    assert isinstance(logs, list)
    # On s'attend à retrouver au moins une entrée d'audit
    assert len(logs) > 0
