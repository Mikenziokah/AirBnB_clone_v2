#!/usr/bin/python3
"""This is the console for AirBnB"""
import cmd
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from shlex import split
from models import storage


class HBNBCommand(cmd.Cmd):
    """this class is entry point of the command interpreter
    """
    prompt = "(hbnb) "
    all_classes = {"BaseModel": BaseModel,
               "City": City,
               "User": User,
               "Place": Place,
               "Review": Review,
               "State": State,
               "Amenity": Amenity}

    def emptyline(self):
        """Ignores empty spaces"""
        pass

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Quit command to exit the program at end of file"""
        return True

    def do_create(self, line):
        "Creates a new instance of BaseModel"
        if len(line) == 0:
            print("** class name missing **")
            return
        
        args = line.split(" ")        
        
        try:
            instance = HBNBCommand.all_classes[args[0]]()
            for parameter in args[1:]:
                key = parameter.split('=')[0].strip("'")
                value = parameter.split('=')[1].strip('"').strip("'")
                if hasattr(instance, key) is True:
                    value = value.replace("_", " ")
                setattr(instance, key, value)
            instance.save()
            print(instance.id)
        except:
            print("** class doesn't exist **")
            return   

    def do_show(self, line):
        """
        Prints the string representation
        of an instance based on the class name and id
        """
        args = line.split(" ")
        if len(line) == 0:
            print("** class name missing **")
            return
            
        if args[0] not in HBNBCommand.all_classes.keys():
            print("** class doesn't exist **")
        else:
            if len(args) == 1:
                print("** instance id missing **")

            if len(args) == 2:
                instance = "{}.{}".format(args[0], args[1])
                for key, values in storage.all().items():
                    if key == instance:
                        print(values)
            
                if instance not in storage.all().keys():
                    print("** no instance found **")

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id
        """
        if line:
            args = line.split(' ')
            if args[0] in HBNBCommand.all_classes:
                if len(args) == 1:
                    print("** instance id missing **")
                else:
                    objs = storage.all()
                    obj = "{}.{}".format(args[0], args[1])
                    if obj in objs.keys():
                        storage.delete(args[0], args[1])
                    else:
                        print("** no instance found **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_all(self, line):
        """Prints all string representation of all instances
        Exceptions:
            NameError: when there is no object taht has the name
        """
        if line:
            args = line.split(" ")
            if args[0] not in HBNBCommand.all_classes:
                print("** class doesn't exist **")
                return
            objects = storage.all(line)
        my_list = []
        if not line:
            objects = storage.all()
            for key in objects:
                my_list.append(objects[key])
            print(my_list)
            return
        # try:
            # args = line.split(" ")
            # if args[0] not in self.all_classes:
            #     raise NameError()
        for key in objects:
            name = key.split('.')
            if name[0] == args[0]:
                my_list.append(objects[key])
        print(my_list)
        # except NameError:
        #     print("** class doesn't exist **")

    def do_update(self, line):
        """Update a instance based on the class name
        """
        if line:
            args = line.split(' ')
            if len(args) == 1:
                print("** instance id missing **")
            elif len(args) == 2:
                print("** attribute name missing **")
            elif len(args) == 3:
                print("** value missing **")
            elif args[0] in HBNBCommand.classes:
                objs = storage.all()
                obj = "{}.{}".format(args[0], args[1])
                if obj in objs.keys():
                    label = getattr(objs[obj], args[2], "")
                    setattr(objs[obj], args[2], type(label)(args[3]))
                    objs[obj].save()
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def count(self, line):
        """count the number of instances of a class
        """
        counter = 0
        try:
            my_list = split(line, " ")
            if my_list[0] not in HBNBCommand.all_classes:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == my_list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """strips the argument and return a string of command
        Args:
            args: input list of args
        Return:
            returns string of argumetns
        """
        new_list = []
        new_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, line):
        """retrieve all instances of a class and
        retrieve the number of instances
        """
        my_list = line.split('.')
        if len(my_list) >= 2:
            if my_list[1] == "all()":
                self.do_all(my_list[0])
            elif my_list[1] == "count()":
                self.count(my_list[0])
            elif my_list[1][:4] == "show":
                self.do_show(self.strip_clean(my_list))
            elif my_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(my_list))
            elif my_list[1][:6] == "update":
                args = self.strip_clean(my_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
