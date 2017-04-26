import random
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
        self.offices = {}
        self.full_offices = {}
        self.livingspaces = {}
        self.full_livingspaces = {}
        self.fellows = []
        self.staff = []

    def create_room(self, room_names, room_type):
        if not isinstance(room_names, list):
            raise ValueError('Room names must be passed as a list.')

        if room_type == self.OFFICE_ROOM_TYPE:
            self._add_offices(room_names)
        if room_type == self.LIVINGSPACE_ROOM_TYPE:
            self._add_livingspaces(room_names)

    def _add_offices(self, names):
        for name in names:
            if name not in self.offices or name not in self.full_offices:
                self.offices[name] = Office(name)

    def _add_livingspaces(self, names):
        for name in names:
            if name not in self.livingspaces or name not in self.full_livingspaces:
                self.livingspaces[name] = Livingspace(name)

    def add_person(self, name, person_type, accommodation):
        if not isinstance(name, str):
            raise ValueError('Name must be a string')

        if person_type == self.FELLOW_PERSON_TYPE:
            self._add_fellow(name, accommodation)
            self._update_available_livingspaces()
        if person_type == self.STAFF_PERSON_TYPE:
            self._add_staff(name)
        self._update_available_offices()

    def _add_fellow(self, name, accommodation):
        fellow = Fellow(name, accommodation)
        fellow = self._assign_office(fellow)
        fellow = self._assign_livingspace(fellow) if fellow.wants_accommodation() else fellow
        self.fellows.append(fellow)

    def _add_staff(self, name):
        staff = Staff(name)
        staff = self._assign_office(staff)
        self.staff.append(staff)

    def _update_available_livingspaces(self):
        self.livingspaces = {livingspace_name: livingspace for livingspace_name, livingspace in
                             self.livingspaces.items() if livingspace.has_space()}

        self.full_livingspaces = {livingspace_name: livingspace for livingspace_name, livingspace in
                                  self.livingspaces.items() if not livingspace.has_space()}

    def _update_available_offices(self):
        self.offices = {office_name: office for office_name, office in self.offices.items() if
                        office.has_space()}

        self.full_offices = {office_name: office for office_name, office in self.offices.items() if
                             not office.has_space()}

    def _assign_office(self, person):
        if self.offices:
            _, available_office = random.choice(list(self.offices.items()))
            return available_office.assign_person_space(person)
        return person

    def _assign_livingspace(self, fellow):
        if self.livingspaces:
            _, available_livingspace = random.choice(list(self.livingspaces.items()))
            return available_livingspace.assign_fellow_space(fellow)
        return fellow

    def print_people_in_room(self, room_name):
        livingspaces = dict(list(self.full_livingspaces.items()) + list(self.livingspaces.items()))
        if room_name in livingspaces:
            livingspace = livingspaces[room_name]
            livingspace.print_occupants(self.fellows)

        offices = dict(list(self.full_offices.items()) + list(self.offices.items()))
        if room_name in offices:
            office = offices[room_name]
            occupants = self.staff + self.fellows
            office.print_occupants(occupants)

    def print_allocated_people(self):
        spaces = dict(list(self.full_livingspaces.items()) + list(self.livingspaces.items()) +
                      list(self.full_offices.items()) + list(self.offices.items()))

        for space_name, space in spaces.items():
            self.print_people_in_room(space.name)
            print

    def print_unallocated_people(self):
        result = ''
        result += ", ".join(
            [fellow.name.upper() for fellow in self.fellows if not fellow.office or not fellow.livingspace])
        result += ", "
        result += ", ".join([staff.name.upper() for staff in self.staff if not staff.office])
        print result

