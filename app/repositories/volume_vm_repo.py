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

# app/repositories/volume_vm_repo.py
from sqlalchemy.orm import Session
from ..models.volume_vm import VolumeVM
from typing import List, Optional

def create_volume_vm(
    db: Session,
    volume_id: int,
    vm_id: int
) -> VolumeVM:
    attachment = VolumeVM(
        volume_id=volume_id,
        vm_id=vm_id
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment

def get_volume_vm(db: Session, attachment_id: int) -> Optional[VolumeVM]:
    return db.query(VolumeVM).filter(VolumeVM.id == attachment_id).first()

def get_volume_vm_by_ids(db: Session, volume_id: int, vm_id: int) -> Optional[VolumeVM]:
    return db.query(VolumeVM).filter(
        VolumeVM.volume_id == volume_id,
        VolumeVM.vm_id == vm_id
    ).first()

def list_volume_vms(db: Session, skip: int = 0, limit: int = 100) -> List[VolumeVM]:
    return db.query(VolumeVM).offset(skip).limit(limit).all()

def list_volume_vms_by_volume(db: Session, volume_id: int) -> List[VolumeVM]:
    return db.query(VolumeVM).filter(VolumeVM.volume_id == volume_id).all()

def list_volume_vms_by_vm(db: Session, vm_id: int) -> List[VolumeVM]:
    return db.query(VolumeVM).filter(VolumeVM.vm_id == vm_id).all()

def delete_volume_vm(db: Session, attachment: VolumeVM) -> None:
    db.delete(attachment)
    db.commit()
