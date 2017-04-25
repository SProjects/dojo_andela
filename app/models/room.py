class Room(object):
    def __init__(self, name, space):
        self.name = name
        self.spaces = space

    def __eq__(self, other):
        return self.name == other.name

    def add_person(self, person):
        person.office = self
        self.spaces -= 1
        return person

    def has_space(self):
        return self.spaces != 0


class Office(Room):
    SPACES = 6

    def __init__(self, name):
        super(self.__class__, self).__init__(name, self.SPACES)


class Livingspace(Room):
    SPACE = 4

    def __init__(self, name):
        super(self.__class__, self).__init__(name, self.SPACE)