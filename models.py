from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class student(Base):
    __tablename__ = 'students'
    code = Column(Integer, primary_key=True)
    Name = Column(String)
    Regno = Column(Integer)
    created_at = Column(Date)
