from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base

class Element(Base):
    __tablename__ = "elements"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    environment_id = Column(Integer, ForeignKey("environments.id"), nullable=False)
