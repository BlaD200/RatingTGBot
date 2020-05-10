from telegram import ReplyKeyboardMarkup

from bot.localization.localization import get_localize
from bot.user import User


def get_menu_keyboard(user=User()):
    strings = get_localize(user.get_lang())
    keyboard = [
        [strings.calculate_rating],
        [strings.get_states],
        [strings.settings],
        [strings.edit],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard)
