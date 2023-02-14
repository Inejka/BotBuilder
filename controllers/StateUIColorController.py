from typing import Dict

from ui.StateUi import StateUI
from bot.Bot import Bot
from PathFile import Paths
from utils.GetStyleFromFile import get_style


class StateUIColorController:
    def __init__(self, bot: Bot, state_uis: Dict):
        self.bot = bot
        self.state_uis = state_uis
        self.normal_style_css = get_style(Paths.StateUI.value)
        self.start_style_css = get_style(Paths.StateUIStart.value)

    def set_start_state(self, state: StateUI):
        previous_state = self.bot.get_start_state()
        if previous_state is not None:
            self.state_uis[previous_state].setStyleSheet(self.normal_style_css)
        self.bot.set_start_state(state.get_state_id())
        state.setStyleSheet(self.start_style_css)
