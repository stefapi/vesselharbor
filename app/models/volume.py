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


class AttachedToType(str, enum.Enum):
    VM = "vm"
    SERVICE = "service"
    APPLICATION = "application"


class Volume(Base):
    __tablename__ = "volumes"

    id = Column(Integer, primary_key=True, index=True)
    pool_id = Column(Integer, ForeignKey("storage_pools.id"), nullable=False)
    size_gb = Column(Integer, nullable=False)
    mode = Column(Enum(VolumeMode), nullable=False)
    attached_to_type = Column(Enum(AttachedToType), nullable=True)
    attached_to_id = Column(Integer, nullable=True)

    # Relationship to StoragePool
    storage_pool = relationship("StoragePool", back_populates="volumes")

    # Properties to access the attached entity
    @property
    def vm(self):
        if self.attached_to_type == AttachedToType.VM and self.attached_to_id:
            from ..repositories import vm_repo
            from ..database.session import get_db
            db = next(get_db())
            return vm_repo.get_vm(db, self.attached_to_id)
        return None

    @property
    def service(self):
        if self.attached_to_type == AttachedToType.SERVICE and self.attached_to_id:
            # This would need to be implemented based on how services are represented
            # For now, we'll assume it's a container cluster
            from ..repositories import container_cluster_repo
            from ..database.session import get_db
            db = next(get_db())
            return container_cluster_repo.get_container_cluster(db, self.attached_to_id)
        return None

    @property
    def application(self):
        if self.attached_to_type == AttachedToType.APPLICATION and self.attached_to_id:
            from ..repositories import application_repo
            from ..database.session import get_db
            db = next(get_db())
            return application_repo.get_application(db, self.attached_to_id)
        return None

    def __repr__(self):
        return f"<Volume(id={self.id}, pool_id={self.pool_id}, size_gb={self.size_gb}, mode='{self.mode}')>"
