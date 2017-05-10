import unittest

from app.models.room import Room


class TestRoom(unittest.TestCase):
    def test_room_should_not_create_an_instance_of_room(self):
        name, spaces = 'Room Name', 3
        self.assertRaises(NotImplementedError, Room, name, spaces)
