import unittest

from app.models.person import Person


class TestPerson(unittest.TestCase):
    def test_person_should_not_create_an_instance_of_person(self):
        name = 'Person Name'
        office = None
        self.assertRaises(NotImplementedError, Person, name, office)
