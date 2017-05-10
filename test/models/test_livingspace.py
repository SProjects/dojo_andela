from mock import MagicMock

import unittest

from app.models.room import Livingspace
from app.db.models import Livingspace as DBLivingspace, Fellow as DBFellow


class TestLivingspace(unittest.TestCase):
    def setUp(self):
        livingspace_name = 'livingspace1'
        self.livingspace = Livingspace(livingspace_name)
        self.livingspaces = {livingspace_name: self.livingspace}
        self.full_livingspaces = {}

        self.db_livingspace = DBLivingspace(livingspace_name, 4)
        self.session = MagicMock()

    def test_office_responds_to_properties(self):
        self.assertListEqual([self.livingspace.name, self.livingspace.spaces], ['livingspace1', 4])

    def test_repr_returns_livingspace_name(self):
        self.assertEqual(self.livingspace.__repr__(), 'livingspace1')

    def test_save_should_add_livingspace_to_session(self):
        self.session.query(DBLivingspace).filter_by(name=self.livingspace.name).first = MagicMock(return_value=None)

        Livingspace.save(self.session, self.livingspaces, self.full_livingspaces)
        self.session.add.assert_called_with(self.db_livingspace)

    def test_should_load_livingspace_from_database(self):
        self.session.query(DBLivingspace).all = MagicMock(return_value=[self.db_livingspace])
        self.livingspaces = {}

        livingspaces, full_livingspaces = Livingspace.load(self.session)
        self.assertEqual(livingspaces['livingspace1'], self.livingspace)
        self.assertEqual(full_livingspaces, {})

    def test_load_adds_full_db_livingspaces_to_the_full_livingspaces_list(self):
        self.full_livingspace = Livingspace('livingspace1')
        self.full_livingspace.spaces = 0

        self.db_livingspace = DBLivingspace('livingspace1', 0)
        self.db_livingspace.fellows = [DBFellow('Fellow1', 'Y'), DBFellow('Fellow1', 'Y'),
                                       DBFellow('Fellow1', 'Y'), DBFellow('Fellow1', 'Y')]
        self.session.query(DBLivingspace).all = MagicMock(return_value=[self.db_livingspace])

        livingspaces, full_livingspaces = Livingspace.load(self.session)
        self.assertEqual(full_livingspaces['livingspace1'], self.full_livingspace)
        self.assertEqual(livingspaces, {})

    def test_create_from_db_livingspace_creates_office_from_db_livingspace(self):
        result = Livingspace.create_from_db_object(self.db_livingspace)
        self.assertEqual(result, self.livingspace)

    def test_create_from_db_livingspace_returns_none_if_no_db_livingspace_was_passed(self):
        result = Livingspace.create_from_db_object(None)
        self.assertEqual(result, None)


