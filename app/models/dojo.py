from room import Office, Livingspace
from person import Fellow, Staff


class Dojo(object):
    OFFICE_ROOM_TYPE = 'OFFICE'
    LIVINGSPACE_ROOM_TYPE = 'LIVINGSPACE'
    FELLOW_PERSON_TYPE = 'FELLOW'
    STAFF_PERSON_TYPE = 'STAFF'

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.offices = []
        self.livingspaces = []
        self.fellows = []
        self.staff = []

    def create_room(self, room_names, room_type):
        if not isinstance(room_names, list):
            raise ValueError('Room names must be passed as a list.')

        if room_type == self.OFFICE_ROOM_TYPE:
            self._add_offices(room_names)
        if room_type == self.LIVINGSPACE_ROOM_TYPE:
            self._add_livingspaces(room_names)

    def _add_offices(self, office_names):
        for name in office_names:
            office = Office(name)
            self.offices.append(office)

    def _add_livingspaces(self, livingspace_names):
        for name in livingspace_names:
            livingspace = Livingspace(name)
            self.livingspaces.append(livingspace)

    def add_person(self, name, person_type, want_living_space):
        if not isinstance(name, str):
            raise ValueError('Name must be a string')

        if person_type == self.FELLOW_PERSON_TYPE:
            self._add_fellow(name, want_living_space)
        if person_type == self.STAFF_PERSON_TYPE:
            self._add_staff(name)

    def _add_fellow(self, name, want_living_space):
        fellow = Fellow(name, want_living_space)
        self.fellows.append(fellow)

    def _add_staff(self, name):
        staff = Staff(name)
        self.staff.append(staff)




