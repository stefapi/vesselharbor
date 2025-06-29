# app/models/policy.py
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base
from .tag import policy_tags

# Liaison policy <-> group
policy_groups = Table(
    "policy_groups",
    Base.metadata,
    Column("policy_id", Integer, ForeignKey("policies.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
)

# Table de liaison user <-> policy
policy_users = Table(
    "policy_users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("policy_id", Integer, ForeignKey("policies.id", ondelete="CASCADE"), primary_key=True),
)



class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(1024), nullable=True)

    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)

    organization = relationship("Organization", back_populates="policies")
    rules = relationship("Rule", back_populates="policy", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=policy_tags, back_populates="policies")
    groups = relationship("Group", secondary=policy_groups, back_populates="policies")
    users = relationship("User", secondary=policy_users, back_populates="policies")

    def __repr__(self):
        return f"<Policy(id={self.id}, name='{self.name}', org='{self.organization.name}')>"
