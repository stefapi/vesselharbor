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
from ..models.user import User
from ..models.policy import Policy
from ..models.tag import Tag, group_tags, user_tags, policy_tags
from ..repositories import group_repo, user_repo, policy_repo, tag_repo
from ..schema.policy import PolicyCreate

def test_tag_auto_deletion_from_group(db: Session):
    """
    Test that a tag is automatically deleted when it's removed from a group
    and is no longer referenced by any other entity.
    """
    # Create a test organization (assuming it exists or create it)
    org_id = 1  # Use an existing organization ID for testing

    # Create a test group
    test_group = group_repo.create_group(
        db=db,
        organization_id=org_id,
        name="test_group_for_tag_auto_deletion",
        description="Test group for tag auto deletion"
    )

    # Create a test tag
    test_tag = tag_repo.create_tag(db, "test_tag_for_auto_deletion_from_group")

    # Associate the tag with the group
    group_repo.add_tag_to_group(db, test_group, test_tag)

    # Verify that the tag exists
    tag_id = test_tag.id
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is not None, "Tag not created"

    # Remove the tag from the group
    group_repo.remove_tag_from_group(db, test_group, test_tag)

    # Verify that the tag has been automatically deleted
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is None, "Tag not automatically deleted after being removed from group"

    # Clean up - delete the test group
    group_repo.delete_group(db, test_group)

def test_tag_auto_deletion_from_policy(db: Session):
    """
    Test that a tag is automatically deleted when it's removed from a policy
    and is no longer referenced by any other entity.
    """
    # Create a test organization (assuming it exists or create it)
    org_id = 1  # Use an existing organization ID for testing

    # Create a test policy
    policy_data = PolicyCreate(
        name="test_policy_for_tag_auto_deletion",
        description="Test policy for tag auto deletion",
        organization_id=org_id
    )
    test_policy = policy_repo.create_policy(db, policy_data)

    # Create a test tag
    test_tag = tag_repo.create_tag(db, "test_tag_for_auto_deletion_from_policy")

    # Associate the tag with the policy
    policy_repo.add_tag(db, test_policy, test_tag)

    # Verify that the tag exists
    tag_id = test_tag.id
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is not None, "Tag not created"

    # Remove the tag from the policy
    policy_repo.remove_tag(db, test_policy, test_tag)

    # Verify that the tag has been automatically deleted
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is None, "Tag not automatically deleted after being removed from policy"

    # Clean up - delete the test policy
    policy_repo.delete_policy(db, test_policy)

def test_tag_auto_deletion_from_user(db: Session):
    """
    Test that a tag is automatically deleted when it's removed from a user
    and is no longer referenced by any other entity.
    """
    # Get a test user (assuming it exists)
    test_user = db.query(User).first()
    assert test_user is not None, "No user found for testing"

    # Create a test tag
    test_tag = tag_repo.create_tag(db, "test_tag_for_auto_deletion_from_user")

    # Associate the tag with the user
    user_repo.add_tag_to_user(db, test_user, test_tag)

    # Verify that the tag exists
    tag_id = test_tag.id
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is not None, "Tag not created"

    # Remove the tag from the user
    user_repo.remove_tag_from_user(db, test_user, test_tag)

    # Verify that the tag has been automatically deleted
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is None, "Tag not automatically deleted after being removed from user"

def test_tag_not_deleted_when_still_referenced(db: Session):
    """
    Test that a tag is not deleted when it's removed from one entity
    but is still referenced by another entity.
    """
    # Create a test organization (assuming it exists or create it)
    org_id = 1  # Use an existing organization ID for testing

    # Create test group and policy
    test_group = group_repo.create_group(
        db=db,
        organization_id=org_id,
        name="test_group_for_tag_reference",
        description="Test group for tag reference"
    )

    policy_data = PolicyCreate(
        name="test_policy_for_tag_reference",
        description="Test policy for tag reference",
        organization_id=org_id
    )
    test_policy = policy_repo.create_policy(db, policy_data)

    # Create a test tag
    test_tag = tag_repo.create_tag(db, "test_tag_for_reference_check")

    # Associate the tag with both group and policy
    group_repo.add_tag_to_group(db, test_group, test_tag)
    policy_repo.add_tag(db, test_policy, test_tag)

    # Verify that the tag exists
    tag_id = test_tag.id
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is not None, "Tag not created"

    # Remove the tag from the group
    group_repo.remove_tag_from_group(db, test_group, test_tag)

    # Verify that the tag still exists (because it's still referenced by the policy)
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is not None, "Tag was deleted even though it's still referenced by policy"

    # Clean up - remove the tag from the policy and delete both entities
    policy_repo.remove_tag(db, test_policy, test_tag)
    group_repo.delete_group(db, test_group)
    policy_repo.delete_policy(db, test_policy)

    # Verify that the tag has been automatically deleted after being removed from all entities
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is None, "Tag not automatically deleted after being removed from all entities"
