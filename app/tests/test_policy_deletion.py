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
from ..models.tag import Tag, policy_tags
from ..models.user import User, policy_users
from ..models.rule import Rule
from ..models.function import Function
from ..repositories import group_repo, policy_repo, user_repo, rule_repo
from ..schema.policy import PolicyCreate

def test_policy_group_cascade_delete(db: Session):
    """Test that policy_group entries are deleted when a policy is deleted."""
    # Create a test organization (assuming it exists or create it)
    org_id = 1  # Use an existing organization ID for testing

    # Create a test group
    test_group = group_repo.create_group(
        db=db,
        organization_id=org_id,
        name="test_group_for_policy_deletion",
        description="Test group for policy deletion"
    )

    # Create a test policy
    test_policy = policy_repo.create_policy(
        db=db,
        policy_in=PolicyCreate(
            name="test_policy_for_group_cascade",
            description="Test policy for group cascade deletion",
            organization_id=org_id
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

    # Delete the policy
    policy_repo.delete_policy(db, test_policy)

    # Verify that the association has been deleted
    stmt = select(policy_groups).where(
        policy_groups.c.policy_id == test_policy.id,
        policy_groups.c.group_id == test_group.id
    )
    result = db.execute(stmt).first()
    assert result is None, "Policy-group association not deleted"

    # Clean up - delete the test group
    group_repo.delete_group(db, test_group)

    print("Test passed: Policy-group association is deleted when policy is deleted")

def test_policy_tags_cascade_delete(db: Session):
    """Test that policy_tags entries are deleted when a policy is deleted."""
    # Create a test organization (assuming it exists or create it)
    org_id = 1  # Use an existing organization ID for testing

    # Create a test tag
    test_tag = Tag(value="test_tag_for_policy_deletion")
    db.add(test_tag)
    db.commit()
    db.refresh(test_tag)

    # Create a test policy
    test_policy = policy_repo.create_policy(
        db=db,
        policy_in=PolicyCreate(
            name="test_policy_for_tag_cascade",
            description="Test policy for tag cascade deletion",
            organization_id=org_id
        )
    )

    # Associate the tag with the policy
    policy_repo.add_tag(db, test_policy, test_tag)

    # Verify that the association exists
    stmt = select(policy_tags).where(
        policy_tags.c.policy_id == test_policy.id,
        policy_tags.c.tag_id == test_tag.id
    )
    result = db.execute(stmt).first()
    assert result is not None, "Policy-tag association not created"

    # Delete the policy
    policy_repo.delete_policy(db, test_policy)

    # Verify that the association has been deleted
    stmt = select(policy_tags).where(
        policy_tags.c.policy_id == test_policy.id,
        policy_tags.c.tag_id == test_tag.id
    )
    result = db.execute(stmt).first()
    assert result is None, "Policy-tag association not deleted"

    # Clean up - delete the test tag
    db.delete(test_tag)
    db.commit()

    print("Test passed: Policy-tag association is deleted when policy is deleted")

def test_policy_users_cascade_delete(db: Session):
    """Test that policy_users entries are deleted when a policy is deleted."""
    # Create a test user
    test_user = user_repo.create_user(
        db=db,
        email="test_user_for_policy_deletion@example.com",
        username="test_user_for_policy_deletion",
        first_name="Test",
        last_name="User",
        password="password123",
        is_superadmin=False
    )

    # Create a test policy
    test_policy = policy_repo.create_policy(
        db=db,
        policy_in=PolicyCreate(
            name="test_policy_for_user_cascade",
            description="Test policy for user cascade deletion",
            organization_id=1  # Use an existing organization ID for testing
        )
    )

    # Associate the user with the policy
    policy_repo.add_user(db, test_policy, test_user)

    # Verify that the association exists
    stmt = select(policy_users).where(
        policy_users.c.policy_id == test_policy.id,
        policy_users.c.user_id == test_user.id
    )
    result = db.execute(stmt).first()
    assert result is not None, "Policy-user association not created"

    # Delete the policy
    policy_repo.delete_policy(db, test_policy)

    # Verify that the association has been deleted
    stmt = select(policy_users).where(
        policy_users.c.policy_id == test_policy.id,
        policy_users.c.user_id == test_user.id
    )
    result = db.execute(stmt).first()
    assert result is None, "Policy-user association not deleted"

    # Clean up - delete the test user
    user_repo.delete_user(db, test_user)

    print("Test passed: Policy-user association is deleted when policy is deleted")

def test_policy_rules_cascade_delete(db: Session):
    """Test that rules entries are deleted when a policy is deleted."""
    # Create a test organization (assuming it exists or create it)
    org_id = 1  # Use an existing organization ID for testing

    # Get a function for testing (assuming it exists)
    test_function = db.query(Function).filter(Function.name == "admin").first()
    if not test_function:
        # If the admin function doesn't exist, create a test function
        test_function = Function(name="test_function_for_rule_deletion", description="Test function for rule deletion")
        db.add(test_function)
        db.commit()
        db.refresh(test_function)

    # Create a test policy
    test_policy = policy_repo.create_policy(
        db=db,
        policy_in=PolicyCreate(
            name="test_policy_for_rule_cascade",
            description="Test policy for rule cascade deletion",
            organization_id=org_id
        )
    )

    # Create a test rule associated with the policy
    test_rule = rule_repo.create_rule(
        db=db,
        policy_id=test_policy.id,
        function_id=test_function.id
    )

    # Verify that the rule exists
    rule = db.query(Rule).filter(Rule.id == test_rule.id).first()
    assert rule is not None, "Rule not created"

    # Delete the policy
    policy_repo.delete_policy(db, test_policy)

    # Verify that the rule has been deleted
    rule = db.query(Rule).filter(Rule.id == test_rule.id).first()
    assert rule is None, "Rule not deleted when policy was deleted"

    # Clean up - if we created a test function, delete it
    if test_function.name == "test_function_for_rule_deletion":
        db.delete(test_function)
        db.commit()

    print("Test passed: Rules are deleted when policy is deleted")
