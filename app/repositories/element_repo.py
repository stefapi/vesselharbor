# app/repositories/element_repo.py
from sqlalchemy.orm import Session
from typing import Optional, Union, Dict, Any
from ..models.element import Element
from ..models.tag import Tag
from ..models.network import Network, NetworkType
from ..models.vm import VM
from ..models.storage_pool import StoragePool, StoragePoolType, StoragePoolScope
from ..models.volume import Volume, VolumeMode
from ..models.domain import Domain
from ..models.container_node import ContainerNode, NodeRole
from ..models.container_cluster import ContainerCluster, ClusterMode
from ..models.stack import Stack
from ..models.application import Application, ApplicationType, DeploymentStatus


def has_subcomponent(element: Element) -> bool:
    """
    Check if an element has at least one sub-component.
    An element must have at least one sub-component to exist.

    Args:
        element: The element to check

    Returns:
        bool: True if the element has at least one sub-component, False otherwise
    """
    # Check if the element has any of the possible sub-components
    return any([
        hasattr(element, 'network') and element.network is not None,
        hasattr(element, 'vm') and element.vm is not None,
        hasattr(element, 'storage_pool') and element.storage_pool is not None,
        hasattr(element, 'volume') and element.volume is not None,
        hasattr(element, 'domain') and element.domain is not None,
        hasattr(element, 'container_node') and element.container_node is not None,
        hasattr(element, 'container_cluster') and element.container_cluster is not None,
        hasattr(element, 'stack') and element.stack is not None,
        hasattr(element, 'application') and element.application is not None,
    ])


def create_element(db: Session, environment_id: int, name: str, description: str = None) -> Element:
    """
    Create a new element.

    Note: This function should not be used directly, as it creates an element without any sub-components,
    which violates the constraint that an element must have at least one sub-component.
    Use create_element_with_subcomponent instead.

    Args:
        db: The database session
        environment_id: The ID of the environment to which the element belongs
        name: The name of the element
        description: An optional description of the element

    Returns:
        The created element
    """
    element = Element(name=name, description=description, environment_id=environment_id)
    db.add(element)
    db.commit()
    db.refresh(element)
    return element

def get_element(db: Session, element_id: int) -> Element:
    return db.query(Element).filter(Element.id == element_id).first()

def update_element(db: Session, element: Element, name: str = None, description: str = None, environment_id: int = None) -> Element:
    if name is not None:
        element.name = name
    if description is not None:
        element.description = description
    if environment_id is not None:
        element.environment_id = environment_id
    db.commit()
    db.refresh(element)
    return element

