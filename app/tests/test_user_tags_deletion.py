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
from ..models.tag import Tag, user_tags
from ..repositories import user_repo

def test_user_tags_cascade_delete(db: Session):
    # Create a test user
    test_user = user_repo.create_user(
        db=db,
        email="test_user_for_tag_deletion@example.com",
        username="test_user_for_tag_deletion",
        first_name="Test",
        last_name="User",
        password="password123",
        is_superadmin=False
    )

    # Create a test tag
    test_tag = Tag(value="test_tag_for_user_deletion")
    db.add(test_tag)
    db.commit()
    db.refresh(test_tag)

    # Associate the tag with the user
    test_user.tags.append(test_tag)
    db.commit()

    # Verify that the association exists
    stmt = select(user_tags).where(
        user_tags.c.user_id == test_user.id,
        user_tags.c.tag_id == test_tag.id
    )
    result = db.execute(stmt).first()
    assert result is not None, "User-tag association not created"

    # Delete the user
    user_repo.delete_user(db, test_user)

    # Verify that the association has been deleted
    stmt = select(user_tags).where(
        user_tags.c.user_id == test_user.id,
        user_tags.c.tag_id == test_tag.id
    )
    result = db.execute(stmt).first()
    assert result is None, "User-tag association not deleted"

    # Clean up - delete the test tag
    db.delete(test_tag)
    db.commit()

    print("Test passed: User-tag association is deleted when user is deleted")
