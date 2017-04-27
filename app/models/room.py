from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Office as DBOffice, Livingspace as DBLivingspace, engine


class Room(object):
    def __init__(self, name, space):
        self.name = name
        self.spaces = space

    def __eq__(self, other):
        return self.name == other.name

    def assign_person_space(self, person):
        person.office = self
        self.spaces -= 1
        return person

    def has_space(self):
        return self.spaces != 0

    def print_occupants(self, occupants):
        print self.name.upper()
        print "--------------------------"
        print ", ".join([occupant.name.upper() for occupant in self.get_occupants(occupants)])

    def get_occupants(self, occupants):
        return [occupant for occupant in occupants if occupant.office.name == self.name]


class Office(Room):
    SPACES = 6

    def __init__(self, name):
        super(self.__class__, self).__init__(name, self.SPACES)

    @staticmethod
    def create_from_db_object(db_office):
        if db_office:
            office = Office(db_office.name)
            office.spaces = db_office.spaces
            return office
        return None


    @staticmethod
    def save(dojo):
        session = dojo.session

        with session.no_autoflush:
            in_memory_offices = dojo.offices
            for _, in_memory_office in in_memory_offices.items():
                db_office = DBOffice(in_memory_office.name, in_memory_office.spaces)
                session.add(db_office)

    @staticmethod
    def load(dojo):
        session = dojo.session

        with session.no_autoflush:
            db_offices = session.query(DBOffice).all()
            for db_office in db_offices:
                office = Office(db_office.name)
                office.spaces = db_office.spaces
                dojo.offices[db_office.name] = office
        return dojo


class Livingspace(Room):
    SPACE = 4

    def __init__(self, name):
        super(self.__class__, self).__init__(name, self.SPACE)

    def assign_fellow_space(self, fellow):
        fellow.livingspace = self
        self.spaces -= 1
        return fellow

    def print_occupants(self, occupants):
        print self.name.upper()
        print "--------------------------"
        print ", ".join([occupant.name.upper() for occupant in self.get_occupants(occupants)])

    def get_occupants(self, occupants):
        return [occupant for occupant in occupants if
                occupant.wants_accommodation() and occupant.livingspace.name == self.name]

    @staticmethod
    def create_from_db_object(db_livingspace):
        if db_livingspace:
            livingspace = Office(db_livingspace.name)
            livingspace.spaces = db_livingspace.spaces
            return livingspace
        return None

    @staticmethod
    def save(dojo):
        session = dojo.session
        with session.no_autoflush:
            in_memory_livingspaces = dojo.livingspaces
            for _, in_memory_livingspace in in_memory_livingspaces.items():
                db_livingspace = DBLivingspace(in_memory_livingspace.name, in_memory_livingspace.spaces)
                session.add(db_livingspace)

    @staticmethod
    def load(dojo):
        session = dojo.session

        with session.no_autoflush:
            db_livingspaces = session.query(DBLivingspace).all()
            for db_livingspace in db_livingspaces:
                livingspace = Office(db_livingspace.name)
                livingspace.spaces = db_livingspace.spaces
                dojo.livingspaces[db_livingspace.name] = livingspace
        return dojo
