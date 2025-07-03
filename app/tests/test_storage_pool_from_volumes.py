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

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.volume import Volume, VolumeMode
from app.models.storage_pool import StoragePool, StoragePoolType, StoragePoolScope
from app.repositories import volume_repo, storage_pool_repo

def test_create_storage_pool_from_volumes():
    """Test creating a storage pool from a set of volumes"""
    db = SessionLocal()

    # First, create a temporary storage pool for initial volumes
    temp_pool = storage_pool_repo.create_storage_pool(
        db=db,
        type=StoragePoolType.NFS,
        scope=StoragePoolScope.GLOBAL,
        parameters={"temp": True}
    )

    # Create some volumes in the temporary pool
    volume1 = volume_repo.create_volume(
        db=db,
        pool_id=temp_pool.id,
        size_gb=10,
        mode=VolumeMode.RWO
    )

    volume2 = volume_repo.create_volume(
        db=db,
        pool_id=temp_pool.id,
        size_gb=20,
        mode=VolumeMode.RWX
    )

    volume3 = volume_repo.create_volume(
        db=db,
        pool_id=temp_pool.id,
        size_gb=30,
        mode=VolumeMode.RWO
    )

    # Get the volumes from the database
    volumes = [
        volume_repo.get_volume(db, volume1.id),
        volume_repo.get_volume(db, volume2.id),
        volume_repo.get_volume(db, volume3.id)
    ]

    # Create a new storage pool from these volumes
    new_pool = storage_pool_repo.create_storage_pool_from_volumes(
        db=db,
        volumes=volumes,
        type=StoragePoolType.CEPH,
        scope=StoragePoolScope.ENVIRONMENT,
        parameters={"assembled": True},
        environment_id=1  # Assuming environment with ID 1 exists
    )

    print(f"Created new storage pool: {new_pool}")

    # Verify that the volumes are now part of the new pool
    updated_volumes = volume_repo.list_volumes_by_pool(db, new_pool.id)
    print(f"Volumes in the new pool: {updated_volumes}")

    # Verify that the volumes are no longer part of the temporary pool
    remaining_volumes = volume_repo.list_volumes_by_pool(db, temp_pool.id)
    print(f"Volumes remaining in the temporary pool: {remaining_volumes}")

    # Clean up
    for volume in updated_volumes:
        volume_repo.delete_volume(db, volume)

    storage_pool_repo.delete_storage_pool(db, new_pool)
    storage_pool_repo.delete_storage_pool(db, temp_pool)

    print("Test completed and resources cleaned up")

    # Close the database session
    db.close()

def test_add_volumes_to_storage_pool():
    """Test adding volumes to an existing storage pool"""
    db = SessionLocal()

    # Create two storage pools
    pool1 = storage_pool_repo.create_storage_pool(
        db=db,
        type=StoragePoolType.NFS,
        scope=StoragePoolScope.GLOBAL,
        parameters={"pool": 1}
    )

    pool2 = storage_pool_repo.create_storage_pool(
        db=db,
        type=StoragePoolType.CEPH,
        scope=StoragePoolScope.GLOBAL,
        parameters={"pool": 2}
    )

    # Create some volumes in pool1
    volume1 = volume_repo.create_volume(
        db=db,
        pool_id=pool1.id,
        size_gb=10,
        mode=VolumeMode.RWO
    )

    volume2 = volume_repo.create_volume(
        db=db,
        pool_id=pool1.id,
        size_gb=20,
        mode=VolumeMode.RWX
    )

    # Get the volumes from the database
    volumes = [
        volume_repo.get_volume(db, volume1.id),
        volume_repo.get_volume(db, volume2.id)
    ]

    # Add the volumes to pool2
    updated_pool = storage_pool_repo.add_volumes_to_storage_pool(
        db=db,
        storage_pool=pool2,
        volumes=volumes
    )

    print(f"Updated storage pool: {updated_pool}")

    # Verify that the volumes are now part of pool2
    pool2_volumes = volume_repo.list_volumes_by_pool(db, pool2.id)
    print(f"Volumes in pool2: {pool2_volumes}")

    # Verify that the volumes are no longer part of pool1
    pool1_volumes = volume_repo.list_volumes_by_pool(db, pool1.id)
    print(f"Volumes in pool1: {pool1_volumes}")

    # Clean up
    for volume in pool2_volumes:
        volume_repo.delete_volume(db, volume)

    storage_pool_repo.delete_storage_pool(db, pool1)
    storage_pool_repo.delete_storage_pool(db, pool2)

    print("Test completed and resources cleaned up")

    # Close the database session
    db.close()

if __name__ == "__main__":
    print("Testing create_storage_pool_from_volumes...")
    test_create_storage_pool_from_volumes()

    print("\nTesting add_volumes_to_storage_pool...")
    test_add_volumes_to_storage_pool()
