class Person(object):
    def __init__(self, name, office):
        self.name = name
        self.office = office

    def __eq__(self, other):
        return self.name == other.name


class Fellow(Person):
    def __init__(self, name, accommodation):
        super(self.__class__, self).__init__(name, None)
        self.accommodation = accommodation
        self.livingspace = None

    def wants_accommodation(self):
        return self.accommodation == 'Y'


class Staff(Person):
    def __init__(self, name):
        super(Staff, self).__init__(name, None)

