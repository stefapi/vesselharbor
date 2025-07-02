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

# app/repositories/application_repo.py
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..models.application import Application, ApplicationType, DeploymentStatus

def create_application(
    db: Session,
    name: str,
    plugin_name: str,
    plugin_version: str,
    application_type: ApplicationType,
    description: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None,
    stack_id: Optional[int] = None,
    vm_id: Optional[int] = None,
    physical_host_id: Optional[int] = None
) -> Application:
    """
    Create a new application.

    Args:
        db: Database session
        name: Name of the application
        plugin_name: Name of the plugin template
        plugin_version: Version of the plugin template
        application_type: Type of application (CONTAINER, VM, PHYSICAL)
        description: Optional description of the application
        config: Optional configuration parameters for the application
        stack_id: ID of the stack (for CONTAINER type)
        vm_id: ID of the VM (for VM type)
        physical_host_id: ID of the physical host (for PHYSICAL type)

    Returns:
        The created application
    """
    application = Application(
        name=name,
        description=description,
        plugin_name=plugin_name,
        plugin_version=plugin_version,
        application_type=application_type,
        config=config,
        stack_id=stack_id if application_type == ApplicationType.CONTAINER else None,
        vm_id=vm_id if application_type == ApplicationType.VM else None,
        physical_host_id=physical_host_id if application_type == ApplicationType.PHYSICAL else None
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

def get_application(db: Session, application_id: int) -> Optional[Application]:
    """
    Get an application by ID.

    Args:
        db: Database session
        application_id: ID of the application

    Returns:
        The application if found, None otherwise
    """
    return db.query(Application).filter(Application.id == application_id).first()

def get_application_by_name(db: Session, name: str) -> Optional[Application]:
    """
    Get an application by name.

    Args:
        db: Database session
        name: Name of the application

    Returns:
        The application if found, None otherwise
    """
    return db.query(Application).filter(Application.name == name).first()

def list_applications(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    application_type: Optional[ApplicationType] = None,
    deployment_status: Optional[DeploymentStatus] = None,
    stack_id: Optional[int] = None,
    vm_id: Optional[int] = None,
    physical_host_id: Optional[int] = None,
    is_active: Optional[bool] = None
) -> List[Application]:
    """
    List applications with optional filters.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        application_type: Filter by application type
        deployment_status: Filter by deployment status
        stack_id: Filter by stack ID
        vm_id: Filter by VM ID
        physical_host_id: Filter by physical host ID
        is_active: Filter by active status

    Returns:
        List of applications matching the filters
    """
    query = db.query(Application)

    if application_type:
        query = query.filter(Application.application_type == application_type)

    if deployment_status:
        query = query.filter(Application.deployment_status == deployment_status)

    if stack_id:
        query = query.filter(Application.stack_id == stack_id)

    if vm_id:
        query = query.filter(Application.vm_id == vm_id)

    if physical_host_id:
        query = query.filter(Application.physical_host_id == physical_host_id)

    if is_active is not None:
        query = query.filter(Application.is_active == is_active)

    return query.offset(skip).limit(limit).all()

def list_applications_by_plugin(
    db: Session,
    plugin_name: str,
    plugin_version: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Application]:
    """
    List applications by plugin name and optionally version.

    Args:
        db: Database session
        plugin_name: Name of the plugin
        plugin_version: Optional version of the plugin
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of applications matching the plugin name and version
    """
    query = db.query(Application).filter(Application.plugin_name == plugin_name)

    if plugin_version:
        query = query.filter(Application.plugin_version == plugin_version)

    return query.offset(skip).limit(limit).all()

def list_active_applications(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Application]:
    """
    List active applications.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of active applications
    """
    return db.query(Application).filter(Application.is_active == True).offset(skip).limit(limit).all()

def list_applications_by_status(
    db: Session,
    status: DeploymentStatus,
    skip: int = 0,
    limit: int = 100
) -> List[Application]:
    """
    List applications by deployment status.

    Args:
        db: Database session
        status: Deployment status
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of applications with the specified deployment status
    """
    return db.query(Application).filter(Application.deployment_status == status).offset(skip).limit(limit).all()

def update_application(
    db: Session,
    application: Application,
    name: Optional[str] = None,
    description: Optional[str] = None,
    plugin_version: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None,
    deployment_status: Optional[DeploymentStatus] = None,
    is_active: Optional[bool] = None,
    stack_id: Optional[int] = None,
    vm_id: Optional[int] = None,
    physical_host_id: Optional[int] = None
) -> Application:
    """
    Update an application.

    Args:
        db: Database session
        application: Application to update
        name: New name
        description: New description
        plugin_version: New plugin version
        config: New configuration
        deployment_status: New deployment status
        is_active: New active status
        stack_id: New stack ID (for CONTAINER type)
        vm_id: New VM ID (for VM type)
        physical_host_id: New physical host ID (for PHYSICAL type)

    Returns:
        The updated application
    """
    if name is not None:
        application.name = name

    if description is not None:
        application.description = description

    if plugin_version is not None:
        application.plugin_version = plugin_version

    if config is not None:
        application.config = config

    if deployment_status is not None:
        application.deployment_status = deployment_status

    if is_active is not None:
        application.is_active = is_active

    if application.application_type == ApplicationType.CONTAINER and stack_id is not None:
        application.stack_id = stack_id

    if application.application_type == ApplicationType.VM and vm_id is not None:
        application.vm_id = vm_id

    if application.application_type == ApplicationType.PHYSICAL and physical_host_id is not None:
        application.physical_host_id = physical_host_id

    db.commit()
    db.refresh(application)
    return application

def delete_application(db: Session, application: Application) -> None:
    """
    Delete an application.

    Args:
        db: Database session
        application: Application to delete
    """
    db.delete(application)
    db.commit()
