from app.db.models import Fellow as DBFellow, Staff as DBStaff
from app.db.models import Office as DBOffice, Livingspace as DBLivingspace
from app.models.room import Office, Livingspace


class Person(object):
    def __init__(self, name, office):
        if type(self) == Person:
            raise NotImplementedError("Can't directly create an instance of person.")

        self.name = name
        self.office = office
        self.saved = False

    def __repr__(self):
        return "{}".format(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def is_saved(self):
        return self.saved

    def get_office_from_db(self, session, office):
        with session.no_autoflush:
            return session.query(DBOffice).filter_by(name=office.name).first()


class Fellow(Person):
    def __init__(self, name, accommodation):
        super(self.__class__, self).__init__(name, None)
        self.accommodation = accommodation
        self.livingspace = None

    def wants_accommodation(self):
        return self.accommodation == 'Y'

    def get_livingspace_from_db(self, session, livingspace):
        with session.no_autoflush:
            return session.query(DBLivingspace).filter_by(name=livingspace.name).first()

    @staticmethod
    def save(session, in_memory_fellows):
        with session.no_autoflush:
            for in_memory_fellow in in_memory_fellows:
                in_memory_office = in_memory_fellow.office
                in_memory_livingspace = in_memory_fellow.livingspace

                office = in_memory_fellow.get_office_from_db(session, in_memory_office) if in_memory_office else None
                livingspace = in_memory_fellow. \
                    get_livingspace_from_db(session, in_memory_livingspace) if in_memory_livingspace else None

                db_fellow = DBFellow(in_memory_fellow.name, in_memory_fellow.accommodation)\
                    if not in_memory_fellow.is_saved() \
                    else session.query(DBFellow).filter_by(name=in_memory_fellow.name).first()

                db_fellow.office = office
                db_fellow.livingspace = livingspace
                session.add(db_fellow)
            print "Saved {} fellows.".format(len(in_memory_fellows))

    @staticmethod
    def load(session):
        fellows = []
        with session.no_autoflush:
            db_fellows = session.query(DBFellow).all()
            for db_fellow in db_fellows:
                fellow = Fellow(db_fellow.name, db_fellow.accommodation)
                office = Office.create_from_db_object(db_fellow.office)
                livingspace = Livingspace.create_from_db_object(db_fellow.livingspace)

                fellow.office = office
                fellow.saved = True
                fellow.livingspace = livingspace

                fellows.append(fellow)
            print "{} fellows loaded".format(len(fellows))
        return fellows


class Staff(Person):
    def __init__(self, name):
        super(Staff, self).__init__(name, None)

    @staticmethod
    def save(session, in_memory_staffs):
        with session.no_autoflush:
            for in_memory_staff in in_memory_staffs:
                in_memory_office = in_memory_staff.office
                office = in_memory_staff.get_office_from_db(session, in_memory_office) if in_memory_office else None

                db_staff = DBStaff(in_memory_staff.name) if not in_memory_staff.is_saved() \
                    else session.query(DBStaff).filter_by(name=in_memory_staff.name).first()

                db_staff.office = office
                session.add(db_staff)
            print "Saved {} staff.".format(len(in_memory_staffs))

    @staticmethod
    def load(session):
        all_staff = []
        with session.no_autoflush:
            db_staff = session.query(DBStaff).all()
            for db_staff in db_staff:
                staff = Staff(db_staff.name)
                office = Office.create_from_db_object(db_staff.office)
                staff.office = office
                staff.saved = True

                all_staff.append(staff)
            print "{} staff loaded.".format(len(all_staff))
        return all_staff
