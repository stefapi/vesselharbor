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

# app/repositories/physical_host_repo.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.physical_host import PhysicalHost, HypervisorType, AllocationMode

def create_physical_host(
    db: Session,
    fqdn: str,
    ip_mgmt: str,
    cpu_threads: int,
    ram_mb: int,
    labels: List[str] = None,
    hypervisor_type: HypervisorType = HypervisorType.NONE,
    is_schedulable: bool = True,
    allocation_mode: AllocationMode = AllocationMode.SHARED,
    dedicated_environment_id: Optional[int] = None
) -> PhysicalHost:
    physical_host = PhysicalHost(
        fqdn=fqdn,
        ip_mgmt=ip_mgmt,
        cpu_threads=cpu_threads,
        ram_mb=ram_mb,
        labels=labels,
        hypervisor_type=hypervisor_type,
        is_schedulable=is_schedulable,
        allocation_mode=allocation_mode,
        dedicated_environment_id=dedicated_environment_id
    )
    db.add(physical_host)
    db.commit()
    db.refresh(physical_host)
    return physical_host

def get_physical_host(db: Session, physical_host_id: int) -> PhysicalHost:
    return db.query(PhysicalHost).filter(PhysicalHost.id == physical_host_id).first()

def get_physical_host_by_fqdn(db: Session, fqdn: str) -> PhysicalHost:
    return db.query(PhysicalHost).filter(PhysicalHost.fqdn == fqdn).first()

def list_physical_hosts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PhysicalHost).offset(skip).limit(limit).all()

def list_physical_hosts_by_environment(db: Session, environment_id: int, skip: int = 0, limit: int = 100):
    return db.query(PhysicalHost).filter(PhysicalHost.dedicated_environment_id == environment_id).offset(skip).limit(limit).all()

def list_physical_hosts_by_hypervisor(db: Session, hypervisor_type: HypervisorType, skip: int = 0, limit: int = 100):
    return db.query(PhysicalHost).filter(PhysicalHost.hypervisor_type == hypervisor_type).offset(skip).limit(limit).all()

def list_schedulable_physical_hosts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PhysicalHost).filter(PhysicalHost.is_schedulable == True).offset(skip).limit(limit).all()

def update_physical_host(
    db: Session,
    physical_host: PhysicalHost,
    fqdn: str = None,
    ip_mgmt: str = None,
    cpu_threads: int = None,
    ram_mb: int = None,
    labels: List[str] = None,
    hypervisor_type: HypervisorType = None,
    is_schedulable: bool = None,
    allocation_mode: AllocationMode = None,
    dedicated_environment_id: Optional[int] = None
) -> PhysicalHost:
    if fqdn is not None:
        physical_host.fqdn = fqdn
    if ip_mgmt is not None:
        physical_host.ip_mgmt = ip_mgmt
    if cpu_threads is not None:
        physical_host.cpu_threads = cpu_threads
    if ram_mb is not None:
        physical_host.ram_mb = ram_mb
    if labels is not None:
        physical_host.labels = labels
    if hypervisor_type is not None:
        physical_host.hypervisor_type = hypervisor_type
    if is_schedulable is not None:
        physical_host.is_schedulable = is_schedulable
    if allocation_mode is not None:
        physical_host.allocation_mode = allocation_mode
    if dedicated_environment_id is not None:
        physical_host.dedicated_environment_id = dedicated_environment_id
    db.commit()
    db.refresh(physical_host)
    return physical_host

def delete_physical_host(db: Session, physical_host: PhysicalHost):
    db.delete(physical_host)
    db.commit()
