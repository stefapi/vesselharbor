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

# app/repositories/network_repo.py
from sqlalchemy.orm import Session
from ..models.network import Network, NetworkType
from typing import Optional, List

def create_network(
    db: Session,
    cidr: str,
    type: NetworkType,
    vlan: Optional[int] = None,
    environment_scoped: bool = False,
    element_id: int = None
) -> Network:
    network = Network(
        cidr=cidr,
        vlan=vlan,
        type=type,
        environment_scoped=environment_scoped,
        element_id=element_id
    )
    db.add(network)
    db.commit()
    db.refresh(network)
    return network

def get_network(db: Session, network_id: int) -> Optional[Network]:
    return db.query(Network).filter(Network.id == network_id).first()

def get_network_by_cidr(db: Session, cidr: str) -> Optional[Network]:
    return db.query(Network).filter(Network.cidr == cidr).first()

def list_networks(db: Session, skip: int = 0, limit: int = 100) -> List[Network]:
    return db.query(Network).offset(skip).limit(limit).all()

def list_networks_by_type(db: Session, network_type: NetworkType) -> List[Network]:
    return db.query(Network).filter(Network.type == network_type).all()

def list_networks_by_element(db: Session, element_id: int) -> List[Network]:
    return db.query(Network).filter(Network.element_id == element_id).all()

def list_environment_scoped_networks(db: Session) -> List[Network]:
    return db.query(Network).filter(Network.environment_scoped == True).all()

def update_network(
    db: Session,
    network: Network,
    cidr: Optional[str] = None,
    vlan: Optional[int] = None,
    type: Optional[NetworkType] = None,
    environment_scoped: Optional[bool] = None,
    element_id: Optional[int] = None
) -> Network:
    if cidr is not None:
        network.cidr = cidr
    if vlan is not None:
        network.vlan = vlan
    if type is not None:
        network.type = type
    if environment_scoped is not None:
        network.environment_scoped = environment_scoped
    if element_id is not None:
        network.element_id = element_id

    db.commit()
    db.refresh(network)
    return network

def delete_network(db: Session, network: Network) -> None:
    db.delete(network)
    db.commit()
