import unittest
from app.models.room import Office
from app.models.dojo import Dojo


class TestOffice(unittest.TestCase):
    def setUp(self):
        self.office = Office('office1')
        self.dojo = Dojo('Andela', 'Nairobi')
        self.office_room_type = 'OFFICE'
        self.database = 'test_andela_dojo.db'

    def test_office_responds_to_properties(self):
        self.assertListEqual([self.office.name, self.office.spaces], ['office1', 6])

