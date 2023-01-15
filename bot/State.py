from utils.StrWrapper import StrWrapper
from bot.Transit import Transit
from bot.WithAssociatedFile import WithAssociatedFile
import os

@WithAssociatedFile
class State:
    def __init__(self, inner_id):
        self.__id = "state_" + str(inner_id)
        self.__name = StrWrapper("State" + str(inner_id))
        self.__transits = []

    def get_name(self) -> StrWrapper:
        return self.__name

    def get_id(self) -> str:
        return self.__id

    def get_transits_count(self) -> int:
        return len(self.__transits)

    def add_transit(self, transit: Transit):
        self.__transits.append(transit)

