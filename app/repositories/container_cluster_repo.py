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

# app/repositories/container_cluster_repo.py
from sqlalchemy.orm import Session
from typing import Optional
from ..models.container_cluster import ContainerCluster, ClusterMode

def create_container_cluster(
    db: Session,
    mode: ClusterMode,
    version: str,
    endpoint: str,
    ha_enabled: bool = False,
    stack_id: Optional[int] = None
) -> ContainerCluster:
    container_cluster = ContainerCluster(
        mode=mode,
        version=version,
        endpoint=endpoint,
        ha_enabled=ha_enabled,
        stack_id=stack_id
    )
    db.add(container_cluster)
    db.commit()
    db.refresh(container_cluster)
    return container_cluster

def get_container_cluster(db: Session, container_cluster_id: int) -> ContainerCluster:
    return db.query(ContainerCluster).filter(ContainerCluster.id == container_cluster_id).first()

def list_container_clusters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ContainerCluster).offset(skip).limit(limit).all()

def list_container_clusters_by_mode(db: Session, mode: ClusterMode, skip: int = 0, limit: int = 100):
    return db.query(ContainerCluster).filter(ContainerCluster.mode == mode).offset(skip).limit(limit).all()

def list_container_clusters_by_stack(db: Session, stack_id: int, skip: int = 0, limit: int = 100):
    return db.query(ContainerCluster).filter(ContainerCluster.stack_id == stack_id).offset(skip).limit(limit).all()

def list_ha_container_clusters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ContainerCluster).filter(ContainerCluster.ha_enabled == True).offset(skip).limit(limit).all()

def update_container_cluster(
    db: Session,
    container_cluster: ContainerCluster,
    mode: ClusterMode = None,
    version: str = None,
    endpoint: str = None,
    ha_enabled: bool = None,
    stack_id: Optional[int] = None
) -> ContainerCluster:
    if mode is not None:
        container_cluster.mode = mode
    if version is not None:
        container_cluster.version = version
    if endpoint is not None:
        container_cluster.endpoint = endpoint
    if ha_enabled is not None:
        container_cluster.ha_enabled = ha_enabled
    if stack_id is not None:
        container_cluster.stack_id = stack_id
    db.commit()
    db.refresh(container_cluster)
    return container_cluster

def delete_container_cluster(db: Session, container_cluster: ContainerCluster):
    db.delete(container_cluster)
    db.commit()
