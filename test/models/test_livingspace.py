import unittest
from app.models.room import Livingspace


class TestLivingspace(unittest.TestCase):
    def setUp(self):
        self.livingspace = Livingspace('livingspace1')

    def test_office_responds_to_properties(self):
        self.assertListEqual([self.livingspace.name, self.livingspace.spaces], ['livingspace1', 4])