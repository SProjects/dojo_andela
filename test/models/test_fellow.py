import unittest
from app.models.person import Fellow


class TestFellow(unittest.TestCase):
    def setUp(self):
        self.fellow = Fellow('Fellow Name', 'N')

    def test_fellow_responds_properties(self):
        self.assertEqual(self.fellow.name, 'Fellow Name')

