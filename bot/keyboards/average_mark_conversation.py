import enum
import logging

from telegram import Update
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler

from bot.main import menu

logger = logging.getLogger()


class States(enum.Enum):
    (FACULTY,
     YEAR,
     SPECIALITY,
     SUBJECT) = range(4)


def start(update: Update, context: CallbackContext):
    logger.info("Starting the conv.")
    update.message.reply_text(
        text="Faculty: ",
        reply_markup=ReplyKeyboardRemove()
    )
    return States.FACULTY


def faculty_handler(update: Update, context: CallbackContext):
    context.user_data[States.FACULTY] = update.message.text
    update.message.reply_text(
        text="Year: "
    )
    return States.YEAR


def year_handler(update: Update, context: CallbackContext):
    context.user_data[States.YEAR] = update.message.text
    update.message.reply_text(
        text="Speciality: "
    )
    return States.SPECIALITY


def speciality_handler(update: Update, context: CallbackContext):
    context.user_data[States.SPECIALITY] = update.message.text
    update.message.reply_text(
        text="Subject: "
    )
    return States.SUBJECT


def subject_handler(update: Update, context: CallbackContext):
    context.user_data[States.SUBJECT] = update.message.text
    update.message.reply_text(
        text="\n".join(['%s: %s' % (k, v) for k, v in context.user_data.items()])
    )
    return menu(update, context)


if __name__ == '__main__':
    print(States.CALC)
