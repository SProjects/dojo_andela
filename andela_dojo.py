"""Andela Dojo

Usage:
    andela_dojo.py create <room_type> <room_name>...
    andela_dojo.py add_person <first_name> <last_name> (TYPE) [<wants_accommodation>]
    andela_dojo.py print_room <room_name>
    andela_dojo.py print_allocations [--o=filename]
    andela_dojo.py print_unallocated [--o=filename]
    andela_dojo.py reallocate_person <first_name> <last_name> <new_room_name>
    andela_dojo.py load_people [--input=filepath]
    andela_dojo.py save_state [--db=sqlite_database]
    andela_dojo.py load_state <sqlite_database>
    andela_dojo.py assign_rooms
    andela_dojo.py reset_system
    andela_dojo.py -i | --interactive
    andela_dojo.py -h | --help
    andela_dojo.py --version

Options:
    -i --interactive  Interactive Mode
    --o=filename   Provide output file [default: output.txt]
    --input=filepath    External input file [default: input.txt]
    --db=sqlite_database    Pass database name as parameter [default: andela_dojo.db]
    -h --help    show help
    --version    show version of the application
"""
from docopt import docopt, DocoptExit

import cmd
import os
import sys

from app.db.utilities import Db
from app.errors.dojo_errors import StaffCantBeAssignedToLivingspace
from app.models.dojo import Dojo

ROOT = os.path.dirname(os.path.abspath(__file__))
db_path = ROOT + '/files/db/'
dojo = Dojo("Andela", "Nairobi")
db = Db()


def docopt_cmd(func):
    """
    Citation: https://github.com/docopt/docopt/blob/master/examples/interactive_example.py

    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.
            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class DojoInteractive(cmd.Cmd):
    intro = 'Welcome to the Andela Dojo!' \
            + ' (type help for a list of commands.)'
    prompt = '(andela_dojo) '
    file = None

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create <room_type> <room_name>..."""
        room_type = args["<room_type>"].upper()
        room_names = [room_name.upper() for room_name in args["<room_name>"]]
        dojo.create_room(room_names, room_type)

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <last_name> <first_name> (TYPE) [<wants_accommodation>]"""
        name = " ".join([args["<last_name>"], args["<first_name>"]])
        person_type = args["TYPE"]
        want_accommodation = args["<wants_accommodation>"] if args["<wants_accommodation>"] else 'N'
        dojo.add_person(name.upper(), person_type.upper(), want_accommodation.upper())

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""
        room_name = args["<room_name>"].upper()
        dojo.print_people_in_room(room_name)

    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [--o=filename]"""
        filename = args["--o"]
        if filename:
            dojo.print_allocated_people_to_file(filename)
        else:
            dojo.print_allocated_people()

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [--o=filename]"""
        filename = args["--o"]
        if filename:
            dojo.print_unallocated_people_to_file(filename)
        else:
            dojo.print_unallocated_people()

    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <last_name> <first_name> <new_room_name>"""
        name = " ".join([args["<last_name>"].upper(), args["<first_name>"].upper()])
        new_room_name = args["<new_room_name>"].upper()
        try:
            dojo.reallocate_person(name, new_room_name)
        except StaffCantBeAssignedToLivingspace as e:
            print e

    @docopt_cmd
    def do_load_people(self, args):
        """Usage: load_people [--input=filepath]"""
        filepath = args['--input']
        dojo.add_people_from_file(filepath)

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=sqlite_database]"""
        database_name = args['--db'] if args['--db'] else 'andela_dojo'
        if database_name == 'andela_dojo':
            if os.path.exists(db_path + database_name + '.db'):
                database = self.read_database(database_name)
            else:
                database = self.initialize_default_db()
        else:
            if os.path.exists(db_path + database_name + '.db'):
                database = self.read_database(database_name)
            else:
                database = self.create_database(database_name)

        dojo.session = database.session
        dojo.save_state()
        dojo.reset()
        dojo.load_state()

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state <sqlite_database>"""
        database_name = args['<sqlite_database>']
        if os.path.exists(db_path + database_name + '.db'):
            database = self.read_database(database_name)
            dojo.session = database.session
            dojo.reset()
            dojo.load_state()
        else:
            print '{}.db does not exit.'.format(database_name)

    @docopt_cmd
    def do_assign_rooms(self, args):
        """Usage: assign_rooms"""
        dojo.assign_rooms_to_unallocated_people()

    @docopt_cmd
    def do_reset_system(self, args):
        """Usage: reset_system"""
        dojo.reset()

    def do_drop_database(self, args):
        """Deletes the currently active database"""
        if db.db_name is None:
            print "No active database detected."
        else:
            self.drop_database()

    def do_quit(self, args):
        """Quits out of Interactive Mode."""
        print('Good Bye!')
        exit()

    def create_database(self, name):
        if name:
            db.create(name)
            return db

    def read_database(self, name):
        if name:
            db.read(name)
            return db

    def initialize_default_db(self):
        db.create('andela_dojo')
        print "Default andela_dojo.db created!"
        return db

    def drop_database(self):
        file_path = db_path + db.db_name + '.db'
        db.drop(file_path)

if __name__ == '__main__':
    opt = docopt(__doc__, sys.argv[1:])
    if opt['--interactive'] or opt['-i']:
        DojoInteractive().cmdloop()
