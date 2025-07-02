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
from ..models.storage_pool import StoragePool, StoragePoolType, StoragePoolScope


def create_storage_pool(
    db: Session,
    type: StoragePoolType,
    scope: StoragePoolScope,
    parameters: dict = None,
    tenant_id: int = None
) -> StoragePool:
    storage_pool = StoragePool(
        type=type,
        scope=scope,
        parameters=parameters,
        tenant_id=tenant_id if scope == StoragePoolScope.TENANT else None
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
    tenant_id: int = None
) -> StoragePool:
    if type is not None:
        storage_pool.type = type
    if scope is not None:
        storage_pool.scope = scope
        # If scope changes to/from TENANT, update tenant_id accordingly
        if scope == StoragePoolScope.TENANT:
            storage_pool.tenant_id = tenant_id
        else:
            storage_pool.tenant_id = None
    if parameters is not None:
        storage_pool.parameters = parameters
    # Only update tenant_id if scope is TENANT and tenant_id is provided
    if tenant_id is not None and storage_pool.scope == StoragePoolScope.TENANT:
        storage_pool.tenant_id = tenant_id
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


def list_storage_pools_by_tenant(db: Session, tenant_id: int):
    return db.query(StoragePool).filter(
        StoragePool.tenant_id == tenant_id,
        StoragePool.scope == StoragePoolScope.TENANT
    ).all()


def list_storage_pools_by_host(db: Session, host_id: int):
    """List storage pools that are local to a specific host"""
    # This requires parsing the JSONB parameters field
    from sqlalchemy.dialects.postgresql import JSONB
    from sqlalchemy import cast
    from sqlalchemy.sql.expression import literal

    # Create a JSON object with the host_id
    host_json = {"host_id": host_id}

    # Query for storage pools where parameters @> {"host_id": host_id}
    return db.query(StoragePool).filter(
        StoragePool.parameters.contains(host_json)
    ).all()
