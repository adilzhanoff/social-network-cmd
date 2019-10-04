class Friend:
    # constructor
    def __init__(self, usr_id=None, lst_friend=[], lst_sent=[]):
        self.__usr_id = usr_id
        self.__lst_friend = lst_friend
        self.__lst_sent = lst_sent

    # functions
    def set_id(self, usr_id):
        self.__usr_id = usr_id

    def set_list(self, lst_friend):
        self.__lst_friend = lst_friend

    def set_sent(self, lst_sent):
        self.__lst_sent = lst_sent

    def get_id(self):
        return self.__usr_id

    def get_list(self):
        return self.__lst_friend

    def get_sent(self):
        return self.__lst_sent
