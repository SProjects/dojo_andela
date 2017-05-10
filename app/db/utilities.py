import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import *


class Db(object):
    def __init__(self):
        self.db_name = None
        self.engine = None
        self.session = None

    def create(self, db_name):
        self.db_name = db_name
        self.engine = create_engine('sqlite:///./files/db/' + self.db_name + '.db')
        Base.metadata.create_all(self.engine)
        self._create_session()
        return self

    def read(self, db_name):
        self.db_name = db_name
        self.engine = create_engine('sqlite:///./files/db/' + self.db_name + '.db')
        self._create_session()
        return self

    def _create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def drop(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            print "{}.db has been deleted!".format(self.db_name)


