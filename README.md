ANDELA DOJO
===========

**Introduction**

Andela Dojo is a commandline application that creates offices and livingspaces at the Dojo and randomly assigns them to the 
Dojo's available space. When commanded, the application can store this data into either the default sqlite database or 
one whose name is supplied by the user of the application.

**Technology Stack**
* Python 2.7
* Sqlite database

**Pre-requisites**
* Install [Python v2.7.*](https://www.python.org/downloads/)
* Install [virtualenv and/or virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

**Setup**
* Create a virtualenv and activate it.
* Clone the repository and `cd` into the project root.
* Run `pip install -r requirements.txt`
* Start the application `python andela_dojo.py -i`
* If you get a welcome message and a prompt ```(andela_dojo)```, congratulations you have setup correctly.

**Usage**
* To get all commands type `help` at the (andela_dojo) prompt. 
* To get help for a particular command type `help command_name`.
* Create a new room `create_room room_type room_names1 room_name2`. Replace `<room_type>` with either OFFICE or LIVINGSPACE.
* Add fellow to dojo `add_person first_name last_name FELLOW Y | N`. Use either Y(yes) or N(no) at the end 
indicates if the fellow wants accommodation.
* Add staff to dojo `add_staff first_name last_name STAFF`.
* Print people allocated to a particular room `print_room room_name`
* Print all room allocations in the dojo `print_allocations`.
* Create text file with all room allocations in the dojo `print_allocations --o=filename.txt`.
* Print unallocated people in the dojo `print_unallocated`.
* Create text file with all unallocated people at the dojo `print_unallocated --o=filename.txt`. 
* Reallocate fellow or staff at dojo yto another office or livingspace `reallocate_person first_name last_name room_name`. `room_name`
refers to the name you gave an office or livingspace.
* Add people to the dojo from a text file `load_people`
* Save the dojo state to a database `save_state`.
* Load data from the database `load_state database_name.db`. Default database is ```andela_dojo.db```.
* Assign rooms to fellows or staff in the system that were previously unallocated `assign_rooms`. 
 


