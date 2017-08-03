from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id            = Column(Integer, primary_key=True)
    username      = Column(String)


class Routine(Base):
    __tablename__ = 'routine'
    id            = Column(Integer, primary_key=True)
    owner         = Column(Integer, ForeignKey("user.id"))
    shoots        = relationship('Shoot')
    

class Shoot(Base):
    __tablename__ = 'shoot'
    id            = Column(Integer, primary_key=True)
    taken_time    = Column(DateTime)
    is_taken      = Column(Boolean, default=False)
    is_missed     = Column(Boolean)
    routine   	  = Column(Integer, ForeignKey("routine.id"))