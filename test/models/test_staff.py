import unittest
from app.models.person import Staff
from app.models.dojo import Dojo
from mock import MagicMock
from app.db.models import Staff as DBStaff, Office as DBOffice
from app.models.room import Office


class TestStaff(unittest.TestCase):
    def setUp(self):
        self.staff = Staff('Staff Name')
        self.db_staff = DBStaff('Staff Name')

        self.db_office = DBOffice('Office1', 5)
        self.db_staff.office = self.db_office

        self.office = Office('Office1')
        self.office.spaces = 5

        self.dojo = Dojo('Andela', 'Nairobi')
        self.dojo.staff.append(self.staff)

        self.dojo.session = MagicMock()

    def test_fellow_responds_properties(self):
        self.assertEqual(self.staff.name, 'Staff Name')

    def test_should_add_a_new_staff_to_database_session(self):
        Staff.save(self.dojo)
        self.dojo.session.add.assert_called_with(self.db_staff)

    def test_should_load_staff_from_database(self):
        self.dojo.session.query(DBStaff).all = MagicMock(return_value=[self.db_staff])
        self.dojo.session.query(DBOffice).filter_by = MagicMock(return_value=self.db_office)
        self.dojo.staff = []

        Staff.load(self.dojo)
        self.assertListEqual(self.dojo.staff, [self.staff])
        self.assertEqual(self.dojo.staff[0].office, self.office)

    def test_get_db_office_object_from_database(self):
        self.staff.get_office_from_db(self.dojo.session, self.office)
        self.dojo.session.query(DBOffice).filter_by.assert_called_with(name=self.office.name)

