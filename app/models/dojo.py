import random, os
from room import Office, Livingspace
from person import Fellow, Staff
from app.errors.dojo_errors import StaffCantBeAssignedToLivingspace
from sqlalchemy.orm import sessionmaker
from app.db.models import engine


class Dojo(object):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    OFFICE_ROOM_TYPE = "OFFICE"
    LIVINGSPACE_ROOM_TYPE = "LIVINGSPACE"
    FELLOW_PERSON_TYPE = "FELLOW"
    STAFF_PERSON_TYPE = "STAFF"

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.offices = {}
        self.full_offices = {}
        self.livingspaces = {}
        self.full_livingspaces = {}
        self.fellows = []
        self.staff = []

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_room(self, room_names, room_type):
        if not isinstance(room_names, list):
            raise ValueError("Room names must be passed as a list.")

        if room_type == self.OFFICE_ROOM_TYPE:
            self._add_offices(room_names)
        if room_type == self.LIVINGSPACE_ROOM_TYPE:
            self._add_livingspaces(room_names)

    def _add_offices(self, names):
        for name in names:
            if name not in self.offices or name not in self.full_offices:
                self.offices[name] = Office(name)
                print "An office called {} has successfully been created.".format(name)

    def _add_livingspaces(self, names):
        for name in names:
            if name not in self.livingspaces or name not in self.full_livingspaces:
                self.livingspaces[name] = Livingspace(name)
                print "A livingspace called {} has successfully been created.".format(name)

    def add_person(self, name, person_type, accommodation):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")

        if person_type == self.FELLOW_PERSON_TYPE:
            self._add_fellow(name, accommodation)
            self._update_available_livingspaces()
        if person_type == self.STAFF_PERSON_TYPE:
            self._add_staff(name)
        self._update_available_offices()

    def add_people_from_file(self):
        file_path = self.ROOT_DIR + "/../../files/input.txt"
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                for line in f.readlines():
                    tokens = line.strip().split(" ")
                    name, person_type = " ".join(tokens[:2]), tokens[2]
                    accommodation = tokens[3:][0] if tokens[3:] else 'N'
                    self.add_person(name, person_type, accommodation)

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
        unallocated_fellows = self._unallocated_fellows()
        unallocated_staff = self._unallocated_staff()

        if unallocated_fellows:
            print "UNALLOCATED FELLOWS"
            print "------------------------"
            print ", ".join([fellow.name.upper() for fellow in unallocated_fellows])
            print

        if unallocated_staff:
            print "UNALLOCATED STAFF"
            print "------------------------"
            print ", ".join([staff.name.upper() for staff in unallocated_staff])

    def _unallocated_fellows(self):
        return [fellow for fellow in self.fellows if not fellow.office or not fellow.livingspace]

    def _unallocated_staff(self):
        return [staff for staff in self.staff if not staff.office]

    def print_allocated_people_to_file(self, filename):
        file_path = self.ROOT_DIR + "/../../files/" + filename
        result_string = self._generate_allocated_print_statement()

        with open(file_path, "w") as f:
            f.write(result_string)

    def _generate_allocated_print_statement(self):
        livingspaces = dict(list(self.full_livingspaces.items()) + list(self.livingspaces.items()))
        offices = dict(list(self.full_offices.items()) + list(self.offices.items()))
        occupants = self.staff + self.fellows

        livingspace_string = ''
        for livingspace_name, livingspace in livingspaces.items():
            livingspace_string += livingspace_name.upper()
            livingspace_string += "\n------------------------\n"
            livingspace_string += ", ".join(
                [occupant.name.upper() for occupant in livingspace.get_occupants(self.fellows)])
            livingspace_string += "\n\n"

        office_string = ''
        for office_name, office in offices.items():
            office_string += office_name.upper()
            office_string += "\n------------------------\n"
            office_string += ", ".join([occupant.name.upper() for occupant in office.get_occupants(occupants)])
            office_string += "\n\n"

        return livingspace_string + office_string

    def print_unallocated_people_to_file(self, filename):
        file_path = self.ROOT_DIR + "/../../files/" + filename
        result_string = self._generate_unallocated_print_statement()

        with open(file_path, "w") as f:
            f.write(result_string)

    def _generate_unallocated_print_statement(self):
        unallocated_fellows = self._unallocated_fellows()
        unallocated_staff = self._unallocated_staff()

        fellow_string = ''
        if unallocated_fellows:
            fellow_string = "UNALLOCATED FELLOWS"
            fellow_string += "\n------------------------\n"
            fellow_string += ", ".join([fellow.name.upper() for fellow in unallocated_fellows])
            fellow_string += "\n\n"

        staff_string = ''
        if unallocated_staff:
            staff_string = "UNALLOCATED STAFF"
            staff_string += "\n------------------------\n"
            staff_string += ", ".join([staff.name.upper() for staff in unallocated_staff])
            staff_string += "\n\n"

        return fellow_string + staff_string

    def reallocate_person(self, identifier, new_room_name):
        fellow = [fellow for fellow in self.fellows if identifier == fellow.name]
        staff = [staff for staff in self.staff if identifier == staff.name]

        new_office = self.offices.get(new_room_name, None)
        new_livingspace = self.livingspaces.get(new_room_name, None)

        if fellow and new_office:
            fellow = fellow[0]
            fellow_index = self.fellows.index(fellow)
            self._reassign_fellow_to_new_office(fellow, fellow_index, new_office)
        if fellow and new_livingspace:
            fellow = fellow[0]
            fellow_index = self.fellows.index(fellow)
            self._reassign_fellow_to_new_livingspace(fellow, fellow_index, new_livingspace)
        if staff and new_office:
            staff = staff[0]
            staff_index = self.staff.index(staff)
            self._reassign_staff_to_new_office(staff, staff_index, new_office)
        if staff and new_livingspace:
            raise StaffCantBeAssignedToLivingspace("Staff can't be assigned a livingspace.")

    def _reassign_fellow_to_new_office(self, fellow, index, new_office):
        fellow.office = new_office
        self.fellows[index] = fellow

    def _reassign_fellow_to_new_livingspace(self, fellow, index, new_livingspace):
        fellow.livingspace = new_livingspace
        self.fellows[index] = fellow

    def _reassign_staff_to_new_office(self, staff, index, new_office):
        staff.office = new_office
        self.staff[index] = staff

    def save_state(self):
        Office.save(self)
        Livingspace.save(self)
        self.session.commit()

        Fellow.save(self)
        Staff.save(self)
        self.session.commit()

    def load_state(self):
        Office.load(self)
        Livingspace.load(self)
        Fellow.load(self)
        Staff.load(self)
        return self



