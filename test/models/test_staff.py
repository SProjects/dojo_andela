import unittest
from app.models.person import Staff


class TestStaff(unittest.TestCase):
    def setUp(self):
        self.staff = Staff('Staff Name')

    def test_fellow_responds_properties(self):
        self.assertEqual(self.staff.name, 'Staff Name')

