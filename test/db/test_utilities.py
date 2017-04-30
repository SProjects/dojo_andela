import unittest
from app.db.models import *
from app.db.utilities import Db
from mock import MagicMock, mock, patch


class TestUtilities(unittest.TestCase):
    def setUp(self):
        self.db = Db()

    def test_db_responds_to_its_properties(self):
        self.assertListEqual([self.db.db_name, self.db.engine, self.db.session], [None, None, None])

    def test_create_create_all_with_engine_object(self):
        fake_path = 'sqlite:///./files/fake_db.db'
        sqlalchemy = MagicMock()
        sqlalchemy.create_engine = MagicMock(return_value=mock)
        fake_engine = sqlalchemy.create_engine(fake_path)

        Base.metadata = MagicMock()
        Base.metadata.create_all = MagicMock()
        Base.metadata.create_all(fake_engine)

        sqlalchemy.orm = MagicMock()
        sqlalchemy.orm.sessionmaker = MagicMock(return_value=mock)
        sqlalchemy.orm.sessionmaker(bind=fake_engine)

        self.db.create('fake_db')
        sqlalchemy.create_engine.assert_called_with(fake_path)
        sqlalchemy.orm.sessionmaker.assert_called_with(bind=fake_engine)

    def test_read_creates_engine_for_existing_database(self):
        existing_fake_path = 'sqlite:///./files/existing_fake_db.db'
        sqlalchemy = MagicMock()
        sqlalchemy.create_engine = MagicMock(return_value=mock)
        fake_engine = sqlalchemy.create_engine(existing_fake_path)

        sqlalchemy.orm = MagicMock()
        sqlalchemy.orm.sessionmaker = MagicMock(return_value=mock)
        sqlalchemy.orm.sessionmaker(bind=fake_engine)

        self.db.read('existing_fake_db')
        sqlalchemy.create_engine.assert_called_with(existing_fake_path)
        sqlalchemy.orm.sessionmaker.assert_called_with(bind=fake_engine)

    @patch('app.db.utilities.os.path')
    @patch('app.db.utilities.os')
    def test_drop_delete_an_existing_database(self, mock_os, mock_path):
        fake_file_path = 'fake/file/path.db'
        mock_path.exists.return_value = False
        self.db.drop(fake_file_path)

        self.assertFalse(mock_os.remove.called)

        mock_path.exists.return_value = True
        self.db.drop(fake_file_path)

        mock_os.remove.assert_called_with(fake_file_path)
