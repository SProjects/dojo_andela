from room import Office


class Dojo(object):
    OFFICE_ROOM_TYPE = 'OFFICE'

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.offices = []

    def create_room(self, room_names, room_type):
        if room_type == self.OFFICE_ROOM_TYPE:
            self._add_offices(room_names)

    def _add_offices(self, office_names):
        for name in office_names:
            office = Office(name)
            self.offices.append(office)




