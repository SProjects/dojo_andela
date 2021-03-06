from app.db.models import Office as DBOffice, Livingspace as DBLivingspace


class Room(object):
    def __init__(self, name, space):
        if type(self) == Room:
            raise NotImplementedError("Can't directly create an instance of room.")

        self.name = name
        self.spaces = space

    def __repr__(self):
        return "{}".format(self.name)

    def __eq__(self, other):
        return self.name == other.name and self.spaces == other.spaces

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
        print ", ".join([occupant.name.upper() + "[{}]".format(occupant.__class__.__name__[0]) for occupant in
                         self.get_occupants(occupants)])
        print

    def get_occupants(self, occupants):
        return [occupant for occupant in occupants if occupant.office and occupant.office.name == self.name]


class Office(Room):
    SPACES = 6

    def __init__(self, name):
        super(self.__class__, self).__init__(name, self.SPACES)

    @staticmethod
    def create_from_db_object(db_office):
        if db_office:
            office = Office(db_office.name)
            office.spaces = Office.SPACES - len(db_office.fellows + db_office.staff)
            office.saved = True
            return office
        return None

    @staticmethod
    def save(session, offices, full_offices):
        with session.no_autoflush:
            in_memory_offices = dict(list(offices.items()) + list(full_offices.items()))
            for _, in_memory_office in in_memory_offices.items():
                db_office = session.query(DBOffice).filter_by(name=in_memory_office.name).first()
                if db_office is None:
                    db_office = DBOffice(in_memory_office.name, in_memory_office.spaces)

                db_office.spaces = in_memory_office.spaces
                session.add(db_office)
            print "Saved {} offices.".format(len(in_memory_offices))

    @staticmethod
    def load(session):
        offices, full_offices = {}, {}
        with session.no_autoflush:
            db_offices = session.query(DBOffice).all()
            for db_office in db_offices:
                office = Office.create_from_db_object(db_office)
                if office.spaces != 0:
                    offices[office.name] = office
                else:
                    full_offices[office.name] = office
            print "{} offices loaded".format(len(db_offices))
        return offices, full_offices


class Livingspace(Room):
    SPACE = 4

    def __init__(self, name):
        super(self.__class__, self).__init__(name, self.SPACE)

    def get_occupants(self, occupants):
        return [occupant for occupant in occupants if occupant.livingspace and
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
            livingspace.spaces = Livingspace.SPACE - len(db_livingspace.fellows)
            livingspace.saved = True
            return livingspace
        return None

    @staticmethod
    def save(session, livingspaces, full_livingspaces):
        with session.no_autoflush:
            in_memory_livingspaces = dict(list(livingspaces.items()) + list(full_livingspaces.items()))
            for _, in_memory_livingspace in in_memory_livingspaces.items():
                db_livingspace = session.query(DBLivingspace).filter_by(name=in_memory_livingspace.name).first()
                if db_livingspace is None:
                    db_livingspace = DBLivingspace(in_memory_livingspace.name, in_memory_livingspace.spaces)

                db_livingspace.spaces = in_memory_livingspace.spaces
                session.add(db_livingspace)
            print "Saved {} livingspaces".format(len(in_memory_livingspaces))

    @staticmethod
    def load(session):
        livingspaces, full_livingspaces = {}, {}
        with session.no_autoflush:
            db_livingspaces = session.query(DBLivingspace).all()
            for db_livingspace in db_livingspaces:
                livingspace = Livingspace.create_from_db_object(db_livingspace)
                if livingspace.spaces != 0:
                    livingspaces[livingspace.name] = livingspace
                else:
                    full_livingspaces[livingspace.name] = livingspace
            print "{} livingspaces loaded".format(len(db_livingspaces))
        return livingspaces, full_livingspaces
