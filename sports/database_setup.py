import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Sport(Base):
    __tablename__ = 'sport'

    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable = False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
        }


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    dob = Column(Date, nullable = False)
    photo = Column(String(100))
    sport_id = Column(Integer, ForeignKey('sport.id'))
    sport = relationship(Sport)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'dob' : self.dob,
        }


engine = create_engine('sqlite:///sports.db')

Base.metadata.create_all(engine)

