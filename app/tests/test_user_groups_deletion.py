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

from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.group import Group, user_groups
from ..repositories import user_repo, group_repo

def test_user_groups_cascade_delete(db: Session):
    # Create a test user
    test_user = user_repo.create_user(
        db=db,
        email="test_user_for_group_deletion@example.com",
        username="test_user_for_group_deletion",
        first_name="Test",
        last_name="User",
        password="password123",
        is_superadmin=False
    )

    # Create a test group
    test_group = group_repo.create_group(
        db=db,
        organization_id=1,  # Use an existing organization ID for testing
        name="test_group_for_user_deletion",
        description="Test group for user deletion"
    )

    # Associate the group with the user
    test_user.groups.append(test_group)
    db.commit()

    # Verify that the association exists
    stmt = select(user_groups).where(
        user_groups.c.user_id == test_user.id,
        user_groups.c.group_id == test_group.id
    )
    result = db.execute(stmt).first()
    assert result is not None, "User-group association not created"

    # Delete the user
    user_repo.delete_user(db, test_user)

    # Verify that the association has been deleted
    stmt = select(user_groups).where(
        user_groups.c.user_id == test_user.id,
        user_groups.c.group_id == test_group.id
    )
    result = db.execute(stmt).first()
    assert result is None, "User-group association not deleted"

    # Clean up - delete the test group
    group_repo.delete_group(db, test_group)

    print("Test passed: User-group association is deleted when user is deleted")
