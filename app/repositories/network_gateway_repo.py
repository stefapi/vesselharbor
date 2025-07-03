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

# app/repositories/network_gateway_repo.py
from sqlalchemy.orm import Session
from ..models.network_gateway import NetworkGateway, NetworkDirection
from typing import Optional, List

def create_network_gateway(
    db: Session,
    network_id: int,
    gateway_id: int,
    ip_address: str,
    direction: NetworkDirection = NetworkDirection.UPSTREAM
) -> NetworkGateway:
    attachment = NetworkGateway(
        network_id=network_id,
        gateway_id=gateway_id,
        ip_address=ip_address,
        direction=direction
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment

def get_network_gateway(db: Session, attachment_id: int) -> Optional[NetworkGateway]:
    return db.query(NetworkGateway).filter(NetworkGateway.id == attachment_id).first()

def list_network_gateways(db: Session, skip: int = 0, limit: int = 100) -> List[NetworkGateway]:
    return db.query(NetworkGateway).offset(skip).limit(limit).all()

def list_network_gateways_by_network(db: Session, network_id: int) -> List[NetworkGateway]:
    return db.query(NetworkGateway).filter(NetworkGateway.network_id == network_id).all()

def list_network_gateways_by_gateway(db: Session, gateway_id: int) -> List[NetworkGateway]:
    return db.query(NetworkGateway).filter(NetworkGateway.gateway_id == gateway_id).all()

def update_network_gateway(
    db: Session,
    attachment: NetworkGateway,
    network_id: Optional[int] = None,
    gateway_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    direction: Optional[NetworkDirection] = None
) -> NetworkGateway:
    if network_id is not None:
        attachment.network_id = network_id
    if gateway_id is not None:
        attachment.gateway_id = gateway_id
    if ip_address is not None:
        attachment.ip_address = ip_address
    if direction is not None:
        attachment.direction = direction

    db.commit()
    db.refresh(attachment)
    return attachment

def delete_network_gateway(db: Session, attachment: NetworkGateway) -> None:
    db.delete(attachment)
    db.commit()

def list_upstream_networks_by_gateway(db: Session, gateway_id: int) -> List[NetworkGateway]:
    """
    List all upstream network attachments for a specific gateway.
    """
    return db.query(NetworkGateway).filter(
        NetworkGateway.gateway_id == gateway_id,
        NetworkGateway.direction == NetworkDirection.UPSTREAM
    ).all()

def list_downstream_networks_by_gateway(db: Session, gateway_id: int) -> List[NetworkGateway]:
    """
    List all downstream network attachments for a specific gateway.
    """
    return db.query(NetworkGateway).filter(
        NetworkGateway.gateway_id == gateway_id,
        NetworkGateway.direction == NetworkDirection.DOWNSTREAM
    ).all()

def get_upstream_networks_by_gateway(db: Session, gateway_id: int) -> List["Network"]:
    """
    Get all upstream networks for a specific gateway.
    Returns a list of Network objects.
    """
    from ..models.network import Network
    return db.query(Network).join(
        NetworkGateway,
        NetworkGateway.network_id == Network.id
    ).filter(
        NetworkGateway.gateway_id == gateway_id,
        NetworkGateway.direction == NetworkDirection.UPSTREAM
    ).all()

def get_downstream_networks_by_gateway(db: Session, gateway_id: int) -> List["Network"]:
    """
    Get all downstream networks for a specific gateway.
    Returns a list of Network objects.
    """
    from ..models.network import Network
    return db.query(Network).join(
        NetworkGateway,
        NetworkGateway.network_id == Network.id
    ).filter(
        NetworkGateway.gateway_id == gateway_id,
        NetworkGateway.direction == NetworkDirection.DOWNSTREAM
    ).all()
