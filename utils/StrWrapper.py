class StrWrapper:
    def __init__(self):
        self.__inner = ""

    def __init__(self, init_with):
        self.__inner = init_with

    def __str__(self):
        return self.__inner

    def set_str(self, inner):
        self.__inner = inner

    def get(self):
        return self.__inner
