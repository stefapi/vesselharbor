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

# app/repositories/gateway_repo.py
from sqlalchemy.orm import Session
from ..models.gateway import Gateway, GatewayKind, CertStrategy
from typing import Optional, List, Dict, Any

def create_gateway(
    db: Session,
    kind: GatewayKind,
    deployment_service_id: Optional[int] = None,
    stack_id: Optional[int] = None,
    cert_strategy: CertStrategy = CertStrategy.NONE,
    entrypoints: Optional[Dict[str, Any]] = None
) -> Gateway:
    gateway = Gateway(
        kind=kind,
        deployment_service_id=deployment_service_id,
        stack_id=stack_id,
        cert_strategy=cert_strategy,
        entrypoints=entrypoints
    )
    db.add(gateway)
    db.commit()
    db.refresh(gateway)
    return gateway

def get_gateway(db: Session, gateway_id: int) -> Optional[Gateway]:
    return db.query(Gateway).filter(Gateway.id == gateway_id).first()

def list_gateways(db: Session, skip: int = 0, limit: int = 100) -> List[Gateway]:
    return db.query(Gateway).offset(skip).limit(limit).all()

def list_gateways_by_kind(db: Session, kind: GatewayKind) -> List[Gateway]:
    return db.query(Gateway).filter(Gateway.kind == kind).all()

def list_gateways_by_service(db: Session, service_id: int) -> List[Gateway]:
    return db.query(Gateway).filter(Gateway.deployment_service_id == service_id).all()

def list_gateways_by_stack(db: Session, stack_id: int) -> List[Gateway]:
    return db.query(Gateway).filter(Gateway.stack_id == stack_id).all()

def update_gateway(
    db: Session,
    gateway: Gateway,
    kind: Optional[GatewayKind] = None,
    deployment_service_id: Optional[int] = None,
    stack_id: Optional[int] = None,
    cert_strategy: Optional[CertStrategy] = None,
    entrypoints: Optional[Dict[str, Any]] = None
) -> Gateway:
    if kind is not None:
        gateway.kind = kind
    if deployment_service_id is not None:
        gateway.deployment_service_id = deployment_service_id
    if stack_id is not None:
        gateway.stack_id = stack_id
    if cert_strategy is not None:
        gateway.cert_strategy = cert_strategy
    if entrypoints is not None:
        gateway.entrypoints = entrypoints

    db.commit()
    db.refresh(gateway)
    return gateway

def delete_gateway(db: Session, gateway: Gateway) -> None:
    db.delete(gateway)
    db.commit()
