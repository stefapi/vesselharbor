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

# app/models/physical_host.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from ..database.base import Base
import enum

class HypervisorType(str, enum.Enum):
    NONE = "none"
    LIBVIRT = "libvirt"
    PROXMOX = "proxmox"

class AllocationMode(str, enum.Enum):
    SHARED = "shared"
    DEDICATED = "dedicated"

class PhysicalHost(Base):
    __tablename__ = "physical_hosts"

    id = Column(Integer, primary_key=True, index=True)
    fqdn = Column(String(255), nullable=False, unique=True)
    ip_mgmt = Column(String(45), nullable=False)
    cpu_threads = Column(Integer, nullable=False)
    ram_mb = Column(Integer, nullable=False)
    disk_gb = Column(Integer, nullable=False)
    labels = Column(ARRAY(String), nullable=True)
    hypervisor_type = Column(Enum(HypervisorType), default=HypervisorType.NONE)
    is_schedulable = Column(Boolean, default=True)
    allocation_mode = Column(Enum(AllocationMode), default=AllocationMode.SHARED)
    dedicated_tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)

    # Relationships
    dedicated_tenant = relationship("Tenant", back_populates="physical_hosts")
    vms = relationship("VM", back_populates="host")
    container_nodes = relationship("ContainerNode", back_populates="host")
    applications = relationship("Application", back_populates="physical_host")

    # Property to get network attachments
    @property
    def network_attachments(self):
        from ..repositories import network_attachment_repo
        from ..models.network_attachment import AttachedToType
        from sqlalchemy.orm import Session
        from ..database.session import get_db
        db = next(get_db())
        return network_attachment_repo.list_network_attachments_by_attached_entity(
            db, AttachedToType.HOST, self.id
        )

    def __repr__(self):
        return f"<PhysicalHost(id={self.id}, fqdn='{self.fqdn}', hypervisor='{self.hypervisor_type}')>"
