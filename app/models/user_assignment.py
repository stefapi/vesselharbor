from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database.base import Base

class UserAssignment(Base):
    __tablename__ = "user_assignments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)  # Obligatoire
    element_id = Column(Integer, ForeignKey("elements.id"), nullable=True)  # Optionnel

    user = relationship("User", back_populates="user_assignments")
    group = relationship("Group", back_populates="user_assignments")
    element = relationship("Element")

    __table_args__ = (UniqueConstraint("user_id", "group_id", "element_id", name="_user_group_elem_uc"),)

    def __repr__(self):
        return f"<UserAssignment(id={self.id}, user_id={self.user_id}, group_id={self.group_id}, element_id={self.element_id})>"
