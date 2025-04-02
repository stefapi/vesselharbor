from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database.base import Base


class Environment(Base):
    __tablename__ = "environments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    # Relation avec les groupes spécifiques à cet environnement.
    # Les groupes globaux n'auront pas d'environnement défini (environment_id = NULL).
    groups = relationship("Group", back_populates="environment")

    def __repr__(self):
        return f"<Environment(id={self.id}, name='{self.name}')>"
