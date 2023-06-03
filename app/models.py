from .database import base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text
from sqlalchemy.orm import relationship

class Post2(base):
    __tablename__ = "Post3"
    ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    published = Column(Boolean, nullable=False, server_default=text("1"))
    rating = Column(Integer, nullable=False, server_default=text("2"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))

class user(base):
    __tablename__ = "Users"
    ID_user = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Password = Column(String(255), nullable=False)
    Email = Column(String(255), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


