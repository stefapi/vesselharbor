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

# app/repositories/volume_repo.py
from sqlalchemy.orm import Session
from ..models.volume import Volume, VolumeMode


def create_volume(
    db: Session,
    pool_id: int,
    size_gb: int,
    mode: VolumeMode
) -> Volume:
    volume = Volume(
        pool_id=pool_id,
        size_gb=size_gb,
        mode=mode
    )
    db.add(volume)
    db.commit()
    db.refresh(volume)
    return volume


def get_volume(db: Session, volume_id: int) -> Volume:
    return db.query(Volume).filter(Volume.id == volume_id).first()


def update_volume(
    db: Session,
    volume: Volume,
    pool_id: int = None,
    size_gb: int = None,
    mode: VolumeMode = None
) -> Volume:
    if pool_id is not None:
        volume.pool_id = pool_id
    if size_gb is not None:
        volume.size_gb = size_gb
    if mode is not None:
        volume.mode = mode
    db.commit()
    db.refresh(volume)
    return volume


def delete_volume(db: Session, volume: Volume):
    db.delete(volume)
    db.commit()


def list_volumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Volume).offset(skip).limit(limit).all()


def list_volumes_by_pool(db: Session, pool_id: int):
    return db.query(Volume).filter(Volume.pool_id == pool_id).all()


def list_volumes_by_mode(db: Session, mode: VolumeMode):
    return db.query(Volume).filter(Volume.mode == mode).all()


# These functions are replaced by the specific repository functions for each attachment type:
# - volume_vm_repo.py
# - volume_container_cluster_repo.py
# - volume_application_repo.py
