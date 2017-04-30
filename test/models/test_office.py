import unittest
from app.models.room import Office
from app.models.dojo import Dojo
from mock import MagicMock
from app.db.models import Office as DBOffice, Fellow as DBFellow


class TestOffice(unittest.TestCase):
    def setUp(self):
        self.office = Office('office1')
        self.db_office = DBOffice('office1', 6)

        self.dojo = Dojo('Andela', 'Nairobi')
        self.dojo.offices['office1'] = self.office

        self.dojo.session = MagicMock()

    def test_office_responds_to_properties(self):
        self.assertListEqual([self.office.name, self.office.spaces], ['office1', 6])

    def test_save_should_add_office_to_session(self):
        Office.save(self.dojo)
        self.dojo.session.add.assert_called_with(self.db_office)

    def test_should_load_office_from_database(self):
        self.dojo.session.query(DBOffice).all = MagicMock(return_value=[self.db_office])
        self.dojo.offices = {}

        Office.load(self.dojo)
        self.assertEqual(self.dojo.offices['office1'], self.office)

    def test_load_adds_full_db_offices_to_the_full_offices_list(self):
        self.dojo.full_offices = {}

        self.full_office = Office('office1')
        self.full_office.spaces = 0

        self.db_office = DBOffice('office1', 0)
        self.db_office.fellows = [DBFellow('Fellow1', 'Y'), DBFellow('Fellow1', 'Y'),
                                  DBFellow('Fellow1', 'Y'), DBFellow('Fellow1', 'Y'),
                                  DBFellow('Fellow1', 'Y'), DBFellow('Fellow1', 'Y')]
        self.dojo.session.query(DBOffice).all = MagicMock(return_value=[self.db_office])

        Office.load(self.dojo)
        self.assertEqual(self.dojo.full_offices['office1'], self.full_office)

    def test_create_from_db_object_creates_office_from_db_office(self):
        result = Office.create_from_db_object(self.db_office)
        self.assertEqual(result, self.office)

    def test_create_from_db_object_returns_none_if_no_db_office_was_passed(self):
        result = Office.create_from_db_object(None)
        self.assertEqual(result, None)

