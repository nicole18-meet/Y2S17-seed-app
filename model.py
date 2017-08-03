import datetime

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

    created_at    = Column(DateTime, default=datetime.datetime.now)

    owner         = Column(Integer, ForeignKey("user.id"))
    shoots        = relationship('Shoot')
    

class Shoot(Base):
    __tablename__ = 'shoot'
    id            = Column(Integer, primary_key=True)
    title         = Column(String)
    taken_time    = Column(DateTime)
    is_taken      = Column(Boolean, default=False)
    is_missed     = Column(Boolean, default=False)

    routine   	  = Column(Integer, ForeignKey("routine.id"))