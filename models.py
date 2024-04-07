from tkinter import CASCADE
import onedal
from pandas import Timestamp
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from database import Base

# if not exists, these datatables would be created after connection has been established. 
# If you, after the specified table exists, create another column, this would not be created in SQL_Alchemy, since the table exists already.
# The only solution is, if you do not want to use migration-tool, to drop the table first.

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    #referencing sqlalchemy class "User"
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
     __tablename__ = "votes"

     user_id = Column(Integer, ForeignKey(
         "users.id", ondelete="CASCADE"), primary_key=True)
     post_id = Column(Integer, ForeignKey(
         "posts.id", ondelete="CASCADE"), primary_key=True)