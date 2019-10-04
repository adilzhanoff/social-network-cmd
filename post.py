class Post:
    # construcor
    def __init__(self, crt=None, id=None, txt=None):
        self.__crt = crt
        self.__id = id
        self.__txt = txt

    # functions
    def set_crt(self, crt):
        self.__crt = crt

    def set_id(self, id):
        self.__id = id

    def set_txt(self, txt):
        self.__txt = txt

    def get_crt(self):
        return self.__crt

    def get_id(self):
        return self.__id

    def get_txt(self):
        return self.__txt
