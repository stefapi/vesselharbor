# app/models/tag.py

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base

# Associations
group_tags = Table(
    "group_tags",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

user_tags = Table(
    "user_tags",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

policy_tags = Table(
    "policy_tags",
    Base.metadata,
    Column("policy_id", Integer, ForeignKey("policies.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

element_tags = Table(
    "element_tags",
    Base.metadata,
    Column("element_id", Integer, ForeignKey("elements.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

environment_tags = Table(
    "environment_tags",
    Base.metadata,
    Column("environment_id", Integer, ForeignKey("environments.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    value = Column(String(80), unique=True, nullable=False)

    users = relationship("User", secondary=user_tags, back_populates="tags")
    groups = relationship("Group", secondary=group_tags, back_populates="tags")
    policies = relationship("Policy", secondary=policy_tags, back_populates="tags")
    elements = relationship("Element", secondary=element_tags, back_populates="tags")
    environments = relationship("Environment", secondary=environment_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag(id={self.id}, value='{self.value}')>"
