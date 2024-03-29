import json

from bot.WithAssociatedFile import WithAssociatedFile
from utils.IntWrapper import IntWrapper
from utils.StrWrapper import StrWrapper


@WithAssociatedFile
class Transit:
    def __init__(self, inner_id: int, from_state: "State", to_state: "State", priority: int) -> None:
        self.__inner_id = "transit_" + str(inner_id)
        self.__name = StrWrapper("Transit" + str(inner_id))
        self.__to_state = to_state
        self.__from_state = from_state
        self.__priority = IntWrapper(priority)

    def set_name(self, name: str) -> None:
        self.__name.set_str(name)

    def set_id(self, inner_id: str) -> None:
        self.__inner_id = inner_id

    def get_id(self) -> str:
        return self.__inner_id

    def get_name(self) -> StrWrapper:
        return self.__name

    def to_json(self) -> dict:
        # json loads for bot serialization for not to return a str
        # todo find way to remove json loads
        return json.loads('{"inner_id":"' + self.__inner_id + '","name":"' + self.__name.get() + '","to_state":"'
                          + self.__to_state.get_id() + '","from_state":"' +
                          self.__from_state.get_id() + '","priority":' + str(
            self.__priority) + ',"associated_file_path":"' + self.get_associated_file().replace("\\", "\\\\") + '"}')

    def get_from_state_id(self) -> str:
        return self.__from_state.get_id()

    def get_to_state_id(self) -> str:
        return self.__to_state.get_id()

    def set_to_state(self, state: "State") -> None:
        self.__to_state = state

    def set_from_state(self, state: "State") -> None:
        self.__from_state = state

    def get_priority(self) -> IntWrapper:
        return self.__priority

    def get_to_state(self) -> "State":
        return self.__to_state

    def get_template_body(self) -> str:
        return """import typing


def execute(data: typing.Any) -> bool:
    raise NotImplementedError
        """
