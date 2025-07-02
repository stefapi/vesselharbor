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

# app/repositories/domain_repo.py
from sqlalchemy.orm import Session
from ..models.domain import Domain
import datetime

def create_domain(
    db: Session,
    tenant_id: int,
    fqdn: str,
    provider_id: int,
    dnssec_enabled: bool = False
) -> Domain:
    domain = Domain(
        tenant_id=tenant_id,
        fqdn=fqdn,
        provider_id=provider_id,
        dnssec_enabled=dnssec_enabled,
        dnssec_status="pending" if dnssec_enabled else "insecure"
    )
    db.add(domain)
    db.commit()
    db.refresh(domain)
    return domain

def get_domain(db: Session, domain_id: int) -> Domain:
    return db.query(Domain).filter(Domain.id == domain_id).first()

def get_domain_by_fqdn(db: Session, fqdn: str) -> Domain:
    return db.query(Domain).filter(Domain.fqdn == fqdn).first()

def list_domains(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Domain).offset(skip).limit(limit).all()

def list_domains_by_tenant(db: Session, tenant_id: int):
    return db.query(Domain).filter(Domain.tenant_id == tenant_id).all()

def list_domains_by_provider(db: Session, provider_id: int):
    return db.query(Domain).filter(Domain.provider_id == provider_id).all()

def update_domain(
    db: Session,
    domain: Domain,
    tenant_id: int = None,
    fqdn: str = None,
    provider_id: int = None,
    dnssec_enabled: bool = None
) -> Domain:
    if tenant_id is not None:
        domain.tenant_id = tenant_id
    if fqdn is not None:
        domain.fqdn = fqdn
    if provider_id is not None:
        domain.provider_id = provider_id

    # Handle DNSSEC enabling/disabling
    if dnssec_enabled is not None and dnssec_enabled != domain.dnssec_enabled:
        if dnssec_enabled:
            domain = enable_dnssec(db, domain)
        else:
            domain = disable_dnssec(db, domain)
    else:
        db.commit()
        db.refresh(domain)

    return domain

def delete_domain(db: Session, domain: Domain):
    db.delete(domain)
    db.commit()

# DNSSEC related functions

def enable_dnssec(db: Session, domain: Domain) -> Domain:
    """
    Enable DNSSEC for a domain
    """
    domain.dnssec_enabled = True
    domain.dnssec_status = "pending"
    db.commit()
    db.refresh(domain)
    return domain

def disable_dnssec(db: Session, domain: Domain) -> Domain:
    """
    Disable DNSSEC for a domain
    """
    domain.dnssec_enabled = False
    domain.dnssec_status = "insecure"
    domain.dnssec_last_signed = None
    domain.dnssec_key_tag = None
    domain.dnssec_algorithm = None
    domain.dnssec_digest_type = None
    domain.dnssec_digest = None
    db.commit()
    db.refresh(domain)
    return domain

def update_dnssec_status(
    db: Session,
    domain: Domain,
    status: str,
    key_tag: int = None,
    algorithm: int = None,
    digest_type: int = None,
    digest: str = None
) -> Domain:
    """
    Update DNSSEC status for a domain
    """
    domain.dnssec_status = status
    if status == "secure":
        domain.dnssec_last_signed = datetime.datetime.utcnow()

    if key_tag is not None:
        domain.dnssec_key_tag = key_tag
    if algorithm is not None:
        domain.dnssec_algorithm = algorithm
    if digest_type is not None:
        domain.dnssec_digest_type = digest_type
    if digest is not None:
        domain.dnssec_digest = digest

    db.commit()
    db.refresh(domain)
    return domain

def list_dnssec_enabled_domains(db: Session):
    """
    List all domains with DNSSEC enabled
    """
    return db.query(Domain).filter(Domain.dnssec_enabled == True).all()

def list_domains_by_dnssec_status(db: Session, status: str):
    """
    List domains by DNSSEC status
    """
    return db.query(Domain).filter(Domain.dnssec_status == status).all()
