from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    environment_id = Column(Integer, ForeignKey("environments.id"), nullable=True)  # Optionnel : si NULL, groupe global

    # Relation avec Environment (si défini)
    environment = relationship("Environment", back_populates="groups")
    # Relation many-to-many avec Function via la table d'association group_functions (non montrée ici)
    functions = relationship("Function", secondary="group_functions", back_populates="groups")
    # Relation avec les affectations d’utilisateurs
    user_assignments = relationship("UserAssignment", back_populates="group")

    def __repr__(self):
        env = self.environment.name if self.environment else "Global"
        return f"<Group(id={self.id}, name='{self.name}', environment='{env}')>"
