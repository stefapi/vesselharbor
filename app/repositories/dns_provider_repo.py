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

# app/repositories/dns_provider_repo.py
from sqlalchemy.orm import Session
from ..models.dns_provider import DNSProvider

def create_dns_provider(db: Session, name: str, api_endpoint: str, creds: dict) -> DNSProvider:
    dns_provider = DNSProvider(name=name, api_endpoint=api_endpoint, creds=creds)
    db.add(dns_provider)
    db.commit()
    db.refresh(dns_provider)
    return dns_provider

def get_dns_provider(db: Session, dns_provider_id: int) -> DNSProvider:
    return db.query(DNSProvider).filter(DNSProvider.id == dns_provider_id).first()

def get_dns_provider_by_name(db: Session, name: str) -> DNSProvider:
    return db.query(DNSProvider).filter(DNSProvider.name == name).first()

def list_dns_providers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DNSProvider).offset(skip).limit(limit).all()

def update_dns_provider(db: Session, dns_provider: DNSProvider, name: str = None, api_endpoint: str = None, creds: dict = None) -> DNSProvider:
    if name is not None:
        dns_provider.name = name
    if api_endpoint is not None:
        dns_provider.api_endpoint = api_endpoint
    if creds is not None:
        dns_provider.creds = creds
    db.commit()
    db.refresh(dns_provider)
    return dns_provider

def delete_dns_provider(db: Session, dns_provider: DNSProvider):
    db.delete(dns_provider)
    db.commit()
