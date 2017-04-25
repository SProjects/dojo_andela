import unittest
from app.models.dojo import Dojo


class TestDojo(unittest.TestCase):
    def setUp(self):
        self.dojo = Dojo('Andela Dojo', 'Nairobi')

    def test_dojo_responds_to_its_properties(self):
        self.assertListEqual([self.dojo.name, self.dojo.location], ['Andela Dojo', 'Nairobi'])


