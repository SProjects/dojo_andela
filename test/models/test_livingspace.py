import unittest
from app.models.room import Livingspace
from app.models.dojo import Dojo
from mock import MagicMock
from app.db.models import Livingspace as DBLivingspace, Fellow as DBFellow


class TestLivingspace(unittest.TestCase):
    def setUp(self):
        self.livingspace = Livingspace('livingspace1')
        self.db_livingspace = DBLivingspace('livingspace1', 4)

        self.dojo = Dojo('Andela', 'Nairobi')
        self.dojo.livingspaces['livingspace1'] = self.livingspace

        self.dojo.session = MagicMock()

    def test_office_responds_to_properties(self):
        self.assertListEqual([self.livingspace.name, self.livingspace.spaces], ['livingspace1', 4])

    def test_save_should_add_livingspace_to_session(self):
        Livingspace.save(self.dojo)
        self.dojo.session.add.assert_called_with(self.db_livingspace)

    def test_should_load_livingspace_from_database(self):
        self.dojo.session.query(DBLivingspace).all = MagicMock(return_value=[self.db_livingspace])
        self.dojo.livingspaces = {}

        Livingspace.load(self.dojo)
        self.assertEqual(self.dojo.livingspaces['livingspace1'], self.livingspace)

    def test_load_adds_full_db_livingspaces_to_the_full_livingspaces_list(self):
        self.dojo.full_livingspaces = {}

        self.full_livingspace = Livingspace('livingspace1')
        self.full_livingspace.spaces = 0

        self.db_livingspace = DBLivingspace('livingspace1', 0)
        self.db_livingspace.fellows = [DBFellow('Fellow1', 'Y'), DBFellow('Fellow1', 'Y'),
                                       DBFellow('Fellow1', 'Y'), DBFellow('Fellow1', 'Y')]
        self.dojo.session.query(DBLivingspace).all = MagicMock(return_value=[self.db_livingspace])

        Livingspace.load(self.dojo)
        self.assertEqual(self.dojo.full_livingspaces['livingspace1'], self.full_livingspace)

    def test_create_from_db_livingspace_creates_office_from_db_livingspace(self):
        result = Livingspace.create_from_db_object(self.db_livingspace)
        self.assertEqual(result, self.livingspace)

    def test_create_from_db_livingspace_returns_none_if_no_db_livingspace_was_passed(self):
        result = Livingspace.create_from_db_object(None)
        self.assertEqual(result, None)


