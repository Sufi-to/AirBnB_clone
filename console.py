#!/usr/bin/python3
"""This is the console/entry point to the whole program."""

import cmd
from models.base_model import BaseModel
import json
from models import storage
from shlex import split
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

obj_model = {"BaseModel": BaseModel, "User": User, "City": City, "Place": Place,
               "Review": Review, "State": State}


class HBNBCommand(cmd.Cmd):
    """Displays a command prompt and process commands\n"""
    prompt = "(hbnb) "

    def emptyline(self):
        """ Overrides the default emptyline """
        pass

    def do_EOF(self, line):
        """Exit\n"""
        return True

    def do_quit(self, line):
        """Exit\n"""
        return True

    def do_create(self, line):
        """Create a model and store it in the json file\n"""
        comm = split(line)
        if len(comm) == 0:
            print("** class name missing **")
            return
        elif comm[0] not in obj_model.keys():
            print("** class doesn't exist **")
            return
        else:
            new_obj = obj_model[comm[0]]()
            print(new_obj.id)
            new_obj.save()
            return

    def do_show(self, line):
        """Print the instance using the id\n"""
        comm = split(line)
        if len(comm) == 0:
            print("** class name missing **")
            return
        elif comm[0] not in obj_model.keys():
            print("** class doesn't exist **")
            return
        elif len(comm) <= 1:
            print("** instance id missing **")
            return

        storage.reload()
        all_obj = storage.all()
        get_object_key = comm[0] + "." + comm[1]
        if get_object_key in all_obj:
            get_object = str(all_obj[get_object_key])
            print(get_object)
        else:
            print("** no instance found **")

    def do_destroy(self, line):
        """Delete the instance using the id\n"""
        comm = split(line)
        if len(comm) == 0:
            print("** class name missing **")
            return
        elif comm[0] not in obj_model.keys():
            print("** class doesn't exist **")
            return
        elif len(comm) <= 1:
            print("** instance id missing **")
            return

        storage.reload()
        all_obj = storage.all()
        get_object_key = comm[0] + "." + comm[1]
        if get_object_key in all_obj:
            del all_obj[get_object_key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, line):
        """Print the string represenation of all the instances"""
        disp_list = []
        storage.reload()
        get_objects = storage.all()
        if not line:
            for get_object_key in get_objects:
                disp_list.append(str(get_objects[get_object_key]))
            print(json.dumps(disp_list))
            return

        comm = split(line)
        if comm[0] in obj_model.keys():
            for get_object_key in get_objects:
                if comm[0] in get_object_key:
                    disp_list.append(str(get_objects[get_object_key]))
            print(json.dumps(disp_list))
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """Update the model and store it to the json file
           Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        if not line:
            print("** class name missing **")
            return
        storage.reload()
        get_objects = storage.all()
        comm = split(line)
        if comm[0] not in obj_model.keys():
            print("** class doesn't exist **")

        if len(comm) == 1:
            print("** instance id missing **")
            return
        try:
            get_objects[f'{comm[0]}.{comm[1]}']
        except KeyError:
            print("** no instance found  **")
            return
        if len(comm) == 2:
            print("** attribute name missing **")
            return
        if len(comm) == 3:
            print("** value missing **")
            return
        my_object = get_objects[f'{comm[0]}.{comm[1]}']
        if hasattr(my_object, comm[2]):
            d_type = type(getattr(my_object, comm[2]))
            setattr(my_object, comm[2], d_type(comm[3]))
        else:
            setattr(my_object, comm[2], comm[3])
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
