# app/models/function.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database.base import Base

class Function(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    description = Column(String(1024), nullable=True)

    rules = relationship("Rule", back_populates="function")

    def __repr__(self):
        return f"<Function(id={self.id}, name='{self.name}')>"
