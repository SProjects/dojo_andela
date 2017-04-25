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
        print ", ".join([occupant.name.upper() for occupant in occupants if occupant.office.name == self.name])


class Office(Room):
    SPACES = 6

    def __init__(self, name):
        super(self.__class__, self).__init__(name, self.SPACES)


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
        print ", ".join([occupant.name.upper() for occupant in occupants if
                         occupant.wants_accommodation() and occupant.livingspace.name == self.name])
