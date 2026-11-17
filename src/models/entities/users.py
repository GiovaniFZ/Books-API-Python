# pylint-disable=R0903

from sqlalchemy import Column, String, Integer
from src.models.connection.base import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    def __repr__(self):
        return f"Users [id={self.id}, name={self.name}]"
