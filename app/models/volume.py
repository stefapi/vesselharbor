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

# app/models/volume.py
from sqlalchemy import Column, Integer, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from ..database.base import Base
import enum


class VolumeMode(str, enum.Enum):
    RWO = "rwo"  # ReadWriteOnce
    RWX = "rwx"  # ReadWriteMany


# This enum is no longer used as we now use liaison tables
# class AttachedToType(str, enum.Enum):
#     VM = "vm"
#     SERVICE = "service"
#     APPLICATION = "application"


class Volume(Base):
    __tablename__ = "volumes"

    id = Column(Integer, primary_key=True, index=True)
    pool_id = Column(Integer, ForeignKey("storage_pools.id"), nullable=False)
    size_gb = Column(Integer, nullable=False)
    mode = Column(Enum(VolumeMode), nullable=False)
    element_id = Column(Integer, ForeignKey("elements.id"), nullable=False)

    # Relationship to StoragePool and Element
    storage_pool = relationship("StoragePool", back_populates="volumes")
    element = relationship("Element", backref="volume")

    # Relationships to attachment tables
    vm_attachments = relationship("VolumeVM", back_populates="volume")
    container_cluster_attachments = relationship("VolumeContainerCluster", back_populates="volume")
    application_attachments = relationship("VolumeApplication", back_populates="volume")

    # Properties to access the attached entities
    @property
    def vms(self):
        return [attachment.vm for attachment in self.vm_attachments]


    @property
    def container_clusters(self):
        return [attachment.container_cluster for attachment in self.container_cluster_attachments]

    @property
    def applications(self):
        return [attachment.application for attachment in self.application_attachments]

    def __repr__(self):
        return f"<Volume(id={self.id}, pool_id={self.pool_id}, size_gb={self.size_gb}, mode='{self.mode}', element_id={self.element_id})>"
