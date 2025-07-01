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

import pytest
from sqlalchemy.orm import Session
from ..models.element import Element
from ..models.environment import Environment
from ..models.tag import Tag
from ..repositories import element_repo, environment_repo, tag_repo

def test_tag_auto_deletion_from_element(db: Session):
    """
    Test that a tag is automatically deleted when it's removed from an element
    and is no longer referenced by any other entity.
    """
    # Create a test environment
    test_env = environment_repo.create_environment(db, "test_env_for_element_tag")

    # Create a test element
    test_element = element_repo.create_element(
        db=db,
        environment_id=test_env.id,
        name="test_element_for_tag_auto_deletion",
        description="Test element for tag auto deletion"
    )

    # Create a test tag
    test_tag = tag_repo.create_tag(db, "test_tag_for_auto_deletion_from_element")

    # Associate the tag with the element
    test_element.tags.append(test_tag)
    db.commit()

    # Verify that the tag exists
    tag_id = test_tag.id
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is not None, "Tag not created"

    # Remove the tag from the element
    test_element.tags.remove(test_tag)
    db.commit()

    # Verify that the tag has been automatically deleted
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is None, "Tag not automatically deleted after being removed from element"

    # Clean up - delete the test element and environment
    element_repo.delete_element(db, test_element)
    environment_repo.delete_environment(db, test_env)

def test_tag_auto_deletion_from_environment(db: Session):
    """
    Test that a tag is automatically deleted when it's removed from an environment
    and is no longer referenced by any other entity.
    """
    # Create a test environment
    test_env = environment_repo.create_environment(db, "test_env_for_tag_auto_deletion")

    # Create a test tag
    test_tag = tag_repo.create_tag(db, "test_tag_for_auto_deletion_from_environment")

    # Associate the tag with the environment
    test_env.tags.append(test_tag)
    db.commit()

    # Verify that the tag exists
    tag_id = test_tag.id
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is not None, "Tag not created"

    # Remove the tag from the environment
    test_env.tags.remove(test_tag)
    db.commit()

    # Verify that the tag has been automatically deleted
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is None, "Tag not automatically deleted after being removed from environment"

    # Clean up - delete the test environment
    environment_repo.delete_environment(db, test_env)

def test_tag_not_deleted_when_still_referenced_by_element_and_environment(db: Session):
    """
    Test that a tag is not deleted when it's removed from one entity
    but is still referenced by another entity.
    """
    # Create test environment and element
    test_env = environment_repo.create_environment(db, "test_env_for_tag_reference")

    test_element = element_repo.create_element(
        db=db,
        environment_id=test_env.id,
        name="test_element_for_tag_reference",
        description="Test element for tag reference"
    )

    # Create a test tag
    test_tag = tag_repo.create_tag(db, "test_tag_for_element_env_reference_check")

    # Associate the tag with both element and environment
    test_element.tags.append(test_tag)
    test_env.tags.append(test_tag)
    db.commit()

    # Verify that the tag exists
    tag_id = test_tag.id
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is not None, "Tag not created"

    # Remove the tag from the element
    test_element.tags.remove(test_tag)
    db.commit()

    # Verify that the tag still exists (because it's still referenced by the environment)
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is not None, "Tag was deleted even though it's still referenced by environment"

    # Clean up - remove the tag from the environment and delete both entities
    test_env.tags.remove(test_tag)
    db.commit()

    element_repo.delete_element(db, test_element)
    environment_repo.delete_environment(db, test_env)

    # Verify that the tag has been automatically deleted after being removed from all entities
    tag = tag_repo.get_tag(db, tag_id)
    assert tag is None, "Tag not automatically deleted after being removed from all entities"
