from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database.base import Base

class Function(Base):
    __tablename__ = "functions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Relation avec les groupes via la table d'association group_functions
    groups = relationship("Group", secondary="group_functions", back_populates="functions")
