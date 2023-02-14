from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(Text, nullable=False)
    role = Column(Text, nullable=False)

    objects = relationship("Object", back_populates="users")
    secure_matrix = relationship("SecureMatrix", back_populates="users")

class Object(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(Text, nullable=False)
    uri = Column(Text, nullable=False)

    users = relationship("User", back_populates="objects")
    secure_matrix = relationship("SecureMatrix", back_populates="objects")

class SecureMatrix(Base):
    __tablename__ = "secure_matrix"

    object_id = Column(Integer, ForeignKey("objects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    rights = Column(Integer, nullable=False)

    objects = relationship("Object", back_populates="secure_matrix")
    users = relationship("User", back_populates="secure_matrix")

