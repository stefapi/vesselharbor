# app/models/organization.py

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base

user_organizations = Table(
    "user_organizations",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("organization_id", Integer, ForeignKey("organizations.id"), primary_key=True),
)

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(1024), nullable=True)

    users = relationship("User", secondary=user_organizations, back_populates="organizations")
    environments = relationship("Environment", back_populates="organization")
    groups = relationship("Group", back_populates="organization")
    policies = relationship("Policy", back_populates="organization")

    @property
    def elements(self):
        return [el for env in self.environments for el in env.elements]

    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}')>"
