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
#
#

# app/models/application.py
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship, foreign
from ..database.base import Base
import enum
from typing import Optional, Dict, Any

class ApplicationType(str, enum.Enum):
    CONTAINER = "container"  # Deployed as container(s) in a container cluster
    VM = "vm"                # Deployed directly to a VM
    PHYSICAL = "physical"    # Deployed directly to a physical host

class DeploymentStatus(str, enum.Enum):
    PENDING = "pending"      # Deployment requested but not started
    DEPLOYING = "deploying"  # Deployment in progress
    DEPLOYED = "deployed"    # Successfully deployed
    FAILED = "failed"        # Deployment failed
    UPGRADING = "upgrading"  # Upgrade in progress
    REMOVING = "removing"    # Removal in progress
    REMOVED = "removed"      # Successfully removed

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    description = Column(String(1024), nullable=True)
    plugin_name = Column(String(255), nullable=False)  # Name of the plugin template
    plugin_version = Column(String(20), nullable=False)  # Version of the plugin template
    application_type = Column(Enum(ApplicationType), nullable=False)
    deployment_status = Column(Enum(DeploymentStatus), default=DeploymentStatus.PENDING)
    config = Column(JSON, nullable=True)  # Configuration parameters for the application
    is_active = Column(Boolean, default=True)
    element_id = Column(Integer, ForeignKey("elements.id"), nullable=False)

    # Target deployment relationships - only one of these should be set based on application_type
    stack_id = Column(Integer, ForeignKey("stacks.id"), nullable=True)  # For CONTAINER type
    vm_id = Column(Integer, ForeignKey("vms.id"), nullable=True)  # For VM type
    physical_host_id = Column(Integer, ForeignKey("physical_hosts.id"), nullable=True)  # For PHYSICAL type

    # Relationships
    stack = relationship("Stack", back_populates="applications")
    vm = relationship("VM", back_populates="applications")
    physical_host = relationship("PhysicalHost", back_populates="applications")
    element = relationship("Element", backref="application")

    # Relationship to volume attachments
    volume_attachments = relationship("VolumeApplication", back_populates="application")

    # Property to get volumes
    @property
    def volumes(self):
        return [attachment.volume for attachment in self.volume_attachments]

    # Relationship to network attachments
    network_attachments = relationship("NetworkApplication", back_populates="application")

    def __repr__(self):
        return f"<Application(id={self.id}, name='{self.name}', type='{self.application_type}', status='{self.deployment_status}', element_id={self.element_id})>"
