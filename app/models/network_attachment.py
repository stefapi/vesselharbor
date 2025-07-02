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

# app/models/network_attachment.py
from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import relationship
from ..database.base import Base
import enum

class AttachedToType(str, enum.Enum):
    HOST = "host"
    VM = "vm"
    SERVICE = "service"
    APPLICATION = "application"

class NetworkAttachment(Base):
    __tablename__ = "network_attachments"

    id = Column(Integer, primary_key=True, index=True)
    network_id = Column(Integer, ForeignKey("networks.id"), nullable=False)
    attached_to_type = Column(Enum(AttachedToType), nullable=False)
    attached_to_id = Column(Integer, nullable=False)
    ip_address = Column(INET, nullable=False)

    # Relationships
    network = relationship("Network", back_populates="attachments")

    # These properties provide convenient access to the attached entity
    @property
    def physical_host(self):
        if self.attached_to_type == AttachedToType.HOST:
            from ..repositories import physical_host_repo
            from sqlalchemy.orm import Session
            from ..database.session import get_db
            db = next(get_db())
            return physical_host_repo.get_physical_host(db, self.attached_to_id)
        return None

    @property
    def vm(self):
        if self.attached_to_type == AttachedToType.VM:
            from ..repositories import vm_repo
            from sqlalchemy.orm import Session
            from ..database.session import get_db
            db = next(get_db())
            return vm_repo.get_vm(db, self.attached_to_id)
        return None

    @property
    def application(self):
        if self.attached_to_type == AttachedToType.APPLICATION:
            from ..repositories import application_repo
            from sqlalchemy.orm import Session
            from ..database.session import get_db
            db = next(get_db())
            return application_repo.get_application(db, self.attached_to_id)
        return None

    def __repr__(self):
        return f"<NetworkAttachment(id={self.id}, network_id={self.network_id}, attached_to_type='{self.attached_to_type}', attached_to_id={self.attached_to_id})>"
