class Enum:  # Class that creates enumerator object
    # constructor
    # 'num' - number of counter values, by default 2 - 0 and 1
    def __init__(self, num=2):
        self.__num = num
        self.__count = 0

    # functions
    def set_count(self, count):
        self.__count = count

    def set_num(self, num):
        self.__num = num

    def get_count(self):
        return self.__count

    def get_num(self):
        return self.__num

    def enum_inc(self, n=1):  # increases enumerator's value by 'n'
        if n == 1:
            if self.get_count() == self.get_num() - 1:
                self.set_count(0)
            else:
                self.set_count(self.get_count() + 1)
        else:
            if self.get_count() == self.get_num() - 1:
                self.set_count(0)

                for _ in range(n - 1):
                    self.enum_inc()
            else:
                for _ in range(n):
                    self.enum_inc()

    def enum_dec(self, n=1):  # decreases enumerator's value by 'n'
        if n == 1:
            if self.get_count() == 0:
                self.set_count(self.get_num() - 1)
            else:
                self.set_count(self.get_count() - 1)
        else:
            if self.get_count() == 0:
                self.set_count(self.get_num() - 1)

                for _ in range(n - 1):
                    self.enum_dec()
            else:
                for _ in range(n):
                    self.enum_dec()
