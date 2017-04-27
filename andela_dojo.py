"""Andela Dojo

Usage:
    andela_dojo.py create <room_type> <room_name>...
    andela_dojo.py -i | --interactive
    andela_dojo.py -h | --help
    andela_dojo.py --version

Options:
    -i --interactive  Interactive Mode
    -h --help    show help
    --version    show version of the application
"""

import sys, cmd
from docopt import docopt, DocoptExit
from app.models.dojo import Dojo


dojo = Dojo("Andela", "Nairobi")


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

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print('Good Bye!')
        exit()


if __name__ == '__main__':
    opt = docopt(__doc__, sys.argv[1:])
    if opt['--interactive'] or opt['-i']:
        DojoInteractive().cmdloop()
