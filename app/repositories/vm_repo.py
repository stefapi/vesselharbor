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

# app/repositories/vm_repo.py
from sqlalchemy.orm import Session
from typing import Optional
from ..models.vm import VM

def create_vm(
    db: Session,
    host_id: int,
    name: str,
    vcpu: int,
    ram_mb: int,
    disk_gb: int,
    os_image: str,
    stack_id: Optional[int] = None
) -> VM:
    vm = VM(
        host_id=host_id,
        name=name,
        vcpu=vcpu,
        ram_mb=ram_mb,
        disk_gb=disk_gb,
        os_image=os_image,
        stack_id=stack_id
    )
    db.add(vm)
    db.commit()
    db.refresh(vm)
    return vm

def get_vm(db: Session, vm_id: int) -> VM:
    return db.query(VM).filter(VM.id == vm_id).first()

def get_vm_by_name(db: Session, name: str) -> VM:
    return db.query(VM).filter(VM.name == name).first()

def list_vms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(VM).offset(skip).limit(limit).all()

def list_vms_by_host(db: Session, host_id: int, skip: int = 0, limit: int = 100):
    return db.query(VM).filter(VM.host_id == host_id).offset(skip).limit(limit).all()

def list_vms_by_stack(db: Session, stack_id: int, skip: int = 0, limit: int = 100):
    return db.query(VM).filter(VM.stack_id == stack_id).offset(skip).limit(limit).all()

def update_vm(
    db: Session,
    vm: VM,
    host_id: int = None,
    name: str = None,
    vcpu: int = None,
    ram_mb: int = None,
    disk_gb: int = None,
    os_image: str = None,
    stack_id: Optional[int] = None
) -> VM:
    if host_id is not None:
        vm.host_id = host_id
    if name is not None:
        vm.name = name
    if vcpu is not None:
        vm.vcpu = vcpu
    if ram_mb is not None:
        vm.ram_mb = ram_mb
    if disk_gb is not None:
        vm.disk_gb = disk_gb
    if os_image is not None:
        vm.os_image = os_image
    if stack_id is not None:
        vm.stack_id = stack_id
    db.commit()
    db.refresh(vm)
    return vm

def delete_vm(db: Session, vm: VM):
    db.delete(vm)
    db.commit()
