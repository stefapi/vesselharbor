# app/schema/element.py

from pydantic import BaseModel
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from .rule import RuleOut  # si on veut les inclure
from .user import UserOut
from .group import GroupOut
from .tag import TagOut
from .physical_host import PhysicalHostOut
from .network import NetworkOut
from .vm import VMOut
from .storage_pool import StoragePoolOut
from .volume import VolumeOut
from .domain import DomainOut
from .container_node import ContainerNodeOut
from .container_cluster import ContainerClusterOut
from .stack import StackOut
from .application import ApplicationOut
if TYPE_CHECKING:
    from .environment import EnvironmentBase

class ElementCreate(BaseModel):
    name: str
    description: Optional[str] = None
    environment_id: int
    subcomponent_type: str
    subcomponent_data: Dict[str, Any]

class ElementUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    environment_id: Optional[int] = None

class ElementBase(BaseModel):
    id: int
    name: str
    description: Optional[str]
    environment_id: int

class ElementOut(ElementBase):

    # Ajouts utiles
    environment: Optional['EnvironmentBase'] = None
    rules: Optional[List[RuleOut]] = []
    users: Optional[List[UserOut]] = []
    groups: Optional[List[GroupOut]] = []
    tags: Optional[List[TagOut]] = []
    environment_physical_hosts: Optional[List[PhysicalHostOut]] = []

    # Nouveaux éléments - un élément est associé à un seul item de chaque type
    network: Optional[NetworkOut] = None
    vm: Optional[VMOut] = None
    storage_pool: Optional[StoragePoolOut] = None
    volume: Optional[VolumeOut] = None
    domain: Optional[DomainOut] = None
    container_node: Optional[ContainerNodeOut] = None
    container_cluster: Optional[ContainerClusterOut] = None
    stack: Optional[StackOut] = None
    application: Optional[ApplicationOut] = None

    model_config = {
        "from_attributes": True
    }
