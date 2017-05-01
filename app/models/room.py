from app.db.models import Office as DBOffice, Livingspace as DBLivingspace


class Room(object):
    def __init__(self, name, space):
        self.name = name
        self.spaces = space
        self.saved = False

    def __eq__(self, other):
        return self.name == other.name

    def is_saved(self):
        return self.saved

    def assign_person_space(self, person):
        person.office = self
        self.spaces -= 1
        print "{} has been allocated the office {}".format(person.name, self.name)
        return person

    def has_space(self):
        return self.spaces != 0

    def print_occupants(self, occupants):
        print self.name.upper()
        print "--------------------------"
        print ", ".join([occupant.name.upper() for occupant in self.get_occupants(occupants)])
        print

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
            in_memory_offices = dict(list(dojo.offices.items()) + list(dojo.full_offices.items()))
            for _, in_memory_office in in_memory_offices.items():
                db_office = DBOffice(in_memory_office.name, in_memory_office.spaces) \
                    if not in_memory_office.is_saved() else \
                    session.query(DBOffice).filter_by(name=in_memory_office.name).first()
                db_office.spaces = in_memory_office.spaces

                session.add(db_office)
            print "Saved {} offices.".format(len(in_memory_offices))

    @staticmethod
    def load(dojo):
        session = dojo.session
        with session.no_autoflush:
            db_offices = session.query(DBOffice).all()
            for db_office in db_offices:
                office = Office(db_office.name)
                office.spaces = Office.SPACES - len(db_office.fellows + db_office.staff)
                office.saved = True
                if office.spaces != 0:
                    dojo.offices[office.name] = office
                else:
                    dojo.full_offices[office.name] = office
            print "{} offices loaded".format(len(db_offices))
        return dojo


class Livingspace(Room):
    SPACE = 4

    def __init__(self, name):
        super(self.__class__, self).__init__(name, self.SPACE)

    def get_occupants(self, occupants):
        return [occupant for occupant in occupants if
                occupant.wants_accommodation() and occupant.livingspace.name == self.name]

    def assign_fellow_space(self, fellow):
        fellow.livingspace = self
        self.spaces -= 1
        print "{} has been allocated the livingspace {}".format(fellow.name, self.name)
        return fellow

    @staticmethod
    def create_from_db_object(db_livingspace):
        if db_livingspace:
            livingspace = Livingspace(db_livingspace.name)
            livingspace.spaces = db_livingspace.spaces
            return livingspace
        return None

    @staticmethod
    def save(dojo):
        session = dojo.session
        with session.no_autoflush:
            in_memory_livingspaces = dict(list(dojo.livingspaces.items()) + list(dojo.full_livingspaces.items()))
            for _, in_memory_livingspace in in_memory_livingspaces.items():
                db_livingspace = DBLivingspace(in_memory_livingspace.name, in_memory_livingspace.spaces) \
                    if not in_memory_livingspace.is_saved() else \
                    session.query(DBLivingspace).filter_by(name=in_memory_livingspace.name).first()
                db_livingspace.spaces = in_memory_livingspace.spaces

                session.add(db_livingspace)
            print "Saved {} livingspaces".format(len(in_memory_livingspaces))

    @staticmethod
    def load(dojo):
        session = dojo.session
        with session.no_autoflush:
            db_livingspaces = session.query(DBLivingspace).all()
            for db_livingspace in db_livingspaces:
                livingspace = Livingspace(db_livingspace.name)
                livingspace.spaces = Livingspace.SPACE - len(db_livingspace.fellows)
                livingspace.saved = True
                if livingspace.spaces != 0:
                    dojo.livingspaces[livingspace.name] = livingspace
                else:
                    dojo.full_livingspaces[livingspace.name] = livingspace
            print "{} livingspaces loaded".format(len(db_livingspaces))
        return dojo
