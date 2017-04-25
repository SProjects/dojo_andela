class Person(object):
    def __init__(self, name, office):
        self.name = name
        self.office = office

    def __eq__(self, other):
        return self.name == other.name


class Fellow(Person):
    def __init__(self, name, want_livingspace):
        super(self.__class__, self).__init__(name, None)
        self.want_livingspace = want_livingspace
        self.livingspace = None

    def wants_accommodation(self):
        return self.want_livingspace == 'Y'


class Staff(Person):
    def __init__(self, name):
        super(Staff, self).__init__(name, None)

