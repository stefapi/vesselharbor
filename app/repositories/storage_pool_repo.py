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

# app/repositories/storage_pool_repo.py
from sqlalchemy.orm import Session
from typing import List
from ..models.storage_pool import StoragePool, StoragePoolType, StoragePoolScope
from ..models.volume import Volume


def create_storage_pool(
    db: Session,
    type: StoragePoolType,
    scope: StoragePoolScope,
    parameters: dict = None,
    environment_id: int = None
) -> StoragePool:
    storage_pool = StoragePool(
        type=type,
        scope=scope,
        parameters=parameters,
        environment_id=environment_id if scope == StoragePoolScope.ENVIRONMENT else None
    )
    db.add(storage_pool)
    db.commit()
    db.refresh(storage_pool)
    return storage_pool


def get_storage_pool(db: Session, storage_pool_id: int) -> StoragePool:
    return db.query(StoragePool).filter(StoragePool.id == storage_pool_id).first()


def update_storage_pool(
    db: Session,
    storage_pool: StoragePool,
    type: StoragePoolType = None,
    scope: StoragePoolScope = None,
    parameters: dict = None,
    environment_id: int = None
) -> StoragePool:
    if type is not None:
        storage_pool.type = type
    if scope is not None:
        storage_pool.scope = scope
        # If scope changes to/from ENVIRONMENT, update environment_id accordingly
        if scope == StoragePoolScope.ENVIRONMENT:
            storage_pool.environment_id = environment_id
        else:
            storage_pool.environment_id = None
    if parameters is not None:
        storage_pool.parameters = parameters
    # Only update environment_id if scope is ENVIRONMENT and environment_id is provided
    if environment_id is not None and storage_pool.scope == StoragePoolScope.ENVIRONMENT:
        storage_pool.environment_id = environment_id
    db.commit()
    db.refresh(storage_pool)
    return storage_pool


def delete_storage_pool(db: Session, storage_pool: StoragePool):
    db.delete(storage_pool)
    db.commit()


def list_storage_pools(db: Session, skip: int = 0, limit: int = 100):
    return db.query(StoragePool).offset(skip).limit(limit).all()


def list_storage_pools_by_type(db: Session, type: StoragePoolType):
    return db.query(StoragePool).filter(StoragePool.type == type).all()


def list_storage_pools_by_scope(db: Session, scope: StoragePoolScope):
    return db.query(StoragePool).filter(StoragePool.scope == scope).all()


def list_storage_pools_by_environment(db: Session, environment_id: int):
    return db.query(StoragePool).filter(
        StoragePool.environment_id == environment_id,
        StoragePool.scope == StoragePoolScope.ENVIRONMENT
    ).all()


def list_storage_pools_by_host(db: Session, host_id: int):
    """List storage pools that are local to a specific host"""
    from ..database.session import DATABASE_URL
    import json

    # Different approach based on database type
    if "postgresql" in DATABASE_URL:
        # PostgreSQL approach using JSONB contains
        host_json = {"host_id": host_id}
        return db.query(StoragePool).filter(
            StoragePool.parameters.contains(host_json)
        ).all()
    else:
        # SQLite approach - fetch all and filter in Python
        # This is less efficient but works with SQLite
        all_pools = db.query(StoragePool).all()
        return [
            pool for pool in all_pools
            if pool.parameters and 'host_id' in pool.parameters and pool.parameters['host_id'] == host_id
        ]


def create_storage_pool_from_volumes(
    db: Session,
    volumes: List[Volume],
    type: StoragePoolType,
    scope: StoragePoolScope,
    parameters: dict = None,
    environment_id: int = None
) -> StoragePool:
    """
    Create a storage pool from a set of existing volumes.
    This emphasizes that volumes are assembled to constitute storage pools.

    Args:
        db: Database session
        volumes: List of volumes to include in the storage pool
        type: Type of storage pool
        scope: Scope of storage pool
        parameters: Additional parameters for the storage pool
        environment_id: ID of the environment if scope is ENVIRONMENT

    Returns:
        The newly created storage pool
    """
    # Create the storage pool
    storage_pool = StoragePool(
        type=type,
        scope=scope,
        parameters=parameters,
        environment_id=environment_id if scope == StoragePoolScope.ENVIRONMENT else None
    )
    db.add(storage_pool)
    db.flush()  # Flush to get the ID without committing

    # Update the volumes to be part of this storage pool
    for volume in volumes:
        volume.pool_id = storage_pool.id

    db.commit()
    db.refresh(storage_pool)
    return storage_pool


def add_volumes_to_storage_pool(
    db: Session,
    storage_pool: StoragePool,
    volumes: List[Volume]
) -> StoragePool:
    """
    Add volumes to an existing storage pool.
    This emphasizes that volumes are assembled to constitute storage pools.

    Args:
        db: Database session
        storage_pool: The storage pool to add volumes to
        volumes: List of volumes to add to the storage pool

    Returns:
        The updated storage pool
    """
    # Update the volumes to be part of this storage pool
    for volume in volumes:
        volume.pool_id = storage_pool.id

    db.commit()
    db.refresh(storage_pool)
    return storage_pool
