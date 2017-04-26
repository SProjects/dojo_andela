import unittest
import sys, re
from cStringIO import StringIO
from app.models.dojo import Dojo
from app.models.room import Office, Livingspace
from app.models.person import Fellow, Staff

"""Citation:
    Link: http://code.activestate.com/lists/python-list/366576/
    By: Miki Tebeka
"""


def with_io_divert(func):
    """Divert stdout"""
    orig = sys.stdout
    io = StringIO()
    sys.stdout = io
    try:
        func(io)
    finally:
        sys.stdout = orig
        io_clear(io)


def io_clear(io):
    """Clear io"""
    io.seek(0)
    io.truncate()


def io_value(io):
    """Value in io"""
    return io.getvalue().strip()

"""End citation"""


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

    def test_when_person_is_created_is_assigned_office_in_dojo(self):
        self.dojo.create_room(['office1'], self.office_room_type)
        office1 = self.dojo.offices[0]

        self.dojo.add_person('Fellow Name', self.fellow_type, self.no_livingspace)
        self.dojo.add_person('Staff Name', self.staff_type, self.no_livingspace)

        self.assertListEqual([self.dojo.staff[0].office, self.dojo.fellows[0].office], [office1, office1])
        self.assertEqual(4, office1.spaces)

    def test_person_is_not_assigned_office_if_no_office_has_been_created(self):
        self.dojo.add_person('Fellow Name', self.fellow_type, self.no_livingspace)
        self.assertEqual(self.dojo.fellows[0].office, None)

    def test_fellow_is_assigned_a_livingspace_if_he_wants_one(self):
        self.dojo.create_room(['livingspace1'], self.livingspace_room_type)
        livingspace1 = self.dojo.livingspaces[0]

        self.dojo.add_person('Fellow Name', self.fellow_type, self.yes_livingspace)
        self.assertEqual(self.dojo.fellows[0].livingspace, livingspace1)
        self.assertEqual(3, livingspace1.spaces)

    def test_fellow_is_not_assigned_a_livingspace_if_no_livingspace_room_is_created(self):
        self.dojo.add_person('Fellow Name', self.fellow_type, self.yes_livingspace)
        self.assertEqual(self.dojo.fellows[0].livingspace, None)

    def test_print_people_in_room_prints_people_assigned_to_a_room(self):
        def func(io):
            self.dojo.create_room(['livingspace1'], self.livingspace_room_type)
            livingspace = self.dojo.livingspaces[0]

            self.dojo.add_person('Fellow Name', self.fellow_type, self.yes_livingspace)
            fellow = self.dojo.fellows[0]

            self.dojo.print_people_in_room('livingspace1')

            self.assertIn(fellow.name.upper(), io_value(io))
            self.assertIn(livingspace.name.upper(), io_value(io))
        with_io_divert(func)

    def test_print_allocated_people_prints_people_that_have_been_assigned_rooms(self):
        def func(io):
            self.dojo.create_room(['livingspace1'], self.livingspace_room_type)
            livingspace = self.dojo.livingspaces[0]

            self.dojo.create_room(['office1'], self.office_room_type)
            office = self.dojo.offices[0]

            self.dojo.add_person('Fellow Name', self.fellow_type, self.yes_livingspace)
            fellow = self.dojo.fellows[0]

            self.dojo.print_allocated_people()

            self.assertIn(fellow.name.upper(), io_value(io))
            self.assertIn(livingspace.name.upper(), io_value(io))
            self.assertIn(office.name.upper(), io_value(io))
        with_io_divert(func)

    def test_print_unallocated_people_prints_people_who_have_not_been_assigned_one_or_all_rooms(self):
        def func(io):
            self.dojo.add_person('Fellow Name', self.fellow_type, self.yes_livingspace)
            fellow = self.dojo.fellows[0]

            self.dojo.print_unallocated_people()

            self.assertIn(fellow.name.upper(), io_value(io))
        with_io_divert(func)
