import datetime, pytz
from sqlalchemy import *
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

eat_timezone = pytz.timezone('Africa/Nairobi')


class Office(Base):
    __tablename__ = "office"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    spaces = Column(Integer, nullable=False, default=6)
    created_at = Column(DateTime, default=datetime.datetime.now(eat_timezone))
    fellows = relationship("Fellow", backref="office")
    staff = relationship("Staff", backref="office")

    def __init__(self, name, spaces):
        self.name = name
        self.spaces = spaces

    def __eq__(self, other):
        return self.name == other.name and self.spaces == self.spaces


class Livingspace(Base):
    __tablename__ = "livingspace"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    spaces = Column(Integer, nullable=False, default=4)
    created_at = Column(DateTime, default=datetime.datetime.now(eat_timezone))
    fellows = relationship("Fellow", backref="livingspace")

    def __init__(self, name, spaces):
        self.name = name
        self.spaces = spaces

    def __eq__(self, other):
        return self.name == other.name and self.spaces == other.spaces


class Fellow(Base):
    __tablename__ = "fellow"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    accommodation = Column(String, nullable=False, default='N')
    created_at = Column(DateTime, default=datetime.datetime.now(eat_timezone))
    livingspace_id = Column(Integer, ForeignKey("livingspace.id"), nullable=True)
    office_id = Column(Integer, ForeignKey("office.id"), nullable=True)

    def __init__(self, name, accommodation):
        self.name = name
        self.accommodation = accommodation

    def __eq__(self, other):
        return self.name == other.name and self.accommodation == other.accommodation


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(eat_timezone))
    office_id = Column(Integer, ForeignKey("office.id"), nullable=True)

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