def create_element_with_subcomponent(
    db: Session,
    environment_id: int,
    name: str,
    description: Optional[str] = None,
    subcomponent_type: str = None,
    subcomponent_data: Dict[str, Any] = None
) -> Element:
    """
    Create a new element with a sub-component.

    Args:
        db: The database session
        environment_id: The ID of the environment to which the element belongs
        name: The name of the element
        description: An optional description of the element
        subcomponent_type: The type of sub-component to create ('network', 'vm', 'storage_pool', etc.)
        subcomponent_data: A dictionary of data for the sub-component

    Returns:
        The created element with the sub-component

    Raises:
        ValueError: If subcomponent_type is not valid or if required data for the sub-component is missing
    """
    # Create the element
    element = Element(name=name, description=description, environment_id=environment_id)
    db.add(element)
    db.flush()  # Flush to get the element ID without committing the transaction

    # Create the sub-component based on the type
    if subcomponent_type == 'network':
        if not subcomponent_data or 'cidr' not in subcomponent_data or 'type' not in subcomponent_data:
            raise ValueError("Network requires 'cidr' and 'type' data")

        network_type = subcomponent_data['type']
        if isinstance(network_type, str):
            network_type = NetworkType(network_type)

        network = Network(
            cidr=subcomponent_data['cidr'],
            vlan=subcomponent_data.get('vlan'),
            type=network_type,
            environment_scoped=subcomponent_data.get('environment_scoped', False),
            element_id=element.id
        )
        db.add(network)

    elif subcomponent_type == 'vm':
        if not subcomponent_data or 'host_id' not in subcomponent_data or 'name' not in subcomponent_data:
            raise ValueError("VM requires 'host_id' and 'name' data")

        vm = VM(
            host_id=subcomponent_data['host_id'],
            name=subcomponent_data['name'],
            vcpu=subcomponent_data.get('vcpu', 1),
            ram_mb=subcomponent_data.get('ram_mb', 1024),
            disk_gb=subcomponent_data.get('disk_gb', 10),
            os_image=subcomponent_data.get('os_image', 'default'),
            stack_id=subcomponent_data.get('stack_id'),
            element_id=element.id
        )
        db.add(vm)

    elif subcomponent_type == 'storage_pool':
        if not subcomponent_data or 'type' not in subcomponent_data or 'scope' not in subcomponent_data:
            raise ValueError("StoragePool requires 'type' and 'scope' data")

        pool_type = subcomponent_data['type']
        if isinstance(pool_type, str):
            pool_type = StoragePoolType(pool_type)

        pool_scope = subcomponent_data['scope']
        if isinstance(pool_scope, str):
            pool_scope = StoragePoolScope(pool_scope)

        storage_pool = StoragePool(
            type=pool_type,
            parameters=subcomponent_data.get('parameters'),
            scope=pool_scope,
            element_id=element.id
        )
        db.add(storage_pool)

    elif subcomponent_type == 'volume':
        if not subcomponent_data or 'pool_id' not in subcomponent_data or 'size_gb' not in subcomponent_data or 'mode' not in subcomponent_data:
            raise ValueError("Volume requires 'pool_id', 'size_gb', and 'mode' data")

        volume_mode = subcomponent_data['mode']
        if isinstance(volume_mode, str):
            volume_mode = VolumeMode(volume_mode)

        volume = Volume(
            pool_id=subcomponent_data['pool_id'],
            size_gb=subcomponent_data['size_gb'],
            mode=volume_mode,
            element_id=element.id
        )
        db.add(volume)

    elif subcomponent_type == 'domain':
        if not subcomponent_data or 'fqdn' not in subcomponent_data:
            raise ValueError("Domain requires 'fqdn' data")

        domain = Domain(
            fqdn=subcomponent_data['fqdn'],
            dnssec_enabled=subcomponent_data.get('dnssec_enabled', False),
            element_id=element.id
        )
        db.add(domain)

    elif subcomponent_type == 'container_node':
        if not subcomponent_data or 'cluster_id' not in subcomponent_data or 'role' not in subcomponent_data:
            raise ValueError("ContainerNode requires 'cluster_id' and 'role' data")

        node_role = subcomponent_data['role']
        if isinstance(node_role, str):
            node_role = NodeRole(node_role)

        container_node = ContainerNode(
            cluster_id=subcomponent_data['cluster_id'],
            vm_id=subcomponent_data.get('vm_id'),
            host_id=subcomponent_data.get('host_id'),
            role=node_role,
            element_id=element.id
        )
        db.add(container_node)

    elif subcomponent_type == 'container_cluster':
        if not subcomponent_data or 'mode' not in subcomponent_data or 'version' not in subcomponent_data or 'endpoint' not in subcomponent_data:
            raise ValueError("ContainerCluster requires 'mode', 'version', and 'endpoint' data")

        cluster_mode = subcomponent_data['mode']
        if isinstance(cluster_mode, str):
            cluster_mode = ClusterMode(cluster_mode)

        container_cluster = ContainerCluster(
            mode=cluster_mode,
            version=subcomponent_data['version'],
            ha_enabled=subcomponent_data.get('ha_enabled', False),
            endpoint=subcomponent_data['endpoint'],
            stack_id=subcomponent_data.get('stack_id'),
            element_id=element.id
        )
        db.add(container_cluster)

    elif subcomponent_type == 'stack':
        if not subcomponent_data or 'name' not in subcomponent_data:
            raise ValueError("Stack requires 'name' data")

        stack = Stack(
            name=subcomponent_data['name'],
            description=subcomponent_data.get('description'),
            element_id=element.id
        )
        db.add(stack)

    elif subcomponent_type == 'application':
        if not subcomponent_data or 'name' not in subcomponent_data or 'plugin_name' not in subcomponent_data or 'plugin_version' not in subcomponent_data or 'application_type' not in subcomponent_data:
            raise ValueError("Application requires 'name', 'plugin_name', 'plugin_version', and 'application_type' data")

        app_type = subcomponent_data['application_type']
        if isinstance(app_type, str):
            app_type = ApplicationType(app_type)

        deployment_status = subcomponent_data.get('deployment_status', 'pending')
        if isinstance(deployment_status, str):
            deployment_status = DeploymentStatus(deployment_status)

        application = Application(
            name=subcomponent_data['name'],
            description=subcomponent_data.get('description'),
            plugin_name=subcomponent_data['plugin_name'],
            plugin_version=subcomponent_data['plugin_version'],
            application_type=app_type,
            deployment_status=deployment_status,
            config=subcomponent_data.get('config'),
            is_active=subcomponent_data.get('is_active', True),
            stack_id=subcomponent_data.get('stack_id'),
            vm_id=subcomponent_data.get('vm_id'),
            physical_host_id=subcomponent_data.get('physical_host_id'),
            element_id=element.id
        )
        db.add(application)

    else:
        # If no valid sub-component type is provided, delete the element and raise an error
        db.delete(element)
        db.flush()
        raise ValueError(f"Invalid sub-component type: {subcomponent_type}. Must be one of: network, vm, storage_pool, volume, domain, container_node, container_cluster, stack, application")

    # Commit the transaction
    db.commit()
    db.refresh(element)

    return element


def delete_element(db: Session, element: Element):
    db.delete(element)
    db.commit()

def list_elements_by_environment(db: Session, environment_id: int):
    return db.query(Element).filter(Element.environment_id == environment_id).all()

def add_tag_to_element(db: Session, element: Element, tag: Tag):
    if tag not in element.tags:
        element.tags.append(tag)
        db.commit()
        db.refresh(element)

def remove_tag_from_element(db: Session, element: Element, tag: Tag):
    if tag in element.tags:
        element.tags.remove(tag)
        db.commit()
        db.refresh(element)

        # Check if the tag is still referenced by any entity
        from ..repositories import tag_repo
        if not tag_repo.is_tag_referenced(db, tag):
            # If the tag is no longer referenced, delete it
            tag_repo.delete_tag(db, tag)
