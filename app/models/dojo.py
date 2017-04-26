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
        self.offices = []
        self.full_offices = []
        self.livingspaces = []
        self.full_livingspaces = []
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
        self.livingspaces = [livingspace for livingspace in self.livingspaces if livingspace.has_space()]
        self.full_livingspaces = [livingspace for livingspace in self.livingspaces if not livingspace.has_space()]

    def _update_available_offices(self):
        self.offices = [office for office in self.offices if office.has_space()]
        self.full_offices = [office for office in self.offices if not office.has_space()]

    def _assign_office(self, person):
        if self.offices:
            available_office = random.choice(self.offices)
            return available_office.assign_person_space(person)
        return person

    def _assign_livingspace(self, fellow):
        if self.livingspaces:
            available_livingspace = random.choice(self.livingspaces)
            return available_livingspace.assign_fellow_space(fellow)
        return fellow

    def print_people_in_room(self, room_name):
        livingspaces = self.full_livingspaces + self.livingspaces
        if room_name in [livingspace.name for livingspace in livingspaces]:
            livingspace = [livingspace for livingspace in livingspaces if livingspace.name == room_name][0]
            livingspace.print_occupants(self.fellows)

        offices = self.full_offices + self.offices
        if room_name in [office.name for office in offices]:
            office = [office for office in offices if office.name == room_name][0]
            occupants = self.staff + self.fellows
            office.print_occupants(occupants)

    def print_allocated_people(self):
        spaces = self.full_livingspaces + self.livingspaces + self.full_offices + self.offices
        for space in spaces:
            self.print_people_in_room(space.name)
            print

    def print_unallocated_people(self):
        result = ''
        result += ", ".join(
            [fellow.name.upper() for fellow in self.fellows if not fellow.office or not fellow.livingspace])
        result += ", "
        result += ", ".join([staff.name.upper() for staff in self.staff if not staff.office])
        print result

