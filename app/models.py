from .database import base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text
from sqlalchemy.orm import relationship
# nếu modify lại table, thì các cột sẽ không cập nhật như modify được bởi vì tên bảng đó đã tồn tại trong database
# cho nên, phải xóa bảng đó trong database đi

class user(base):
    __tablename__ = "Users"
    ID_user = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Password = Column(String(255), nullable=False)
    Email = Column(String(255), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Post2(base):
    __tablename__ = "Post_user"
    ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    published = Column(Boolean, nullable=False, server_default=text("1"))
    rating = Column(Integer, nullable=False, server_default=text("2"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    owner_id = Column(Integer, ForeignKey("Users.ID_user", ondelete="CASCADE"), nullable=False)
    owner = relationship("user")


