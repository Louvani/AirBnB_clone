#!/usr/bin/python3
""" console """
import cmd
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User
import parser


class HBNBCommand(cmd.Cmd):
    ''' Console '''
    prompt = "(hbnb) "
    __models_list = ['Amenity', 'BaseModel',
                     'City', 'Place', 'Review', 'State', 'User']
    __prev_objects = storage.all()

    def emptyline(self):
        """ empty line
        """
        pass

    def do_EOF(self, line):
        ''' Exit the console
        '''
        print()
        return True

    def do_quit(self, line):
        ''' Quit the console
        '''
        return True

    def do_create(self, args):
        ''' Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id.
        Ex: $ create BaseModel
        '''
        arg = args.split(" ")
        if not args:
            print('** class name missing **')
        elif arg[0] not in self.__models_list:
            print('''** class doesn't exist **''')
        else:
            # create basemodel
            new_obj = eval("{}()".format(arg[0]))
            new_obj.save()
            # print the ID
            print(new_obj.id)

    def do_show(self, arg):
        '''Prints the string representation of an instance
        based on the class name and id.
        '''
        if not arg:
            print('** class name missing **')
        else:
            arg = arg.split()
            if arg[0] not in self.__models_list:
                print('''** class doesn't exist **''')
            elif len(arg) == 1:
                print('** instance id missing **')
            else:
                obj_name = "{}.{}".format(arg[0], arg[1])
                if obj_name in self.__prev_objects.keys():
                    print(self.__prev_objects[obj_name])
                else:
                    print('** no instance found **')

    def do_destroy(self, arg):
        '''Deletes an instance based on the class name
        and id (save the change into the JSON file)
        Ex: $ destroy BaseModel 1234-1234-1234.
        '''
        if not arg:
            print('** class name missing **')
        else:
            arg = arg.split()
            if arg[0] not in self.__models_list:
                print('''** class doesn't exist **''')
            elif len(arg) == 1:
                print('** instance id missing **')
            else:
                obj_name = "{}.{}".format(arg[0], arg[1])
                if obj_name in self.__prev_objects.keys():
                    self.__prev_objects.pop(obj_name)
                    storage.save()
                else:
                    print('** no instance found **')

    def do_all(self, args):
        """Prints all string representation of all instances
        Exceptions:
            NameError: when there is no object taht has the name
        """
        my_list = []
        if not args:
            for key in self.__prev_objects.keys():
                my_list.append(self.__prev_objects[key].__str__())
            print(my_list)
            return
        try:
            if args not in self.__models_list:
                raise NameError()
            for key in self.__prev_objects.keys():
                if key.rfind(args) != -1:
                    my_list.append(self.__prev_objects[key].__str__())
            print(my_list)
        except NameError:
            print("** class doesn't exist **")

    def do_update(self, args):
        '''Updates an instance based on the class name and id
        by adding or updating attribute (save the change into
        the JSON file). Ex: $ update BaseModel 1234-1234-1234
        email "aibnb@holbertonschool.com".
        '''
        if not args:
            print("** class name missing **")
        else:
            my_list = args.split()
            if my_list[0] not in self.__models_list:
                print("** class doesn't exist **")
            elif len(my_list) == 1:
                print("** instance id missing **")
            else:
                key = my_list[0] + '.' + my_list[1]
                if key not in self.__prev_objects.keys():
                    print("** no instance found **")
                elif len(my_list) < 3:
                    print("** attribute name missing **")
                elif len(my_list) < 4:
                    print("** value missing **")
                else:
                    self.__prev_objects[key].\
                        __dict__[my_list[2]] = eval(my_list[3])
                    storage.save()

    def do_count(self, args):
        if not args:
            print("** needs class name **")
        elif args in self.__models_list:
            num = 0
            for key in self.__prev_objects.keys():
                if key.rfind(args) != -1:
                    num += 1
            print(num)
        else:
            print("** class doesn't exist **")

    def default(self, line):
        if line.rfind(".all()") != -1:
            self.do_all(line.split(".")[0])
        elif line.rfind(".count()") != -1:
            self.do_count(line.split(".")[0])
        elif line.rfind(".show(") != -1:
            name_class = line.split(".")[0]
            id_num = line.split("\"")[1]
            self.do_show(name_class + " " + id_num)
        elif line.rfind(".destroy(") != -1:
            name_class = line.split(".")[0]
            id_num = line.split("\"")[1]
            self.do_destroy(name_class + " " + id_num)
        else:
            print("** command not found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
