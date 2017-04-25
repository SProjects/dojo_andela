class Person(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


class Fellow(Person):
    def __init__(self, name, want_livingspace):
        super(self.__class__, self).__init__(name)
        self.want_livingspace = want_livingspace


class Staff(Person):
    def __init__(self, name):
        super(Staff, self).__init__(name)

