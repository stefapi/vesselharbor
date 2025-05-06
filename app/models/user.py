# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from ..database.base import Base
from .tag import user_tags
from .policy import policy_users
from .organization import user_organizations
from .group import user_groups

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), unique=True, index=True, nullable=False)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    hashed_password = Column(String(1024), nullable=False)
    is_superadmin = Column(Boolean, default=False)

    tags = relationship("Tag", secondary=user_tags, back_populates="users")
    groups = relationship("Group", secondary=user_groups, back_populates="users")
    organizations = relationship("Organization", secondary=user_organizations, back_populates="users")
    policies = relationship("Policy", secondary=policy_users, back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', is_superadmin={self.is_superadmin})>"
