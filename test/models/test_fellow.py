import unittest
from app.models.person import Fellow
from mock import MagicMock
from app.db.models import Fellow as DBFellow, Office as DBOffice, Livingspace as DBLivingspace
from app.models.room import Office, Livingspace


class TestFellow(unittest.TestCase):
    def setUp(self):
        self.fellow = Fellow('Fellow Name', 'N')
        self.db_fellow = DBFellow('Fellow Name', 'N')

        self.db_office = DBOffice('Office1', 5)
        self.db_fellow.office = self.db_office

        self.office = Office('Office1')
        self.office.spaces = 5

        self.db_livingspace = DBLivingspace('Livingspace1', 3)
        self.db_fellow.livingspace = self.db_livingspace

        self.livingspace = Livingspace('Livingspace1')
        self.livingspace.spaces = 3

        self.fellows = [self.fellow]
        self.session = MagicMock()

    def test_fellow_responds_properties(self):
        self.assertEqual(self.fellow.name, 'Fellow Name')

    def test_should_add_a_new_fellow_database_session(self):
        Fellow.save(self.session, self.fellows)
        self.session.add.assert_called_with(self.db_fellow)

    def test_should_load_a_fellow_from_the_database(self):
        self.session.query(DBFellow).all = MagicMock(return_value=[self.db_fellow])
        self.session.query(DBOffice).filter_by = MagicMock(return_value=self.db_office)
        self.session.query(DBLivingspace).filter_by = MagicMock(return_value=self.db_livingspace)

        result_fellows = Fellow.load(self.session)
        self.assertListEqual(result_fellows, [self.fellow])
        self.assertEqual(result_fellows[0].office, self.office)
        self.assertEqual(result_fellows[0].livingspace, self.livingspace)

    def test_get_db_office_object_from_database(self):
        self.fellow.get_office_from_db(self.session, self.office)
        self.session.query(DBOffice).filter_by.assert_called_with(name=self.office.name)

    def test_get_db_livingspace_object_from_database(self):
        self.fellow.get_livingspace_from_db(self.session, self.livingspace)
        self.session.query(DBLivingspace).filter_by.assert_called_with(name=self.livingspace.name)


