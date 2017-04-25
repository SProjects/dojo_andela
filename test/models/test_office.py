import unittest
from app.models.room import Office


class TestOffice(unittest.TestCase):
    def setUp(self):
        self.office = Office('office1')

    def test_office_responds_to_properties(self):
        self.assertEqual(self.office.name, 'office1')