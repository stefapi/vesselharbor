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

# app/models/container_cluster.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..database.base import Base
import enum

class ClusterMode(str, enum.Enum):
    DOCKER = "docker"
    SWARM = "swarm"
    K8S = "k8s"

class ContainerCluster(Base):
    __tablename__ = "container_clusters"

    id = Column(Integer, primary_key=True, index=True)
    mode = Column(Enum(ClusterMode), nullable=False)
    version = Column(String(20), nullable=False)
    ha_enabled = Column(Boolean, default=False)
    endpoint = Column(String(255), nullable=False)
    stack_id = Column(Integer, ForeignKey("stacks.id"), nullable=True)

    # Relationships
    stack = relationship("Stack", back_populates="container_clusters")
    nodes = relationship("ContainerNode", back_populates="cluster")

    # Property to get volumes
    @property
    def volumes(self):
        from ..repositories import volume_repo
        from ..models.volume import AttachedToType
        from ..database.session import get_db
        db = next(get_db())
        return volume_repo.list_volumes_by_attachment(
            db, AttachedToType.SERVICE, self.id
        )

    def __repr__(self):
        return f"<ContainerCluster(id={self.id}, mode='{self.mode}', version='{self.version}')>"
