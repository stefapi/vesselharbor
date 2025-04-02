from sqlalchemy import Table, Column, Integer, ForeignKey
from ..database.base import Base

group_functions = Table(
    'group_functions',
    Base.metadata,
    Column('group_id', Integer, ForeignKey("groups.id"), primary_key=True),
    Column('function_id', Integer, ForeignKey("functions.id"), primary_key=True)
)
