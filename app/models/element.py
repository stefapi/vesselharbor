# app/models/element.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base

class Element(Base):
    __tablename__ = "elements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    description = Column(String(1024), nullable=True)
    environment_id = Column(Integer, ForeignKey("environments.id"), nullable=False)

    environment = relationship("Environment", back_populates="elements")
    rules = relationship("Rule", back_populates="element")  # pour voir où cet élément est utilisé dans des règles

    @property
    def groups(self):
        # Toutes les rules pointant vers cet element → policy → groups
        group_set = set()
        for rule in self.rules:
            for group in rule.policy.groups:
                group_set.add(group)
        return list(group_set)

    @property
    def users(self):
        # Toutes les rules pointant vers cet element → policy → users + users des groupes
        user_set = set()
        for rule in self.rules:
            for user in rule.policy.users:
                user_set.add(user)
            for group in rule.policy.groups:
                for user in group.users:
                    user_set.add(user)
        return list(user_set)

    def __repr__(self):
        return f"<Element(id={self.id}, name='{self.name}', env_id={self.environment_id})>"
