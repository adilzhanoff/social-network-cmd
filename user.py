from friend import Friend
from enumpy import Enum


class User:
    # constructor
    def __init__(self, id=None, log=None, name=None,
                 surname=None, password=None, friends=Friend(),
                 access=[Enum(3)]):
        """
        'access' - privacy settings
        'access[0]' - true by default, access to view a wall
        """
        self.__id = id
        self.__log = log
        self.__name = name
        self.__surname = surname
        self.__pass = password
        self.__friends = friends
        self.__access = access

    # functions
    def set_id(self, id):
        self.__id = id

    def set_log(self, log):
        self.__log = log

    def set_name(self, name):
        self.__name = name

    def set_surname(self, surname):
        self.__surname = surname

    def set_pass(self, password):
        self.__pass = password

    def set_friends(self, friends):
        self.__friends = friends

    def set_access(self, access):
        self.__access = access

    def get_id(self):
        return self.__id

    def get_log(self):
        return self.__log

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_pass(self):
        return self.__pass

    def get_friends(self):
        return self.__friends

    def get_access(self):
        return self.__access
