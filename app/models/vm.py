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

# app/models/vm.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, foreign
from ..database.base import Base

class VM(Base):
    __tablename__ = "vms"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("physical_hosts.id"), nullable=False)
    name = Column(String(80), nullable=False)
    vcpu = Column(Integer, nullable=False)
    ram_mb = Column(Integer, nullable=False)
    disk_gb = Column(Integer, nullable=False)
    os_image = Column(String(255), nullable=False)
    stack_id = Column(Integer, ForeignKey("stacks.id"), nullable=True)
    element_id = Column(Integer, ForeignKey("elements.id"), nullable=False)

    # Relationships
    host = relationship("PhysicalHost", back_populates="vms")
    stack = relationship("Stack", back_populates="vms")
    container_nodes = relationship("ContainerNode", back_populates="vm")
    applications = relationship("Application", back_populates="vm")
    element = relationship("Element", backref="vm")

    # Relationship to network attachments
    network_attachments = relationship("NetworkVM", back_populates="vm")

    # Relationship to volume attachments
    volume_attachments = relationship("VolumeVM", back_populates="vm")

    # Property to get volumes
    @property
    def volumes(self):
        return [attachment.volume for attachment in self.volume_attachments]

    def __repr__(self):
        return f"<VM(id={self.id}, name='{self.name}', host_id={self.host_id}, element_id={self.element_id})>"
