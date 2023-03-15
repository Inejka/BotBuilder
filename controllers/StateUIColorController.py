from PathFile import Paths
from bot.Bot import Bot
from ui.StateUi import StateUI
from utils.GetStyleFromFile import get_style


class StateUIColorController:
    def __init__(self, bot: Bot, state_uis: dict) -> None:
        self.bot = bot
        self.state_uis = state_uis
        self.normal_style_css = get_style(Paths.StateUI)
        self.start_style_css = get_style(Paths.StateUIStart)
        self.end_style_css = get_style(Paths.StateUIEnd)

    def set_start_state(self, state: StateUI) -> None:
        previous_state = self.bot.get_start_state()
        if previous_state is not None:
            self.state_uis[previous_state].setStyleSheet(self.normal_style_css)
        self.bot.set_start_state(state.get_state_id())
        state.setStyleSheet(self.start_style_css)
        self.bot.remove_end_state(state.get_state_id())

    def add_end_state(self, state: StateUI) -> None:
        state.setStyleSheet(self.end_style_css)
        self.bot.add_end_state(state.get_state_id())
        self.bot.clear_start_state(state.get_state_id())

    def remove_end_state(self, state: StateUI) -> None:
        if self.bot.is_end_state(state.get_state_id()):
            self.bot.remove_end_state(state.get_state_id())
            state.setStyleSheet(self.normal_style_css)

    def paint_start_state(self, state: StateUI) -> None:
        state.setStyleSheet(self.start_style_css)

    def paint_end_state(self, state: StateUI) -> None:
        state.setStyleSheet(self.end_style_css)
