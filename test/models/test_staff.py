from mock import MagicMock

import unittest

from app.models.person import Staff
from app.models.room import Office
from app.db.models import Staff as DBStaff, Office as DBOffice


class TestStaff(unittest.TestCase):
    def setUp(self):
        self.staff = Staff('Staff Name')
        self.db_staff = DBStaff('Staff Name')

        self.db_office = DBOffice('Office1', 5)
        self.db_staff.office = self.db_office

        self.office = Office('Office1')
        self.office.spaces = 5

        self.all_staff = [self.staff]
        self.session = MagicMock()

    def test_staff_responds_properties(self):
        self.assertEqual(self.staff.name, 'Staff Name')

    def test_repr_returns_staff_name(self):
        self.assertEqual(self.staff.__repr__(), 'Staff Name')

    def test_should_add_a_new_staff_to_database_session(self):
        self.session.query(DBStaff).filter_by(name=self.staff.name).first = MagicMock(return_value=None)

        Staff.save(self.session, self.all_staff)
        self.session.add.assert_called_with(self.db_staff)

    def test_should_load_staff_from_database(self):
        self.session.query(DBStaff).all = MagicMock(return_value=[self.db_staff])
        self.session.query(DBOffice).filter_by = MagicMock(return_value=self.db_office)

        result_staff = Staff.load(self.session)
        self.assertListEqual(result_staff, [self.staff])
        self.assertEqual(result_staff[0].office, self.office)

    def test_get_db_office_object_from_database(self):
        self.staff.get_office_from_db(self.session, self.office)
        self.session.query(DBOffice).filter_by.assert_called_with(name=self.office.name)

