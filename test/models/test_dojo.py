import unittest
import sys
from cStringIO import StringIO
from mock import mock_open, patch
from app.models.dojo import Dojo
from app.models.room import Office, Livingspace
from app.models.person import Fellow, Staff
from app.errors.dojo_errors import StaffCantBeAssignedToLivingspace

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
        self.ROOT_DIR = Dojo.ROOT_DIR

    def test_dojo_responds_to_its_properties(self):
        self.assertListEqual([self.dojo.name, self.dojo.location], ['Andela Dojo', 'Nairobi'])

    def test_create_room_adds_new_office_to_dojo(self):
        office_name = 'office_name'
        self.dojo.create_room([office_name], self.office_room_type)
        self.assertEqual(self.dojo.offices[office_name], Office(office_name))

    def test_create_room_adds_multiple_offices_to_dojo(self):
        office1 = 'office1'
        office2 = 'office2'
        self.dojo.create_room([office1, office2], self.office_room_type)
        self.assertDictEqual(self.dojo.offices, {office1: Office(office1), office2: Office(office2)})

    def test_create_room_adds_new_living_space_to_dojo(self):
        livingspace_name = 'livingspace_name'
        self.dojo.create_room([livingspace_name], self.livingspace_room_type)
        self.assertEqual(self.dojo.livingspaces[livingspace_name], Livingspace(livingspace_name))

    def test_create_room_adds_multiple_living_spaces_to_dojo(self):
        livingspace1 = 'livingspace1'
        livingspace2 = 'livingspace2'
        self.dojo.create_room([livingspace1, livingspace2], self.livingspace_room_type)

        actual_dictionary = {livingspace1: Livingspace(livingspace1), livingspace2: Livingspace(livingspace2)}
        self.assertDictEqual(self.dojo.livingspaces, actual_dictionary)

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
        office_name = 'office1'
        self.dojo.create_room([office_name], self.office_room_type)
        office1 = self.dojo.offices[office_name]

        self.dojo.add_person('Fellow Name', self.fellow_type, self.no_livingspace)
        self.dojo.add_person('Staff Name', self.staff_type, self.no_livingspace)

        self.assertListEqual([self.dojo.staff[0].office, self.dojo.fellows[0].office], [office1, office1])
        self.assertEqual(4, office1.spaces)

    def test_person_is_not_assigned_office_if_no_office_has_been_created(self):
        self.dojo.add_person('Fellow Name', self.fellow_type, self.no_livingspace)
        self.assertEqual(self.dojo.fellows[0].office, None)

    def test_fellow_is_assigned_a_livingspace_if_he_wants_one(self):
        livingspace1 = 'livingspace1'
        self.dojo.create_room([livingspace1], self.livingspace_room_type)
        livingspace1 = self.dojo.livingspaces[livingspace1]

        self.dojo.add_person('Fellow Name', self.fellow_type, self.yes_livingspace)
        self.assertEqual(self.dojo.fellows[0].livingspace, livingspace1)
        self.assertEqual(3, livingspace1.spaces)

    def test_fellow_is_not_assigned_a_livingspace_if_no_livingspace_room_is_created(self):
        self.dojo.add_person('Fellow Name', self.fellow_type, self.yes_livingspace)
        self.assertEqual(self.dojo.fellows[0].livingspace, None)

    def test_print_people_in_room_prints_people_assigned_to_a_room(self):
        def func(io):
            livingspace1 = 'livingspace1'
            self.dojo.create_room([livingspace1], self.livingspace_room_type)
            livingspace = self.dojo.livingspaces[livingspace1]

            self.dojo.add_person('Fellow Name', self.fellow_type, self.yes_livingspace)
            fellow = self.dojo.fellows[0]

            self.dojo.print_people_in_room(livingspace1)

            self.assertIn(fellow.name.upper(), io_value(io))
            self.assertIn(livingspace.name.upper(), io_value(io))

        with_io_divert(func)

    def test_print_allocated_people_prints_people_that_have_been_assigned_rooms(self):
        def func(io):
            livingspace1 = 'livingspace1'
            self.dojo.create_room([livingspace1], self.livingspace_room_type)
            livingspace = self.dojo.livingspaces[livingspace1]

            office1 = 'office1'
            self.dojo.create_room([office1], self.office_room_type)
            office = self.dojo.offices[office1]

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

    @patch('__builtin__.open', new_callable=mock_open, create=True)
    def test_print_allocated_people_to_file_prints_text_file_with_allocated_people(self, fake_open):
        livingspace1 = 'livingspace1'
        self.dojo.create_room([livingspace1], self.livingspace_room_type)
        livingspace = self.dojo.livingspaces[livingspace1]

        office1 = 'office1'
        self.dojo.create_room([office1], self.office_room_type)
        office = self.dojo.offices[office1]

        self.dojo.add_person('Fellow Name', self.fellow_type, self.yes_livingspace)
        fellow = self.dojo.fellows[0]

        self.dojo.add_person('Staff Name', self.staff_type, self.no_livingspace)
        staff = self.dojo.staff[0]

        filename = 'output.txt'
        file_path = self.ROOT_DIR + '/../../files/output.txt'
        expected_output = '{}\n------------------------\n{}\n\n'.format(livingspace.name.upper(), fellow.name.upper())
        expected_output += '{}\n------------------------\n{}, {}\n\n'.format(office.name.upper(), staff.name.upper(),
                                                                             fellow.name.upper())

        self.dojo.print_allocated_people_to_file(filename)

        fake_open.assert_called_once_with(file_path, 'w')
        mock_output_file_handle = fake_open()
        mock_output_file_handle.write.assert_called_with(expected_output)

    @patch('__builtin__.open', new_callable=mock_open, create=True)
    def test_print_unallocated_people_to_file_prints_text_file_unallocated_people(self, fake_open):
        self.dojo.add_person('Fellow Name', self.fellow_type, self.yes_livingspace)
        fellow = self.dojo.fellows[0]

        self.dojo.add_person('Staff Name', self.staff_type, self.no_livingspace)
        staff = self.dojo.staff[0]

        filename = 'output.txt'
        file_path = self.ROOT_DIR + '/../../files/output.txt'
        expected_output = 'UNALLOCATED FELLOWS\n------------------------\n{}\n\n'.format(fellow.name.upper())
        expected_output += 'UNALLOCATED STAFF\n------------------------\n{}\n\n'.format(staff.name.upper())

        self.dojo.print_unallocated_people_to_file(filename)
        fake_open.assert_called_once_with(file_path, 'w')
        mock_output_file_handle = fake_open()
        mock_output_file_handle.write.assert_called_with(expected_output)

    @patch('__builtin__.open', new_callable=mock_open, read_data='FELLOW NAME FELLOW Y', create=True)
    def test_add_people_from_file_add_new_people_from_a_formatted_input_text_file(self, fake_open):
        filename = 'input.txt'
        file_path = self.ROOT_DIR + '/../../files/'+filename
        fellow = Fellow('FELLOW NAME', self.yes_livingspace)

        self.dojo.add_people_from_file()

        fake_open.assert_called_once_with(file_path, 'r')
        mock_output_file_handle = fake_open()
        mock_output_file_handle.readlines.assert_called_with()
        self.assertListEqual(self.dojo.fellows, [fellow])

    def test_reallocate_person_changes_fellow_to_another_office(self):
        office1_name = 'office1'
        office2_name = 'office2'
        self.dojo.create_room([office1_name], self.office_room_type)
        office1 = self.dojo.offices[office1_name]

        fellow_name = "Fellow Name"
        self.dojo.add_person(fellow_name, self.fellow_type, self.yes_livingspace)

        self.dojo.create_room([office2_name], self.office_room_type)
        office2 = self.dojo.offices[office2_name]

        self.dojo.reallocate_person(fellow_name, office2_name)

        self.assertNotEqual(self.dojo.fellows[0].office, office1)
        self.assertEqual(self.dojo.fellows[0].office, office2)

    def test_reallocate_person_changes_fellow_to_another_living_space(self):
        livingspace1_name = 'livingspace1'
        livingspace2_name = 'livingspace2'
        self.dojo.create_room([livingspace1_name], self.livingspace_room_type)
        livingspace1 = self.dojo.livingspaces[livingspace1_name]

        fellow_name = "Fellow Name"
        self.dojo.add_person(fellow_name, self.fellow_type, self.yes_livingspace)

        self.dojo.create_room([livingspace2_name], self.livingspace_room_type)
        livingspace2 = self.dojo.livingspaces[livingspace2_name]

        self.dojo.reallocate_person(fellow_name, livingspace2_name)

        self.assertNotEqual(self.dojo.fellows[0].livingspace, livingspace1)
        self.assertEqual(self.dojo.fellows[0].livingspace, livingspace2)

    def test_reallocate_person_changes_staff_to_another_office(self):
        office1_name = 'office1'
        office2_name = 'office2'
        self.dojo.create_room([office1_name], self.office_room_type)
        office1 = self.dojo.offices[office1_name]

        staff_name = "Staff Name"
        self.dojo.add_person(staff_name, self.staff_type, self.no_livingspace)

        self.dojo.create_room([office2_name], self.office_room_type)
        office2 = self.dojo.offices[office2_name]

        self.dojo.reallocate_person(staff_name, office2_name)

        self.assertNotEqual(self.dojo.staff[0].office, office1)
        self.assertEqual(self.dojo.staff[0].office, office2)

    def test_reallocate_person_raises_error_when_there_is_attempt_to_reassign_staff_to_livingspace(self):
        livingspace1_name = 'livingspace1'
        self.dojo.create_room([livingspace1_name], self.livingspace_room_type)

        staff_name = "Staff Name"
        self.dojo.add_person(staff_name, self.staff_type, self.no_livingspace)

        self.assertRaises(StaffCantBeAssignedToLivingspace, self.dojo.reallocate_person, staff_name, livingspace1_name)


