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

# app/repositories/dnssec_key_repo.py
from sqlalchemy.orm import Session
from ..models.dnssec_key import DNSSECKey, DNSSECKeyType, DNSSECKeyAlgorithm
import datetime

def create_dnssec_key(
    db: Session,
    domain_id: int,
    key_type: DNSSECKeyType,
    algorithm: DNSSECKeyAlgorithm,
    key_tag: int,
    flags: int,
    public_key: str,
    private_key: str = None,
    expiry_date: datetime.datetime = None
) -> DNSSECKey:
    """
    Create a new DNSSEC key for a domain
    """
    dnssec_key = DNSSECKey(
        domain_id=domain_id,
        key_type=key_type,
        algorithm=algorithm,
        key_tag=key_tag,
        flags=flags,
        public_key=public_key,
        private_key=private_key,
        expiry_date=expiry_date,
        activated_at=datetime.datetime.utcnow()  # Activate immediately by default
    )
    db.add(dnssec_key)
    db.commit()
    db.refresh(dnssec_key)
    return dnssec_key

def get_dnssec_key(db: Session, dnssec_key_id: int) -> DNSSECKey:
    """
    Get a DNSSEC key by ID
    """
    return db.query(DNSSECKey).filter(DNSSECKey.id == dnssec_key_id).first()

def list_dnssec_keys(db: Session, skip: int = 0, limit: int = 100):
    """
    List all DNSSEC keys with pagination
    """
    return db.query(DNSSECKey).offset(skip).limit(limit).all()

def list_dnssec_keys_by_domain(db: Session, domain_id: int):
    """
    List all DNSSEC keys for a specific domain
    """
    return db.query(DNSSECKey).filter(DNSSECKey.domain_id == domain_id).all()

def list_active_dnssec_keys_by_domain(db: Session, domain_id: int):
    """
    List active DNSSEC keys for a specific domain
    """
    return db.query(DNSSECKey).filter(
        DNSSECKey.domain_id == domain_id,
        DNSSECKey.is_active == True,
        (DNSSECKey.expiry_date == None) | (DNSSECKey.expiry_date > datetime.datetime.utcnow())
    ).all()

def list_dnssec_keys_by_type(db: Session, domain_id: int, key_type: DNSSECKeyType):
    """
    List DNSSEC keys of a specific type for a domain
    """
    return db.query(DNSSECKey).filter(
        DNSSECKey.domain_id == domain_id,
        DNSSECKey.key_type == key_type
    ).all()

def update_dnssec_key(
    db: Session,
    dnssec_key: DNSSECKey,
    is_active: bool = None,
    activated_at: datetime.datetime = None,
    revoked_at: datetime.datetime = None,
    expiry_date: datetime.datetime = None
) -> DNSSECKey:
    """
    Update a DNSSEC key's status fields
    """
    if is_active is not None:
        dnssec_key.is_active = is_active
    if activated_at is not None:
        dnssec_key.activated_at = activated_at
    if revoked_at is not None:
        dnssec_key.revoked_at = revoked_at
        # If a key is revoked, it's no longer active
        if revoked_at <= datetime.datetime.utcnow():
            dnssec_key.is_active = False
    if expiry_date is not None:
        dnssec_key.expiry_date = expiry_date

    db.commit()
    db.refresh(dnssec_key)
    return dnssec_key

def revoke_dnssec_key(db: Session, dnssec_key: DNSSECKey) -> DNSSECKey:
    """
    Revoke a DNSSEC key
    """
    dnssec_key.is_active = False
    dnssec_key.revoked_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(dnssec_key)
    return dnssec_key

def delete_dnssec_key(db: Session, dnssec_key: DNSSECKey):
    """
    Delete a DNSSEC key
    """
    db.delete(dnssec_key)
    db.commit()
