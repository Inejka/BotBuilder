class IntWrapper:
    def __init__(self):
        self.__inner = 0

    def __init__(self, init_with):
        self.__inner = init_with

    def __str__(self):
        return str(self.__inner)

    def set_int(self, inner):
        self.__inner = inner

    def get(self):
        return self.__inner
