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

# app/repositories/network_container_node_repo.py
from sqlalchemy.orm import Session
from ..models.network_container_node import NetworkContainerNode
from typing import Optional, List

def create_network_container_node(
    db: Session,
    network_id: int,
    container_node_id: int,
    ip_address: str
) -> NetworkContainerNode:
    attachment = NetworkContainerNode(
        network_id=network_id,
        container_node_id=container_node_id,
        ip_address=ip_address
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment

def get_network_container_node(db: Session, attachment_id: int) -> Optional[NetworkContainerNode]:
    return db.query(NetworkContainerNode).filter(NetworkContainerNode.id == attachment_id).first()

def list_network_container_nodes(db: Session, skip: int = 0, limit: int = 100) -> List[NetworkContainerNode]:
    return db.query(NetworkContainerNode).offset(skip).limit(limit).all()

def list_network_container_nodes_by_network(db: Session, network_id: int) -> List[NetworkContainerNode]:
    return db.query(NetworkContainerNode).filter(NetworkContainerNode.network_id == network_id).all()

def list_network_container_nodes_by_container_node(db: Session, container_node_id: int) -> List[NetworkContainerNode]:
    return db.query(NetworkContainerNode).filter(NetworkContainerNode.container_node_id == container_node_id).all()

def update_network_container_node(
    db: Session,
    attachment: NetworkContainerNode,
    network_id: Optional[int] = None,
    container_node_id: Optional[int] = None,
    ip_address: Optional[str] = None
) -> NetworkContainerNode:
    if network_id is not None:
        attachment.network_id = network_id
    if container_node_id is not None:
        attachment.container_node_id = container_node_id
    if ip_address is not None:
        attachment.ip_address = ip_address

    db.commit()
    db.refresh(attachment)
    return attachment

def delete_network_container_node(db: Session, attachment: NetworkContainerNode) -> None:
    db.delete(attachment)
    db.commit()
