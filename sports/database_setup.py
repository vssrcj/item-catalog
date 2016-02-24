import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    email = Column(String(250), nullable = False)
    name = Column(String(250), nullable = False)


class Sport(Base):
    __tablename__ = 'sport'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)
   

class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    dob = Column(Date, nullable = False)
    photo = Column(String(100))
    sport_id = Column(Integer, ForeignKey('sport.id'), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    sport = relationship(Sport, foreign_keys=[sport_id])
    user = relationship(User, foreign_keys=[user_id])


engine = create_engine('sqlite:///sports.db')

Base.metadata.create_all(engine)

