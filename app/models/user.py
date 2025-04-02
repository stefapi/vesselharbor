from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superadmin = Column(Boolean, default=False)

    user_assignments = relationship("UserAssignment", back_populates="user", cascade="all, delete-orphan")

    @property
    def groups(self):
        # Retourne la liste des groupes via les affectations (UserAssignment)
        return [assignment.group for assignment in self.user_assignments if assignment.group is not None]

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', is_superadmin={self.is_superadmin})>"
