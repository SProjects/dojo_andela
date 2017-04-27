"""Andela Dojo

Usage:
    andela_dojo.py create <room_type> <room_name>...
    andela_dojo.py add_person <person_name> (FELLOW | STAFF) [wants_accommodation]
    andela_dojo.py print_room <room_name>
    andela_dojo.py print_allocations [-o FILENAME]
    andela_dojo.py print_unallocated [-o FILENAME]
    andela_dojo.py reallocate_person <person_identifier> <new_room_name>
    andela_dojo.py -i | --interactive
    andela_dojo.py -h | --help
    andela_dojo.py --version

Options:
    -i --interactive  Interactive Mode
    -o FILENAME --output=FILENAME   Provide output file [default: output.txt]
    -h --help    show help
    --version    show version of the application
"""

import sys, cmd
from docopt import docopt, DocoptExit
from app.models.dojo import Dojo
from app.errors.dojo_errors import StaffCantBeAssignedToLivingspace


dojo = Dojo("Andela", "Nairobi")
dojo.load_state()


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
        room_names = args["<room_name>"]
        dojo.create_room(room_names, room_type)

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <person_name> <FELLOW|STAFF> [wants_accommodation]"""
        print args

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""
        room_name = args["<room_name>"]
        dojo.print_people_in_room(room_name)

    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [-o FILENAME]"""
        output_to_file = args["-o"]
        filename = args["FILENAME"]
        if output_to_file and filename:
            dojo.print_allocated_people_to_file(filename)
        else:
            dojo.print_allocated_people()

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [-o FILENAME]"""
        output_to_file = args["-o"]
        filename = args["FILENAME"]
        if output_to_file and filename:
            dojo.print_unallocated_people_to_file(filename)
        else:
            dojo.print_unallocated_people()

    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""
        name = args["<person_identifier>"]
        new_room_name = args["<new_room_name>"]
        try:
            dojo.reallocate_person(name, new_room_name)
        except StaffCantBeAssignedToLivingspace as e:
            print e

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print('Good Bye!')
        exit()


if __name__ == '__main__':
    opt = docopt(__doc__, sys.argv[1:])
    if opt['--interactive'] or opt['-i']:
        DojoInteractive().cmdloop()
