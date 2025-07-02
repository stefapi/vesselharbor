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

# app/models/storage_pool.py
from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..database.base import Base
import enum


class StoragePoolType(str, enum.Enum):
    NFS = "nfs"
    CEPH = "ceph"
    LONGHORN = "longhorn"
    EBS = "ebs"


class StoragePoolScope(str, enum.Enum):
    GLOBAL = "global"
    TENANT = "tenant"
    PROJECT = "project"


class StoragePool(Base):
    __tablename__ = "storage_pools"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(StoragePoolType), nullable=False)
    parameters = Column(JSONB, nullable=True)
    scope = Column(Enum(StoragePoolScope), nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)

    # Relationships
    tenant = relationship("Tenant", back_populates="storage_pools")
    volumes = relationship("Volume", back_populates="storage_pool")

    @property
    def host(self):
        """Get the host if this storage pool is host-local"""
        if self.parameters and 'host_id' in self.parameters:
            from ..repositories import physical_host_repo
            from ..database.session import get_db
            db = next(get_db())
            return physical_host_repo.get_physical_host(db, self.parameters['host_id'])
        return None

    def __repr__(self):
        return f"<StoragePool(id={self.id}, type='{self.type}', scope='{self.scope}')>"
