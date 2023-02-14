from typing import List

from bot.State import State
from bot.Transit import Transit


class Bot:
    def __init__(self):
        self.__states = {}
        self.__transits = {}
        self.__state_counter = 0
        self.__transit_counter = 0
        self.__start_state = None
        self.__end_states = {}

    def create_state(self):
        state = State(self.__state_counter)
        self.__states[state.get_id()] = state
        self.__state_counter += 1
        return state.get_name(), state.get_id()

    def create_transit(self, from_state_id: str, to_state_id: str):
        transit = Transit(self.__transit_counter, self.__states[from_state_id], self.__states[to_state_id],
                          self.__states[from_state_id].get_transits_count())
        self.__transits[transit.get_id()] = transit
        self.__transit_counter += 1
        self.__states[from_state_id].add_transit(transit)
        return transit.get_name(), transit.get_id()

    def set_start_state(self, start_state_id: str) -> None:
        self.__start_state = self.__states[start_state_id]

    def get_start_state(self) -> str:
        return self.__start_state.get_id() if self.__start_state is not None else None

    def add_end_state(self, end_state_id: str) -> None:
        self.__end_states[end_state_id] = self.__states[end_state_id]

    def get_end_states(self) -> List:
        return list(self.__end_states.keys())

    def remove_end_state(self, end_state_id: str) -> None:
        del self.__end_states[end_state_id]
