from utils.StrWrapper import StrWrapper
from bot.WithAssociatedFile import WithAssociatedFile

@WithAssociatedFile
class Transit:
    def __init__(self, inner_id: int, to_state, from_state, priority: int):
        self.__inner_id = "transit_" + str(inner_id)
        self.__name = StrWrapper("Transit" + str(inner_id))
        self.__to_state = to_state
        self.__from_state = from_state
        self.__priority = priority

    def get_id(self):
        return self.__inner_id

    def get_name(self):
        return self.__name
