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

# app/models/gateway.py
from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..database.base import Base
import enum

class GatewayKind(str, enum.Enum):
    TRAEFIK = "traefik"
    HAPROXY = "haproxy"
    NGINX = "nginx"

class CertStrategy(str, enum.Enum):
    LETSENCRYPT = "letsencrypt"
    CUSTOM = "custom"
    NONE = "none"

class Gateway(Base):
    __tablename__ = "gateways"

    id = Column(Integer, primary_key=True, index=True)
    kind = Column(Enum(GatewayKind), nullable=False)
    deployment_service_id = Column(Integer, ForeignKey("services.id", name="fk_gateway_service"), nullable=True)
    stack_id = Column(Integer, ForeignKey("stacks.id"), nullable=True)
    cert_strategy = Column(Enum(CertStrategy), nullable=False, default=CertStrategy.NONE)
    entrypoints = Column(JSONB, nullable=True)

    # Relationships
    # Note: The Service model is not defined yet, so this relationship will be established later
    # service = relationship("Service", back_populates="gateways")
    stack = relationship("Stack", back_populates="gateways")

    def __repr__(self):
        return f"<Gateway(id={self.id}, kind='{self.kind}', cert_strategy='{self.cert_strategy}')>"
