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

# app/repositories/stack_repo.py
from sqlalchemy.orm import Session
from ..models.stack import Stack

def create_stack(db: Session, name: str, environment_id: int, description: str = None) -> Stack:
    stack = Stack(name=name, environment_id=environment_id, description=description)
    db.add(stack)
    db.commit()
    db.refresh(stack)
    return stack

def get_stack(db: Session, stack_id: int) -> Stack:
    return db.query(Stack).filter(Stack.id == stack_id).first()

def get_stack_by_name(db: Session, name: str) -> Stack:
    return db.query(Stack).filter(Stack.name == name).first()

def list_stacks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Stack).offset(skip).limit(limit).all()

def list_stacks_by_environment(db: Session, environment_id: int, skip: int = 0, limit: int = 100):
    return db.query(Stack).filter(Stack.environment_id == environment_id).offset(skip).limit(limit).all()

def update_stack(db: Session, stack: Stack, name: str = None, description: str = None, environment_id: int = None) -> Stack:
    if name is not None:
        stack.name = name
    if description is not None:
        stack.description = description
    if environment_id is not None:
        stack.environment_id = environment_id
    db.commit()
    db.refresh(stack)
    return stack

def delete_stack(db: Session, stack: Stack):
    db.delete(stack)
    db.commit()
