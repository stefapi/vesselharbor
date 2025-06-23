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
from ..models.group import Group
from ..models.policy import Policy, policy_groups
from ..repositories import group_repo, policy_repo
from ..schema.policy import PolicyCreate

def test_policy_group_cascade_delete(db: Session):
    # Create a test organization (assuming it exists or create it)
    org_id = 1  # Use an existing organization ID for testing

    # Create a test group
    test_group = group_repo.create_group(
        db=db,
        organization_id=org_id,
        name="test_group_for_deletion",
        description="Test group for deletion"
    )

    # Create a test policy
    test_policy = policy_repo.create_policy(
        db=db,
        policy_in=PolicyCreate(
            name="test_policy_for_deletion",
            description="Test policy for deletion",
            organization_id=org_id,
            access_schedule=None
        )
    )

    # Associate the group with the policy
    policy_repo.add_group(db, test_policy, test_group)

    # Verify that the association exists
    stmt = select(policy_groups).where(
        policy_groups.c.policy_id == test_policy.id,
        policy_groups.c.group_id == test_group.id
    )
    result = db.execute(stmt).first()
    assert result is not None, "Policy-group association not created"

    # Delete the group
    group_repo.delete_group(db, test_group)

    # Verify that the association has been deleted
    stmt = select(policy_groups).where(
        policy_groups.c.policy_id == test_policy.id,
        policy_groups.c.group_id == test_group.id
    )
    result = db.execute(stmt).first()
    assert result is None, "Policy-group association not deleted"

    # Clean up - delete the test policy
    db.delete(test_policy)
    db.commit()

    print("Test passed: Policy-group association is deleted when group is deleted")
