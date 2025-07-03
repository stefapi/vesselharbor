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

# app/repositories/volume_container_cluster_repo.py
from sqlalchemy.orm import Session
from ..models.volume_container_cluster import VolumeContainerCluster
from typing import List, Optional

def create_volume_container_cluster(
    db: Session,
    volume_id: int,
    container_cluster_id: int
) -> VolumeContainerCluster:
    attachment = VolumeContainerCluster(
        volume_id=volume_id,
        container_cluster_id=container_cluster_id
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment

def get_volume_container_cluster(db: Session, attachment_id: int) -> Optional[VolumeContainerCluster]:
    return db.query(VolumeContainerCluster).filter(VolumeContainerCluster.id == attachment_id).first()

def get_volume_container_cluster_by_ids(db: Session, volume_id: int, container_cluster_id: int) -> Optional[VolumeContainerCluster]:
    return db.query(VolumeContainerCluster).filter(
        VolumeContainerCluster.volume_id == volume_id,
        VolumeContainerCluster.container_cluster_id == container_cluster_id
    ).first()

def list_volume_container_clusters(db: Session, skip: int = 0, limit: int = 100) -> List[VolumeContainerCluster]:
    return db.query(VolumeContainerCluster).offset(skip).limit(limit).all()

def list_volume_container_clusters_by_volume(db: Session, volume_id: int) -> List[VolumeContainerCluster]:
    return db.query(VolumeContainerCluster).filter(VolumeContainerCluster.volume_id == volume_id).all()

def list_volume_container_clusters_by_container_cluster(db: Session, container_cluster_id: int) -> List[VolumeContainerCluster]:
    return db.query(VolumeContainerCluster).filter(VolumeContainerCluster.container_cluster_id == container_cluster_id).all()

def delete_volume_container_cluster(db: Session, attachment: VolumeContainerCluster) -> None:
    db.delete(attachment)
    db.commit()
