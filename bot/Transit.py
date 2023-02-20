import json

from bot.WithAssociatedFile import WithAssociatedFile
from utils.StrWrapper import StrWrapper


@WithAssociatedFile
class Transit:
    def __init__(self, inner_id: int, from_state, to_state, priority: int):
        self.__inner_id = "transit_" + str(inner_id)
        self.__name = StrWrapper("Transit" + str(inner_id))
        self.__to_state = to_state
        self.__from_state = from_state
        self.__priority = priority

    def get_id(self):
        return self.__inner_id

    def get_name(self):
        return self.__name

    def to_json(self):
        # json loads for bot serialization for not to return a str
        # todo find way to remove json loads
        return json.loads('{"inner_id":"' + self.__inner_id + '","name":"' + self.__name.get() + '","to_state":"' \
                          + self.__to_state.get_id() + '","from_state":"' + self.__from_state.get_id() + '","priority":' + str(
            self.__priority) + ',"associated_file_path":"' + self.get_associated_file() + '"}')
