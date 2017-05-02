import unittest
from app.models.room import Office
from mock import MagicMock
from app.db.models import Office as DBOffice, Fellow as DBFellow


class TestOffice(unittest.TestCase):
    def setUp(self):
        office_name = 'office1'
        self.office = Office(office_name)
        self.offices = {office_name: self.office}
        self.full_offices = {}

        self.db_office = DBOffice(office_name, 6)
        self.session = MagicMock()

    def test_office_responds_to_properties(self):
        self.assertListEqual([self.office.name, self.office.spaces], ['office1', 6])

    def test_save_should_add_office_to_session(self):
        Office.save(self.session, self.offices, self.full_offices)
        self.session.add.assert_called_with(self.db_office)

    def test_should_load_office_from_database(self):
        self.session.query(DBOffice).all = MagicMock(return_value=[self.db_office])
        self.offices = {}

        offices, full_offices = Office.load(self.session)
        self.assertEqual(offices['office1'], self.office)
        self.assertEqual(full_offices, {})

    def test_load_adds_full_db_offices_to_the_full_offices_list(self):
        self.full_offices = {}

        self.full_office = Office('office1')
        self.full_office.spaces = 0

        self.db_office = DBOffice('office1', 0)
        self.db_office.fellows = [DBFellow('Fellow1', 'Y'), DBFellow('Fellow1', 'Y'),
                                  DBFellow('Fellow1', 'Y'), DBFellow('Fellow1', 'Y'),
                                  DBFellow('Fellow1', 'Y'), DBFellow('Fellow1', 'Y')]
        self.session.query(DBOffice).all = MagicMock(return_value=[self.db_office])

        offices, full_offices = Office.load(self.session)
        self.assertEqual(full_offices['office1'], self.full_office)
        self.assertEqual(offices, {})

    def test_create_from_db_object_creates_office_from_db_office(self):
        result = Office.create_from_db_object(self.db_office)
        self.assertEqual(result, self.office)

    def test_create_from_db_object_returns_none_if_no_db_office_was_passed(self):
        result = Office.create_from_db_object(None)
        self.assertEqual(result, None)

