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
#
#

# app/repositories/volume_application_repo.py
from sqlalchemy.orm import Session
from ..models.volume_application import VolumeApplication
from typing import List, Optional

def create_volume_application(
    db: Session,
    volume_id: int,
    application_id: int
) -> VolumeApplication:
    attachment = VolumeApplication(
        volume_id=volume_id,
        application_id=application_id
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment

def get_volume_application(db: Session, attachment_id: int) -> Optional[VolumeApplication]:
    return db.query(VolumeApplication).filter(VolumeApplication.id == attachment_id).first()

def get_volume_application_by_ids(db: Session, volume_id: int, application_id: int) -> Optional[VolumeApplication]:
    return db.query(VolumeApplication).filter(
        VolumeApplication.volume_id == volume_id,
        VolumeApplication.application_id == application_id
    ).first()

def list_volume_applications(db: Session, skip: int = 0, limit: int = 100) -> List[VolumeApplication]:
    return db.query(VolumeApplication).offset(skip).limit(limit).all()

def list_volume_applications_by_volume(db: Session, volume_id: int) -> List[VolumeApplication]:
    return db.query(VolumeApplication).filter(VolumeApplication.volume_id == volume_id).all()

def list_volume_applications_by_application(db: Session, application_id: int) -> List[VolumeApplication]:
    return db.query(VolumeApplication).filter(VolumeApplication.application_id == application_id).all()

def delete_volume_application(db: Session, attachment: VolumeApplication) -> None:
    db.delete(attachment)
    db.commit()
