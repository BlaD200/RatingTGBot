from telegram import ReplyKeyboardMarkup

from bot.localization.localization import get_localize


class User:
    """
    Temporally class; used to simulate user class.
    """

    def __init__(self):
        self.lang = "ukr"

    def get_lang(self):
        return self.lang


def get_base_reply_keyboard(user=User()):
    strings = get_localize(user.get_lang())
    keyboard = [
        [strings.calculate_rating],
        [strings.get_states],
        [strings.settings],
        [strings.edit],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard)
