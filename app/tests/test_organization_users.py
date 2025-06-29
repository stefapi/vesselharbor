#  Copyright (c) 2025.  VesselHarbor
#
#  ____   ____                          .__    ___ ___             ___.
#  \   \ /   /____   ______ ______ ____ |  |  /   |   \_____ ______\_ |__   ___________
#   \   Y   // __ \ /  ___//  ___// __ \|  | /    ~    \__  \\_  __ \ __ \ /  _ \_  __ \
#    \     /\  ___/ \___ \ \___ \\  ___/|  |_\    Y    // __ \|  | \/ \_\ (  <_> )  | \/
#     \___/  \___  >____  >____  >\___  >____/\___|_  /(____  /__|  |___  /\____/|__|
#                \/     \/     \/     \/            \/      \/          \/
#
#
#  MIT License
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

from ..main import app
from ..models.user import User
from ..models.organization import Organization
from ..models.group import Group

client = TestClient(app)

def test_list_organization_users(db_session: Session, test_user_token: str, test_organization: Organization, test_user: User):
    """Test listing users of an organization."""
    # Add the test user to the test organization if not already
    if test_user not in test_organization.users:
        test_organization.users.append(test_user)
        db_session.commit()

    # Make the request with authentication
    response = client.get(
        f"/api/v1/organizations/{test_organization.id}/users",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0

    # Verify the user data is correct
    user_data = data["data"][0]
    assert "id" in user_data
    assert "username" in user_data
    assert "email" in user_data

def test_remove_non_admin_user(db_session: Session, test_user_token: str, test_organization: Organization):
    """Test removing a non-admin user from an organization."""
    # Create a non-admin user
    non_admin_user = User(
        username="nonadmin",
        email="nonadmin@example.com",
        hashed_password="hashed_password",
        is_active=True
    )
    db_session.add(non_admin_user)
    db_session.commit()

    # Add the non-admin user to the organization
    test_organization.users.append(non_admin_user)
    db_session.commit()

    # Make the request to remove the non-admin user
    response = client.delete(
        f"/api/v1/organizations/{test_organization.id}/users/{non_admin_user.id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert "data" in data

    # Verify the user was removed
    db_session.refresh(test_organization)
    assert non_admin_user not in test_organization.users

def test_remove_admin_user_with_other_admins(db_session: Session, test_user_token: str, test_organization: Organization, test_user: User):
    """Test removing an admin user when there are other admins."""
    # Get the admin group
    admin_group = db_session.query(Group).filter(
        Group.organization_id == test_organization.id,
        Group.name == "admin"
    ).first()

    # Create another admin user
    another_admin = User(
        username="anotheradmin",
        email="anotheradmin@example.com",
        hashed_password="hashed_password",
        is_active=True
    )
    db_session.add(another_admin)
    db_session.commit()

    # Add the user to the organization and admin group
    test_organization.users.append(another_admin)
    admin_group.users.append(another_admin)
    db_session.commit()

    # Make the request to remove the admin user
    response = client.delete(
        f"/api/v1/organizations/{test_organization.id}/users/{another_admin.id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert "data" in data

    # Verify the user was removed
    db_session.refresh(test_organization)
    assert another_admin not in test_organization.users

def test_remove_last_admin_user(db_session: Session, test_user_token: str, test_organization: Organization, test_user: User):
    """Test that removing the last admin user fails."""
    # Get the admin group
    admin_group = db_session.query(Group).filter(
        Group.organization_id == test_organization.id,
        Group.name == "admin"
    ).first()

    # Ensure test_user is the only admin
    for user in admin_group.users:
        if user.id != test_user.id:
            admin_group.users.remove(user)
    db_session.commit()

    # Make the request to remove the last admin user
    response = client.delete(
        f"/api/v1/organizations/{test_organization.id}/users/{test_user.id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    # Check the response - should fail with 409 Conflict
    assert response.status_code == 409
    data = response.json()
    assert "detail" in data
    assert "dernier administrateur" in data["detail"]

    # Verify the user was not removed
    db_session.refresh(test_organization)
    assert test_user in test_organization.users
