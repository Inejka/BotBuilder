import json
import os
from typing import List

from PathFile import Paths
from bot.State import State
from bot.Transit import Transit
from utils.StrWrapper import StrWrapper


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
        if end_state_id in self.__end_states:
            del self.__end_states[end_state_id]

    def clear_start_state(self, start_state_id: str) -> None:
        if self.__start_state is not None and self.__start_state.get_id() == start_state_id:
            self.__start_state = None

    def is_end_state(self, end_state_id: str) -> bool:
        return end_state_id in self.__end_states

    def clear(self):
        self.__states = {}
        self.__transits = {}
        self.__state_counter = 0
        self.__transit_counter = 0
        self.__start_state = None
        self.__end_states = {}

    def save(self):
        with open(os.path.join(Paths.BotGeneratedFolder, "bot.json"), 'w') as file:
            json.dump(self, file, default=Bot.to_json, indent=4)

    def to_json(self):
        # json loads for bot serialization for not to return a str
        # todo find way to remove json loads
        to_return = "{"
        to_return += '"states":' + (json.dumps(self.__states, default=State.to_json))
        to_return += ',"transits":' + (json.dumps(self.__transits, default=Transit.to_json))
        to_return += ',"state_counter":' + str(self.__state_counter)
        to_return += ',"transit_counter":' + str(self.__transit_counter)
        to_return += ',"start_state":"' + (
            self.__start_state.get_id() if self.__start_state is not None else "None") + '"'
        to_return += ',"end_states":' + json.dumps(self.__end_states, default=State.get_id)
        to_return += "}"
        return json.loads(to_return)

    def load(self):
        with open(os.path.join(Paths.BotGeneratedFolder, "bot.json"), 'r') as file:
            self.from_json(json.load(file))

    def from_json(self, json_parsed):
        # todo remove unnecessary information from json such as:
        # bot->states->transits
        # bot->states from dict to list
        # bot->states from dict to list
        # bot->end states from dict to list
        self.__state_counter = json_parsed["state_counter"]
        self.__transit_counter = json_parsed["transit_counter"]
        for _, state in json_parsed["states"].items():
            self.load_state(state)
        for _, transit in json_parsed["transits"].items():
            self.load_transit(transit)
        self.load_start_end_states(json_parsed["start_state"], json_parsed["end_states"])

    def load_state(self, load_from):
        state = State(load_from["id"][load_from["id"].rfind("_") + 1:])
        state.set_name(load_from["name"])
        state.set_associated_file(load_from["associated_file_path"])
        self.__states[load_from["id"]] = state

    def load_transit(self, load_from):
        transit = Transit(load_from["inner_id"][load_from["inner_id"].rfind("_") + 1:],
                          self.__states[load_from["from_state"]],
                          self.__states[load_from["to_state"]], load_from["priority"])
        transit.set_name(load_from["name"])
        transit.set_associated_file(load_from["associated_file_path"])
        self.__transits[transit.get_id()] = transit
        self.__states[load_from["from_state"]].add_transit(transit)

    def load_start_end_states(self, start_state_id, end_states):
        self.__start_state = self.__states[start_state_id] if not start_state_id == "None" else None
        for _, i in end_states.items():
            self.__end_states[i] = self.__states[i]

    def get_name_wrapper_by_state_id(self, state_id) -> StrWrapper:
        return self.__states[state_id].get_name()

    def get_name_wrapper_by_transit_id(self, transit_id) -> StrWrapper:
        return self.__transits[transit_id].get_name()

    def get_transit_by_id(self, transit_id) -> Transit:
        return self.__transits[transit_id]

    def get_state_by_id(self, state_id) -> State:
        return self.__states[state_id]

    def remove_transit_by_id(self, transit_id) -> None:
        transit = self.__transits[transit_id]
        self.__states[transit.get_from_state_id()].remove_transit(transit)
        self.__transits.pop(transit_id)

    def get_associated_transit_by_state_id(self, state_id) -> dict:
        to_return = {"starts": [], "ends": []}
        for transit in self.__transits.values():
            if transit.get_from_state_id() == state_id:
                to_return["starts"].append(transit.get_id())
                continue
            if transit.get_to_state_id() == state_id:
                to_return["ends"].append(transit.get_id())
                continue
        return to_return

    def remove_state_by_id(self, transit_id) -> None:
        # it doesn't remove state transit, because it removes StateUIController at moment
        self.__states.pop(transit_id)
