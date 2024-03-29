import json

from bot.Transit import Transit
from bot.WithAssociatedFile import WithAssociatedFile
from utils.StrWrapper import StrWrapper


@WithAssociatedFile
class State:
    def __init__(self, inner_id: int) -> None:
        self.__id = "state_" + str(inner_id)
        self.__name = StrWrapper("State" + str(inner_id))
        self.__transits = []

    def get_name(self) -> StrWrapper:
        return self.__name

    def get_id(self) -> str:
        return self.__id

    def get_transits_count(self) -> int:
        return len(self.__transits)

    def add_transit(self, transit: Transit) -> None:
        self.__transits.append(transit)

    def set_name(self, name: str) -> None:
        self.__name.set_str(name)

    def set_id(self, inner_id: str) -> None:
        self.__id = inner_id

    def to_json(self) -> dict:
        # json loads for bot serialization for not to return a str
        # todo find way to remove json loads
        transits = [f.get_id() for f in self.__transits]
        return json.loads(
            '{"id":"' + self.__id + '","name":"' + self.__name.get() + '","transits":' +
            str(transits).replace("'", '"') + ',"associated_file_path":"' +
            self.get_associated_file().replace("\\", "\\\\") + '"}')

    def remove_transit(self, transit: Transit) -> None:
        self.__transits.remove(transit)

    def sort_transits_by_priority(self) -> None:
        self.__transits.sort(key=lambda x: x.get_priority().get(), reverse=True)

    def get_transits(self) -> list[Transit]:
        return self.__transits

    def get_template_body(self) -> str:
        return """import typing


def execute(data: typing.Any) -> None:
    raise NotImplementedError
        """
