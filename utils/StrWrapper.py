class StrWrapper:

    def __init__(self, init_with: str) -> None:
        self.__inner = init_with

    def __str__(self) -> str:
        return self.__inner

    def set_str(self, inner: str) -> None:
        self.__inner = inner

    def get(self) -> str:
        return self.__inner
