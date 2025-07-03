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

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database.base import Base
import datetime

class Domain(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True, index=True)
    element_id = Column(Integer, ForeignKey("elements.id"), nullable=False)
    fqdn = Column(String(255), nullable=False, index=True)
    # provider_id = Column(Integer, ForeignKey("dns_providers.id"), nullable=False)

    # DNSSEC related fields
    dnssec_enabled = Column(Boolean, default=False, nullable=False)
    dnssec_status = Column(String(50), nullable=True)  # e.g., "secure", "insecure", "pending", "error"
    dnssec_last_signed = Column(DateTime, nullable=True)
    dnssec_key_tag = Column(Integer, nullable=True)  # DS record key tag
    dnssec_algorithm = Column(Integer, nullable=True)  # Algorithm used for signing
    dnssec_digest_type = Column(Integer, nullable=True)  # Digest type for DS record
    dnssec_digest = Column(String(255), nullable=True)  # DS record digest

    element = relationship("Element", backref="domain")
    # provider = relationship("DNSProvider")
    dns_records = relationship("DNSRecord", back_populates="domain", cascade="all, delete-orphan")
    dnssec_keys = relationship("DNSSECKey", back_populates="domain", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Domain(id={self.id}, fqdn='{self.fqdn}', element_id={self.element_id})>"
