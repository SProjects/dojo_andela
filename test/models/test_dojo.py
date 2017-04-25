import unittest
from app.models.dojo import Dojo
from app.models.room import Office, Livingspace
from app.models.person import Fellow, Staff


class TestDojo(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo('Andela Dojo', 'Nairobi')
        self.office_room_type = 'OFFICE'
        self.livingspace_room_type = 'LIVINGSPACE'
        self.fellow_type = 'FELLOW'
        self.no_livingspace = 'N'
        self.yes_livingspace = 'Y'
        self.staff_type = 'STAFF'

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

    def test_create_room_raises_value_error_when_non_list_argument_is_passed(self):
        self.assertRaises(ValueError, self.dojo.create_room, 'livingspace_name', self.livingspace_room_type)

    def test_create_room_raises_type_error_when_wrong_number_of_parameters_is_received(self):
        self.assertRaises(TypeError, self.dojo.create_room, ['livingspace_name'])

    def test_add_person_adds_new_fellow_to_dojo(self):
        self.dojo.add_person('Fellow Name', self.fellow_type, self.no_livingspace)
        self.assertEqual(self.dojo.fellows, [Fellow('Fellow Name', self.no_livingspace)])

    def test_add_person_adds_new_staff_to_dojo(self):
        self.dojo.add_person('Staff Name', self.staff_type, self.no_livingspace)
        self.assertEqual(self.dojo.staff, [Staff('Staff Name')])

    def test_add_person_raises_values_error_when_none_string_name_parameter_is_passed(self):
        self.assertRaises(ValueError, self.dojo.add_person, 123, self.fellow_type, self.no_livingspace)

    def test_add_person_raises_type_error_when_wrong_number_of_arguments_are_passed(self):
        self.assertRaises(TypeError, self.dojo.add_person, 123, self.fellow_type)

