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

# app/repositories/dns_record_repo.py
from sqlalchemy.orm import Session
from ..models.dns_record import DNSRecord, DNSRecordType

def create_dns_record(db: Session, domain_id: int, record_type: DNSRecordType, name: str, value: str, ttl: int = 3600) -> DNSRecord:
    dns_record = DNSRecord(domain_id=domain_id, type=record_type, name=name, value=value, ttl=ttl)
    db.add(dns_record)
    db.commit()
    db.refresh(dns_record)
    return dns_record

def get_dns_record(db: Session, dns_record_id: int) -> DNSRecord:
    return db.query(DNSRecord).filter(DNSRecord.id == dns_record_id).first()

def list_dns_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DNSRecord).offset(skip).limit(limit).all()

def list_dns_records_by_domain(db: Session, domain_id: int):
    return db.query(DNSRecord).filter(DNSRecord.domain_id == domain_id).all()

def list_dns_records_by_type(db: Session, domain_id: int, record_type: DNSRecordType):
    return db.query(DNSRecord).filter(DNSRecord.domain_id == domain_id, DNSRecord.type == record_type).all()

def update_dns_record(db: Session, dns_record: DNSRecord, record_type: DNSRecordType = None, name: str = None, value: str = None, ttl: int = None) -> DNSRecord:
    if record_type is not None:
        dns_record.type = record_type
    if name is not None:
        dns_record.name = name
    if value is not None:
        dns_record.value = value
    if ttl is not None:
        dns_record.ttl = ttl
    db.commit()
    db.refresh(dns_record)
    return dns_record

def delete_dns_record(db: Session, dns_record: DNSRecord):
    db.delete(dns_record)
    db.commit()
