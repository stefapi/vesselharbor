# app/models/environment.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base

class Environment(Base):
    __tablename__ = "environments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), unique=True, index=True, nullable=False)
    description = Column(String(1024), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)

    organization = relationship("Organization", back_populates="environments")
    elements = relationship("Element", back_populates="environment")
    rules = relationship("Rule", back_populates="environment")

    @property
    def users(self):
        # Tous les users ayant accès à l'environnement via une policy avec une règle sur cet env
        user_set = set()
        for rule in self.rules:
            for user in rule.policy.users:
                user_set.add(user)
            for group in rule.policy.groups:
                for user in group.users:
                    user_set.add(user)
        return list(user_set)

    @property
    def groups_with_access(self):
        group_set = set()
        for rule in self.rules:
            for group in rule.policy.groups:
                group_set.add(group)
        return list(group_set)

    def __repr__(self):
        return f"<Environment(id={self.id}, name='{self.name}', org_id={self.organization_id})>"
