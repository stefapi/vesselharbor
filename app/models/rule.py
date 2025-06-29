# models/rule.py
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from ..database.base import Base

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True)
    policy_id = Column(Integer, ForeignKey("policies.id", ondelete="CASCADE"), nullable=False)
    function_id = Column(Integer, ForeignKey("functions.id"), nullable=False)
    environment_id = Column(Integer, ForeignKey("environments.id", ondelete="CASCADE"), nullable=True)
    element_id = Column(Integer, ForeignKey("elements.id", ondelete="CASCADE"), nullable=True)
    access_schedule = Column(String(80), nullable=True)

    policy = relationship("Policy", back_populates="rules")
    function = relationship("Function", back_populates="rules")
    environment = relationship("Environment", back_populates="rules")
    element = relationship("Element", back_populates="rules")

    def __repr__(self):
        parts = [f"function='{self.function.name}'"]
        if self.environment:
            parts.append(f"env='{self.environment.name}'")
        if self.element:
            parts.append(f"element='{self.element.name}'")
        return f"<Rule(id={self.id}, {' '.join(parts)})>"
