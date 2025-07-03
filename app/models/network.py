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

# app/models/network.py
from sqlalchemy import Column, Integer, Boolean, Enum, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, String
from ..database.base import Base
from ..database.session import DATABASE_URL
import enum

# Custom CIDR type that works with both PostgreSQL and SQLite
class CIDRType(TypeDecorator):
    impl = String

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            from sqlalchemy.dialects.postgresql import CIDR
            return dialect.type_descriptor(CIDR())
        else:
            return dialect.type_descriptor(String())

class NetworkType(str, enum.Enum):
    PHYSICAL = "physical"
    OVERLAY = "overlay"

class Network(Base):
    __tablename__ = "networks"

    id = Column(Integer, primary_key=True, index=True)
    cidr = Column(CIDRType, nullable=False)
    vlan = Column(Integer, nullable=True)
    type = Column(Enum(NetworkType), nullable=False)
    environment_scoped = Column(Boolean, default=False)
    element_id = Column(Integer, ForeignKey("elements.id"), nullable=False)

    # Relationships
    element = relationship("Element", backref="network")

    # Network attachments relationships
    physical_host_attachments = relationship("NetworkPhysicalHost", back_populates="network")
    vm_attachments = relationship("NetworkVM", back_populates="network")
    container_node_attachments = relationship("NetworkContainerNode", back_populates="network")
    application_attachments = relationship("NetworkApplication", back_populates="network")
    gateway_attachments = relationship("NetworkGateway", back_populates="network")


    def __repr__(self):
        return f"<Network(id={self.id}, cidr='{self.cidr}', type='{self.type}', element_id={self.element_id})>"
