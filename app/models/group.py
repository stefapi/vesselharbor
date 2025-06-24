# app/models/group.py
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..database.base import Base

from .tag import group_tags  # table intermédiaire
from .policy import policy_groups

user_groups = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
)

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    description = Column(String(1024), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)

    organization = relationship("Organization", back_populates="groups")
    tags = relationship("Tag", secondary=group_tags, back_populates="groups")
    users = relationship("User", secondary=user_groups, back_populates="groups")
    policies = relationship("Policy", secondary=policy_groups, back_populates="groups")

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}', org='{self.organization.name}')>"
