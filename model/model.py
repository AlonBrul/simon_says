import random
from constants import BUTTON_TEXT_PAD


class Rectangle:
    """Rectangle we show on the screen
    :param dim - (height, width), position, color
    :return:
    """
    def __init__(self, dim, position, color):
        self.dim = dim
        self.position = position
        self.color = color
        self.main_color = color
        self.secondary_color = (
            color[0] + (255 - color[0]) * 1 / 4,
            color[1] + (255 - color[1]) * 1 / 2,
            color[2] + (255 - color[2]) * 3 / 4,)

    def get_height(self):
        return self.dim[0]

    def get_width(self):
        return self.dim[1]

    def set_color(self, color):
        """
        :param color: Tuple that represent RGB color
        :return:
        """
        self.color = color


class Button(Rectangle):
    """
    :param
    :return:
    """
    def __init__(self, dim, position, color, sound_path="", text=None, on_click=None):
        super().__init__(dim, position, color)
        self.sound_path = sound_path
        txt_pos = (self.position[0] + BUTTON_TEXT_PAD[0], self.position[1] + BUTTON_TEXT_PAD[1])
        self.text = Text(text, txt_pos)
        self.on_click = on_click

    def set_text_msg(self, msg):
        """
        :param msg: a string
        :return:
        """
        self.text.msg = msg

    def get_text_msg(self):
        """
        :param
        :return: the string msg
        """
        return self.text.msg

    def has_text_msg(self):
        return self.text.msg is not None


class Simon:
    """ Simon is responsible to show the steps and set the lvl
    :param
    :return:
    """
    def __init__(self):
        self.challenge = []
        self.steps_to_show = []
        self.lvl = 1

    def init_challenge(self, custom_lvl):
        if custom_lvl is not None:
            self.challenge = custom_lvl[:]
            self.lvl = len(custom_lvl)

        else:
            self.steps_to_show = []
            num = random.randint(0, 3)
            self.challenge.append(num)

        self.steps_to_show = self.challenge[:]


class Memento:
    def __init__(self, state) -> None:
        self._state = state

    def get_saved_state(self):
        return self._state


class Originator:
    _state = None

    def set(self, state) -> None:
        self._state = state

    def save_to_memento(self) -> Memento:
        return Memento(self._state)

    def restore_from_memento(self, memento) -> None:
        self._state = memento.get_saved_state()


class Player:
    """ Player needs to follow simon steps, this class also saves the player name and tracks the player score.
    :param
    :return:
    """
    def __init__(self, player_name, all_scores):
        self.score = 0
        self.steps_done = []
        self.total_score = 0
        self.name = player_name
        for name, score in all_scores:
            if name == self.name:
                self.total_score = score


class Text:
    """ Text we want to show on the screen.
      :param small: if we want the font to be small
      :return:
      """
    def __init__(self, msg, pos, small=False):
        self.msg = msg
        self.pos = pos
        self.small = small
