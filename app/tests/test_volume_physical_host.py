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
from app.database.session import get_db
from app.models.volume import Volume
from app.models.physical_host import PhysicalHost
from app.models.volume_physical_host import VolumePhysicalHost
from app.repositories import volume_repo, physical_host_repo, volume_physical_host_repo

def test_volume_physical_host_relationship():
    """Test the relationship between volumes and physical hosts"""
    db = next(get_db())

    # Get a volume and a physical host
    volumes = volume_repo.list_volumes(db, limit=1)
    physical_hosts = physical_host_repo.list_physical_hosts(db, limit=1)

    if not volumes or not physical_hosts:
        print("No volumes or physical hosts found. Please create some first.")
        return

    volume = volumes[0]
    physical_host = physical_hosts[0]

    # Create a relationship between the volume and the physical host
    attachment = volume_physical_host_repo.create_volume_physical_host(
        db=db,
        volume_id=volume.id,
        physical_host_id=physical_host.id
    )

    print(f"Created attachment: {attachment}")

    # Verify the relationship
    attachments_by_volume = volume_physical_host_repo.list_volume_physical_hosts_by_volume(db, volume.id)
    attachments_by_host = volume_physical_host_repo.list_volume_physical_hosts_by_physical_host(db, physical_host.id)

    print(f"Attachments by volume: {attachments_by_volume}")
    print(f"Attachments by host: {attachments_by_host}")

    # Verify the properties
    volume_from_db = volume_repo.get_volume(db, volume.id)
    physical_host_from_db = physical_host_repo.get_physical_host(db, physical_host.id)

    print(f"Volume's physical hosts: {volume_from_db.physical_hosts}")
    print(f"Physical host's volumes: {[attachment.volume for attachment in physical_host_from_db.volume_attachments]}")

    # Clean up
    volume_physical_host_repo.delete_volume_physical_host(db, attachment)
    print("Attachment deleted")

if __name__ == "__main__":
    test_volume_physical_host_relationship()
