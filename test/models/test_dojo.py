import unittest
from app.models.dojo import Dojo
from app.models.room import Office, Livingspace


class TestDojo(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo('Andela Dojo', 'Nairobi')
        self.office_room_type = 'OFFICE'
        self.livingspace_room_type = 'LIVINGSPACE'

    def test_dojo_responds_to_its_properties(self):
        self.assertListEqual([self.dojo.name, self.dojo.location], ['Andela Dojo', 'Nairobi'])

    def test_create_room_adds_new_office_to_dojo(self):
        self.dojo.create_room(['office_name'], self.office_room_type)
        self.assertEqual(self.dojo.offices, [Office('office_name')])

    def test_create_room_adds_multiple_offices_to_dojo(self):
        self.dojo.create_room(['office1', 'office2'], self.office_room_type)
        self.assertListEqual(self.dojo.offices, [Office('office1'), Office('office2')])

    def test_create_room_adds_new_living_space_to_dojo(self):
        self.dojo.create_room(['livingspace_name'], self.livingspace_room_type)
        self.assertEqual(self.dojo.livingspaces, [Livingspace('livingspace_name')])

    def test_create_room_adds_multiple_living_spaces_to_dojo(self):
        self.dojo.create_room(['livingspace1', 'livingspace2'], self.livingspace_room_type)
        self.assertListEqual(self.dojo.livingspaces, [Livingspace('livingspace1'), Livingspace('livingspace2')])