from sqlalchemy import Column, Integer, String
from database import Base


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String, nullable=False)
    body = Column(String)