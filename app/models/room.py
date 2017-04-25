class Room(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


class Office(Room):
    def __init__(self, name):
        super(self.__class__, self).__init__(name)


class Livingspace(Room):
    def __init__(self, name):
        super(self.__class__, self).__init__(name)