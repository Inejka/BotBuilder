class IntWrapper:

    def __init__(self, init_with: int) -> None:
        self.__inner = init_with

    def __str__(self) -> str:
        return str(self.__inner)

    def set_int(self, inner: int) -> None:
        self.__inner = inner

    def get(self) -> int:
        return self.__inner
