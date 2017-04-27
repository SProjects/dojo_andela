from sqlalchemy.orm import sessionmaker
from app.db.models import Fellow as DBFellow, Staff as DBStaff, engine
from app.db.models import Office as DBOffice, Livingspace as DBLivingspace


class Person(object):
    def __init__(self, name, office):
        self.name = name
        self.office = office

    def __eq__(self, other):
        return self.name == other.name

    def get_office_from_db(self, session, office):
        with session.no_autoflush:
            return session.query(DBOffice).filter_by(name=office.name).first()

    def get_livingspace_from_db(self, session, livingspace):
        with session.no_autoflush:
            return session.query(DBLivingspace).filter_by(name=livingspace.name).first()


class Fellow(Person):
    def __init__(self, name, accommodation):
        super(self.__class__, self).__init__(name, None)
        self.accommodation = accommodation
        self.livingspace = None

    def wants_accommodation(self):
        return self.accommodation == 'Y'

    @staticmethod
    def save(dojo):
        session = dojo.session
        with session.no_autoflush:
            in_memory_fellows = dojo.fellows
            for in_memory_fellow in in_memory_fellows:
                in_memory_office = in_memory_fellow.office
                in_memory_livingspace = in_memory_fellow.livingspace

                office = in_memory_fellow.get_office_from_db(session, in_memory_office) if in_memory_office else None
                livingspace = in_memory_fellow.\
                    get_livingspace_from_db(session,in_memory_livingspace) if in_memory_livingspace else None

                db_fellow = DBFellow(in_memory_fellow.name, in_memory_fellow.accommodation)
                db_fellow.office = office
                db_fellow.livingspace = livingspace
                session.add(db_fellow)


class Staff(Person):
    def __init__(self, name):
        super(Staff, self).__init__(name, None)

    @staticmethod
    def save(dojo):
        session = dojo.session
        with session.no_autoflush:
            in_memory_staff = dojo.staff
            for in_memory_staff in in_memory_staff:
                in_memory_office = in_memory_staff.office
                office = in_memory_staff.get_office_from_db(session, in_memory_office) if in_memory_office else None

                db_staff = DBStaff(in_memory_staff.name)
                db_staff.office = office
                session.add(db_staff)
