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

# app/repositories/container_node_repo.py
from sqlalchemy.orm import Session
from typing import Optional
from ..models.container_node import ContainerNode, NodeRole

def create_container_node(
    db: Session,
    cluster_id: int,
    role: NodeRole,
    vm_id: Optional[int] = None,
    host_id: Optional[int] = None
) -> ContainerNode:
    # Ensure at least one of vm_id or host_id is provided
    if vm_id is None and host_id is None:
        raise ValueError("Either vm_id or host_id must be provided")

    container_node = ContainerNode(
        cluster_id=cluster_id,
        role=role,
        vm_id=vm_id,
        host_id=host_id
    )
    db.add(container_node)
    db.commit()
    db.refresh(container_node)
    return container_node

def get_container_node(db: Session, container_node_id: int) -> ContainerNode:
    return db.query(ContainerNode).filter(ContainerNode.id == container_node_id).first()

def list_container_nodes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ContainerNode).offset(skip).limit(limit).all()

def list_container_nodes_by_cluster(db: Session, cluster_id: int, skip: int = 0, limit: int = 100):
    return db.query(ContainerNode).filter(ContainerNode.cluster_id == cluster_id).offset(skip).limit(limit).all()

def list_container_nodes_by_role(db: Session, role: NodeRole, skip: int = 0, limit: int = 100):
    return db.query(ContainerNode).filter(ContainerNode.role == role).offset(skip).limit(limit).all()

def list_container_nodes_by_vm(db: Session, vm_id: int, skip: int = 0, limit: int = 100):
    return db.query(ContainerNode).filter(ContainerNode.vm_id == vm_id).offset(skip).limit(limit).all()

def list_container_nodes_by_host(db: Session, host_id: int, skip: int = 0, limit: int = 100):
    return db.query(ContainerNode).filter(ContainerNode.host_id == host_id).offset(skip).limit(limit).all()

def update_container_node(
    db: Session,
    container_node: ContainerNode,
    cluster_id: int = None,
    role: NodeRole = None,
    vm_id: Optional[int] = None,
    host_id: Optional[int] = None
) -> ContainerNode:
    if cluster_id is not None:
        container_node.cluster_id = cluster_id
    if role is not None:
        container_node.role = role
    if vm_id is not None:
        container_node.vm_id = vm_id
    if host_id is not None:
        container_node.host_id = host_id

    # Ensure at least one of vm_id or host_id is not None
    if container_node.vm_id is None and container_node.host_id is None:
        raise ValueError("Either vm_id or host_id must be provided")

    db.commit()
    db.refresh(container_node)
    return container_node

def delete_container_node(db: Session, container_node: ContainerNode):
    db.delete(container_node)
    db.commit()
